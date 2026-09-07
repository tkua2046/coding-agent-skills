import os
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock
from zipfile import BadZipFile, ZIP_STORED, ZipFile, ZipInfo

import packet_import
from packet_import import import_packet, preview


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive = self.root / "packet.zip"
        self.write_archive(
            [
                ("handouts/", b""),
                ("handouts/day 1.txt", b"Bring pencils.\n"),
                ("caf\N{LATIN SMALL LETTER E WITH ACUTE}/notes \N{SNOWMAN}.txt", b"\x00\xffnotes\n"),
                ("agenda.txt", b"Doors open at nine.\n"),
            ]
        )

    def write_archive(self, entries):
        with ZipFile(self.archive, "w", compression=ZIP_STORED) as packet:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                for entry in entries:
                    name, contents, *mode = entry
                    member = ZipInfo(name)
                    if mode:
                        member.create_system = 3
                        member.external_attr = mode[0] << 16
                    packet.writestr(member, contents)

    def assert_no_import_artifacts(self, destination):
        self.assertFalse(os.path.lexists(destination))
        self.assertFalse(
            any(
                path.name.startswith(f".{destination.name}.import-")
                for path in self.root.iterdir()
            )
        )

    def test_preview_lists_sorted_files_without_creating_anything(self):
        before = sorted(self.root.iterdir())

        self.assertEqual(
            preview(self.archive),
            [
                "agenda.txt",
                "caf\N{LATIN SMALL LETTER E WITH ACUTE}/notes \N{SNOWMAN}.txt",
                "handouts/day 1.txt",
            ],
        )
        self.assertEqual(sorted(self.root.iterdir()), before)

    def test_import_preserves_bytes_and_places_complete_folder_at_once(self):
        target = self.root / "received"
        real_rename = os.rename

        def inspect_then_rename(staging, destination):
            self.assertFalse(os.path.lexists(destination))
            self.assertEqual(
                (Path(staging) / "handouts/day 1.txt").read_bytes(),
                b"Bring pencils.\n",
            )
            self.assertEqual(
                (
                    Path(staging)
                    / "caf\N{LATIN SMALL LETTER E WITH ACUTE}/notes \N{SNOWMAN}.txt"
                ).read_bytes(),
                b"\x00\xffnotes\n",
            )
            real_rename(staging, destination)

        with mock.patch("packet_import.os.rename", side_effect=inspect_then_rename):
            names = import_packet(self.archive, target)

        self.assertEqual(names, preview(self.archive))
        self.assertEqual((target / "handouts/day 1.txt").read_bytes(), b"Bring pencils.\n")

    def test_rejects_invalid_member_paths_in_preview_and_import(self):
        invalid_names = [
            "",
            "/absolute.txt",
            "C:drive.txt",
            "back\\slash.txt",
            "one//two.txt",
            "./dot.txt",
            "one/../two.txt",
            "../parent.txt",
            "directory//",
        ]
        for index, name in enumerate(invalid_names):
            with self.subTest(name=name):
                self.write_archive([(name, b"unsafe")])
                before = sorted(self.root.iterdir())
                with self.assertRaises(ValueError):
                    preview(self.archive)
                self.assertEqual(sorted(self.root.iterdir()), before)

                target = self.root / f"invalid-{index}"
                with self.assertRaises(ValueError):
                    import_packet(self.archive, target)
                self.assert_no_import_artifacts(target)

    def test_rejects_duplicate_and_file_directory_conflicts_in_either_order(self):
        conflicting_entries = [
            [("same.txt", b"one"), ("same.txt", b"two")],
            [("node", b"file"), ("node/", b"")],
            [("node/", b""), ("node", b"file")],
            [("parent", b"file"), ("parent/child.txt", b"child")],
            [("parent/child.txt", b"child"), ("parent", b"file")],
        ]
        for index, entries in enumerate(conflicting_entries):
            with self.subTest(entries=[entry[0] for entry in entries]):
                self.write_archive(entries)
                with self.assertRaises(ValueError):
                    preview(self.archive)
                target = self.root / f"conflict-{index}"
                with self.assertRaises(ValueError):
                    import_packet(self.archive, target)
                self.assert_no_import_artifacts(target)

    def test_rejects_unix_symlinks_and_special_files(self):
        for index, file_type in enumerate((stat.S_IFLNK, stat.S_IFIFO, stat.S_IFSOCK)):
            with self.subTest(file_type=file_type):
                self.write_archive([("special", b"target", file_type | 0o644)])
                with self.assertRaises(ValueError):
                    preview(self.archive)
                target = self.root / f"special-{index}"
                with self.assertRaises(ValueError):
                    import_packet(self.archive, target)
                self.assert_no_import_artifacts(target)

    def test_existing_destination_is_not_overwritten(self):
        target = self.root / "received"
        target.mkdir()
        (target / "keep.txt").write_text("local note")
        with self.assertRaises(FileExistsError):
            import_packet(self.archive, target)
        self.assertEqual(list(target.iterdir()), [target / "keep.txt"])

    def test_dangling_destination_symlink_is_existing_and_unchanged(self):
        target = self.root / "received"
        target.symlink_to(self.root / "missing-target", target_is_directory=True)

        with self.assertRaises(FileExistsError):
            import_packet(self.archive, target)

        self.assertTrue(target.is_symlink())
        self.assertEqual(os.readlink(target), str(self.root / "missing-target"))

    def test_archive_read_failure_cleans_staging_and_allows_retry(self):
        payload = b"unique packet contents"
        self.write_archive([("handout.txt", payload)])
        damaged = bytearray(self.archive.read_bytes())
        offset = damaged.index(payload)
        damaged[offset] ^= 0xFF
        self.archive.write_bytes(damaged)
        target = self.root / "received"

        with self.assertRaises(BadZipFile):
            import_packet(self.archive, target)
        self.assert_no_import_artifacts(target)

        self.write_archive([("handout.txt", payload)])
        self.assertEqual(import_packet(self.archive, target), ["handout.txt"])
        self.assertEqual((target / "handout.txt").read_bytes(), payload)

    def test_write_failure_cleans_staging_and_preserves_other_parent_files(self):
        target = self.root / "received"
        keep = self.root / "keep.txt"
        keep.write_text("unrelated")

        def fail_after_writing(packet, members, staging):
            (staging / "partial.txt").write_text("partial")
            raise OSError("simulated write failure")

        with mock.patch("packet_import._copy_members", side_effect=fail_after_writing):
            with self.assertRaises(OSError):
                import_packet(self.archive, target)

        self.assert_no_import_artifacts(target)
        self.assertEqual(keep.read_text(), "unrelated")

    def test_final_placement_failure_cleans_staging(self):
        target = self.root / "received"
        with mock.patch("packet_import.os.rename", side_effect=OSError("simulated rename failure")):
            with self.assertRaises(OSError):
                import_packet(self.archive, target)
        self.assert_no_import_artifacts(target)

    def test_cli_failure_has_no_traceback_or_success_listing(self):
        self.write_archive([("../escape.txt", b"unsafe")])
        target = self.root / "received"
        result = subprocess.run(
            [
                sys.executable,
                str(Path(packet_import.__file__)),
                "import",
                str(self.archive),
                str(target),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("error:", result.stderr)
        self.assert_no_import_artifacts(target)

    def test_cli_preview_and_import_print_sorted_file_names(self):
        expected = (
            "agenda.txt\n"
            "caf\N{LATIN SMALL LETTER E WITH ACUTE}/notes \N{SNOWMAN}.txt\n"
            "handouts/day 1.txt\n"
        )
        script = str(Path(packet_import.__file__))
        preview_result = subprocess.run(
            [sys.executable, script, "preview", str(self.archive)],
            text=True,
            capture_output=True,
            check=False,
        )
        target = self.root / "received"
        import_result = subprocess.run(
            [sys.executable, script, "import", str(self.archive), str(target)],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(
            (preview_result.returncode, preview_result.stdout, preview_result.stderr),
            (0, expected, ""),
        )
        self.assertEqual(
            (import_result.returncode, import_result.stdout, import_result.stderr),
            (0, expected, ""),
        )
        self.assertEqual(
            (
                target
                / "caf\N{LATIN SMALL LETTER E WITH ACUTE}/notes \N{SNOWMAN}.txt"
            ).read_bytes(),
            b"\x00\xffnotes\n",
        )


if __name__ == "__main__":
    unittest.main()
