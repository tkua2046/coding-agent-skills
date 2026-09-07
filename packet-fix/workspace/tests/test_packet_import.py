import os
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile, ZipInfo

from packet_import import import_packet, preview


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive = self.root / "packet.zip"
        self._write_packet(
            ("handouts/", b""),
            ("handouts/day 1.txt", b"Bring pencils.\n"),
            ("agenda ☃.txt", b"Doors open at nine.\n"),
        )

    def _write_packet(self, *entries):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with ZipFile(self.archive, "w") as packet:
                for name, content in entries:
                    packet.writestr(name, content)

    def _write_damaged_deflate_packet(self):
        with ZipFile(self.archive, "w", compression=ZIP_DEFLATED) as packet:
            packet.writestr("file.txt", b"workshop payload " * 20)
        corrected = self.archive.read_bytes()
        with ZipFile(self.archive) as packet:
            member = packet.getinfo("file.txt")
            header_offset = member.header_offset
        name_length = int.from_bytes(
            corrected[header_offset + 26 : header_offset + 28], "little"
        )
        extra_length = int.from_bytes(
            corrected[header_offset + 28 : header_offset + 30], "little"
        )
        payload_offset = header_offset + 30 + name_length + extra_length
        damaged = bytearray(corrected)
        damaged[payload_offset] = (damaged[payload_offset] & 0xF9) | 0x06
        self.archive.write_bytes(damaged)
        return corrected

    def assert_rejected_without_import(self, *entries):
        self._write_packet(*entries)
        target = self.root / "received"
        before = set(self.root.iterdir())
        with self.assertRaises(ValueError):
            preview(self.archive)
        self.assertEqual(set(self.root.iterdir()), before)
        with self.assertRaises(ValueError):
            import_packet(self.archive, target)
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

    def test_preview_lists_sorted_files_without_extracting(self):
        before = set(self.root.iterdir())
        self.assertEqual(preview(self.archive), ["agenda ☃.txt", "handouts/day 1.txt"])
        self.assertEqual(set(self.root.iterdir()), before)

    def test_import_preserves_content_and_names(self):
        target = self.root / "received"
        self.assertEqual(import_packet(self.archive, target), preview(self.archive))
        self.assertEqual((target / "handouts/day 1.txt").read_bytes(), b"Bring pencils.\n")
        self.assertEqual((target / "agenda ☃.txt").read_bytes(), b"Doors open at nine.\n")

    def test_invalid_member_paths_are_rejected(self):
        for name in (
            "/absolute.txt",
            "back\\slash.txt",
            "drive:C.txt",
            "",
            "a//b.txt",
            "./a.txt",
            "a/../b.txt",
            "directory//",
        ):
            with self.subTest(name=name):
                self.assert_rejected_without_import((name, b"payload"))

    def test_duplicate_and_conflicting_paths_are_rejected(self):
        cases = (
            (("same.txt", b"one"), ("same.txt", b"two")),
            (("same/", b""), ("same", b"file")),
            (("parent", b"file"), ("parent/child.txt", b"child")),
            (("parent/child.txt", b"child"), ("parent", b"file")),
        )
        for entries in cases:
            with self.subTest(entries=[entry[0] for entry in entries]):
                self.assert_rejected_without_import(*entries)

    def test_unix_symlinks_and_special_files_are_rejected(self):
        for mode in (stat.S_IFLNK | 0o777, stat.S_IFIFO | 0o600):
            with self.subTest(mode=mode):
                info = ZipInfo("special")
                info.create_system = 3
                info.external_attr = mode << 16
                self.assert_rejected_without_import((info, b"target"))

    def test_entries_without_unix_file_type_metadata_are_valid(self):
        info = ZipInfo("plain.txt")
        info.create_system = 3
        info.external_attr = 0o600 << 16
        self._write_packet((info, b"plain bytes"))
        target = self.root / "received"
        self.assertEqual(preview(self.archive), ["plain.txt"])
        self.assertEqual(import_packet(self.archive, target), ["plain.txt"])
        self.assertEqual((target / "plain.txt").read_bytes(), b"plain bytes")

    def test_existing_destinations_are_not_overwritten(self):
        directory = self.root / "received"
        directory.mkdir()
        keep = directory / "keep.txt"
        keep.write_text("local note")
        with self.assertRaises(FileExistsError):
            import_packet(self.archive, directory)
        self.assertEqual(keep.read_text(), "local note")

        dangling = self.root / "dangling"
        dangling.symlink_to(self.root / "missing")
        with self.assertRaises(FileExistsError):
            import_packet(self.archive, dangling)
        self.assertTrue(dangling.is_symlink())

        file = self.root / "existing-file"
        file.write_bytes(b"keep me")
        with self.assertRaises(FileExistsError):
            import_packet(self.archive, file)
        self.assertEqual(file.read_bytes(), b"keep me")

    def test_corrupt_data_leaves_no_destination_or_temporary_folder(self):
        payload = b"unique uncompressed workshop payload"
        self._write_packet(("file.txt", payload))
        damaged = self.archive.read_bytes().replace(payload, b"X" * len(payload), 1)
        self.archive.write_bytes(damaged)
        target = self.root / "received"
        before = set(self.root.iterdir())
        with self.assertRaises(BadZipFile):
            import_packet(self.archive, target)
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

    def test_malformed_deflate_is_bad_zip_and_retryable(self):
        corrected = self._write_damaged_deflate_packet()
        target = self.root / "received"
        before = set(self.root.iterdir())

        with self.assertRaises(BadZipFile):
            import_packet(self.archive, target)
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

        self.archive.write_bytes(corrected)
        self.assertEqual(import_packet(self.archive, target), ["file.txt"])
        self.assertEqual((target / "file.txt").read_bytes(), b"workshop payload " * 20)

    def test_write_and_final_placement_failures_are_cleaned_up_and_retryable(self):
        target = self.root / "received"
        before = set(self.root.iterdir())
        with mock.patch("packet_import.shutil.copyfileobj", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                import_packet(self.archive, target)
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

        with mock.patch("packet_import.os.rename", side_effect=OSError("rename failed")):
            with self.assertRaises(OSError):
                import_packet(self.archive, target)
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

        self.assertEqual(import_packet(self.archive, target), preview(self.archive))

    def test_destination_appears_only_after_all_files_are_written(self):
        target = self.root / "received"
        real_rename = os.rename

        def checked_rename(source, destination):
            self.assertEqual(Path(destination), target)
            self.assertFalse(os.path.lexists(target))
            self.assertEqual(
                sorted(
                    path.relative_to(source).as_posix()
                    for path in Path(source).rglob("*")
                    if path.is_file()
                ),
                ["agenda ☃.txt", "handouts/day 1.txt"],
            )
            real_rename(source, destination)

        with mock.patch("packet_import.os.rename", side_effect=checked_rename):
            import_packet(self.archive, target)
        self.assertTrue(target.is_dir())

    def test_cli_failure_has_no_traceback_or_success_listing(self):
        self._write_packet(("../escape.txt", b"no"))
        command = [
            sys.executable,
            "packet_import.py",
            "import",
            str(self.archive),
            str(self.root / "received"),
        ]
        result = subprocess.run(
            command,
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.root / "received").exists())

    def test_cli_malformed_deflate_has_clean_error_and_is_retryable(self):
        corrected = self._write_damaged_deflate_packet()
        project = Path(__file__).resolve().parents[1]
        target = self.root / "received"
        before = set(self.root.iterdir())
        command = [
            sys.executable,
            "packet_import.py",
            "import",
            str(self.archive),
            str(target),
        ]

        failed = subprocess.run(command, cwd=project, text=True, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("corrupt compressed data", failed.stderr)
        self.assertNotIn("Traceback", failed.stderr)
        self.assertEqual(failed.stdout, "")
        self.assertFalse(os.path.lexists(target))
        self.assertEqual(set(self.root.iterdir()), before)

        self.archive.write_bytes(corrected)
        retried = subprocess.run(command, cwd=project, text=True, capture_output=True)
        self.assertEqual(retried.returncode, 0, retried.stderr)
        self.assertEqual(retried.stdout, "file.txt\n")
        self.assertEqual((target / "file.txt").read_bytes(), b"workshop payload " * 20)

    def test_cli_commands_print_the_sorted_success_listing(self):
        project = Path(__file__).resolve().parents[1]
        expected = "agenda ☃.txt\nhandouts/day 1.txt\n"
        preview_result = subprocess.run(
            [sys.executable, "packet_import.py", "preview", str(self.archive)],
            cwd=project,
            text=True,
            capture_output=True,
        )
        self.assertEqual(preview_result.returncode, 0, preview_result.stderr)
        self.assertEqual(preview_result.stdout, expected)

        target = self.root / "received"
        import_result = subprocess.run(
            [
                sys.executable,
                "packet_import.py",
                "import",
                str(self.archive),
                str(target),
            ],
            cwd=project,
            text=True,
            capture_output=True,
        )
        self.assertEqual(import_result.returncode, 0, import_result.stderr)
        self.assertEqual(import_result.stdout, expected)
        self.assertEqual((target / "agenda ☃.txt").read_bytes(), b"Doors open at nine.\n")


if __name__ == "__main__":
    unittest.main()
