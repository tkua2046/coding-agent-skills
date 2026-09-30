"""Evaluator-only behavioral checks. Usage: python accept.py WORKER_DIRECTORY."""
import importlib.util
import stat
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path
from zipfile import BadZipFile, ZipFile, ZipInfo

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
work = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("packet_import", work / "packet_import.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(call, errors, message):
    try:
        call()
    except errors:
        return
    raise AssertionError(message)


def snapshot(root):
    result = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = ("link", str(path.readlink()))
        elif path.is_file():
            result[relative] = ("file", path.read_bytes())
        else:
            result[relative] = ("directory",)
    return result


def archive(path, members):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with ZipFile(path, "w") as packet:
            for name, content in members:
                packet.writestr(name, content)


with tempfile.TemporaryDirectory(prefix="oracle-", dir=ROOT) as temporary:
    root = Path(temporary)
    parent = root / "collections"
    parent.mkdir()
    (parent / "keep.txt").write_bytes(b"local notes\n")
    source, destination = root / "packet.zip", parent / "received"
    members = [("notes/", b""), ("notes/day 1.txt", b"Pencils\n"),
               ("agenda.txt", b"09:00\n"), ("notes/café.bin", bytes(range(256)))]
    archive(source, members)
    names = sorted(name for name, _ in members if not name.endswith("/"))
    before = snapshot(root)
    check(module.preview(source) == names, "valid preview listing")
    check(snapshot(root) == before, "preview must not write")
    check(module.import_packet(source, destination) == names, "valid import listing")
    for name, data in members:
        if not name.endswith("/"):
            check((destination / name).read_bytes() == data, "file bytes changed")
    imported = snapshot(root)
    rejects(lambda: module.import_packet(source, destination), FileExistsError, "existing destination accepted")
    check(snapshot(root) == imported, "existing destination or neighbors changed")
    destination = parent / "retry"

    link = ZipInfo("linked.txt")
    link.create_system = 3
    link.external_attr = (stat.S_IFLNK | 0o777) << 16
    fifo = ZipInfo("pipe")
    fifo.create_system = 3
    fifo.external_attr = (stat.S_IFIFO | 0o600) << 16
    bad_packets = [[(name, b"escape")] for name in (
        "../keep.txt", "nested/../../keep.txt", str(parent / "keep.txt"),
        "C:escape.txt", "nested\\escape.txt", "./note.txt", "a//b.txt", "a/../b.txt")]
    bad_packets += [[("same.txt", b"one"), ("same.txt", b"two")],
                    [("node", b"file"), ("node/leaf.txt", b"child")],
                    [("node/leaf.txt", b"child"), ("node", b"file")],
                    [("node/", b""), ("node", b"file")], [(link, b"../keep.txt")], [(fifo, b"")]]
    for index, bad_members in enumerate(bad_packets):
        archive(source, [("innocent.txt", b"first"), *bad_members])
        before = snapshot(root)
        rejects(lambda: module.preview(source), ValueError, f"unsafe preview accepted: {index}")
        check(snapshot(root) == before, f"unsafe preview wrote files: {index}")
        rejects(lambda: module.import_packet(source, destination), ValueError, f"unsafe import accepted: {index}")
        check(snapshot(root) == before, f"failed import changed files or leaked staging: {index}")

    archive(source, members)
    destination.symlink_to(parent / "missing-folder", target_is_directory=True)
    before = snapshot(root)
    rejects(lambda: module.import_packet(source, destination), FileExistsError, "dangling destination symlink accepted")
    check(snapshot(root) == before, "destination symlink changed")
    destination.unlink()

    archive(source, [("first.txt", b"written first"), ("late.txt", b"late-content-for-crc-check")])
    raw = source.read_bytes()
    check(raw.count(b"late-content-for-crc-check") == 1, "invalid evaluator corruption setup")
    source.write_bytes(raw.replace(b"late-content-for-crc-check", b"LATE-content-for-crc-check"))
    before = snapshot(root)
    rejects(lambda: module.import_packet(source, destination), (BadZipFile, ValueError, OSError), "corrupt ZIP accepted")
    check(snapshot(root) == before, "read failure left partial destination or staging")

    def cli(*arguments):
        return subprocess.run([sys.executable, "-B", str(work / "packet_import.py"), *map(str, arguments)],
                              cwd=work, text=True, capture_output=True, timeout=15)

    failed = cli("import", source, destination)
    check(failed.returncode != 0 and failed.stderr and not failed.stdout
          and "Traceback" not in failed.stderr, "failed CLI import needs an honest clean error")
    check(snapshot(root) == before, "failed CLI import changed files")
    archive(source, members)
    expected = "".join(name + "\n" for name in names)
    listing = cli("preview", source)
    check((listing.returncode, listing.stdout, listing.stderr) == (0, expected, ""), "preview CLI compatibility")
    result = cli("import", source, destination)
    check((result.returncode, result.stdout, result.stderr) == (0, expected, ""), "retry/CLI compatibility")
    check((parent / "keep.txt").read_bytes() == b"local notes\n", "neighbor was modified")
print("PASS: packet content, path boundary, rejection cleanup, retry and CLI behavior")
