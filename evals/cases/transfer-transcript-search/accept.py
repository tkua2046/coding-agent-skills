"""Evaluator-only behavioral checks. Usage: python accept.py [WORKER_DIRECTORY], or python -c SOURCE in the workspace."""
import contextlib
import csv
import importlib.util
import io
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
work = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
ROOT = work
spec = importlib.util.spec_from_file_location("transcript", work / "transcript.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(call, message):
    try:
        call()
    except ValueError:
        return
    raise AssertionError(message)


check(hasattr(module, "find_cues"), "missing requested find_cues API")
Cue, find = module.Cue, module.find_cues
texts = ["Opening", "River path", "bridge", "RIVER PATH reopened", "Straße map",
         "[draft]", "draft", "river", "path", "River path", "Closing"]
cues = [Cue(i * 2000, i * 2000 + 1500, text) for i, text in enumerate(texts)]
before = list(cues)
with contextlib.redirect_stdout(io.StringIO()) as emitted:
    check(find(cues, "river PATH") == [cues[i] for i in (1, 3, 9)], "literal per-cue matching")
    check(find(cues, "river path", context=1) == [cues[i] for i in (*range(5), 8, 9, 10)],
          "context union must deduplicate and preserve source order")
    check(find(cues, "strasse") == [cues[4]], "Unicode casefold matching")
    check(find(cues, "[draft]") == [cues[5]], "punctuation must remain literal")
    check(find(cues, " river") == [], "nonempty phrase must not be trimmed")
    check(find(cues, "absent", context=20) == [], "no match must not select context")
    check(find(cues, "Opening", context=100) == cues, "context clipped to transcript bounds")
    check(find([], "hello", context=1) == [], "empty transcript")
    for phrase in ("", " \t\n"):
        rejects(lambda: find([], phrase), "invalid phrase accepted on empty transcript")
    for context in (-1, True, False, 1.5, "1"):
        rejects(lambda: find([], "river", context=context), "invalid context accepted")
check(cues == before, "input was changed")
check(not emitted.getvalue(), "library search must return results without printing")

with tempfile.TemporaryDirectory(prefix="oracle-", dir=ROOT) as temporary:
    path = Path(temporary) / "source.tsv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["start_ms", "end_ms", "text"])
        writer.writerows((c.start_ms, c.end_ms, c.text) for c in cues)

    def cli(*arguments):
        return subprocess.run([sys.executable, "-B", str(work / "transcript.py"), str(path), *arguments],
                              cwd=work, text=True, capture_output=True, timeout=15)

    def expected(indices):
        return "".join(f"00:00:{i * 2:02}.000 --> 00:00:{i * 2 + 1:02}.500 {texts[i]}\n" for i in indices)

    full = cli()
    check((full.returncode, full.stdout, full.stderr) == (0, expected(range(len(cues))), ""),
          "existing CLI output changed")
    found = cli("--find", "RIVER path", "--context", "1")
    check((found.returncode, found.stdout, found.stderr) == (0, expected((*range(5), 8, 9, 10)), ""),
          "search CLI output")
    none = cli("--find", "absent")
    check((none.returncode, none.stdout, none.stderr) == (0, "", ""), "empty search CLI output")
    for arguments in (("--context", "1"), ("--context", "-1"), ("--find", " "),
                      ("--find", "river", "--context", "-1")):
        result = cli(*arguments)
        check(result.returncode != 0 and result.stderr and not result.stdout
              and "Traceback" not in result.stderr, "CLI must explain invalid input cleanly")
print("PASS: transcript search behavior and existing CLI compatibility")
