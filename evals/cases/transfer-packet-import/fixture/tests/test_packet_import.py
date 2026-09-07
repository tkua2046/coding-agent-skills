import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from packet_import import import_packet, preview


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive = self.root / "packet.zip"
        with ZipFile(self.archive, "w") as packet:
            packet.writestr("handouts/", b"")
            packet.writestr("handouts/day 1.txt", b"Bring pencils.\n")
            packet.writestr("agenda.txt", b"Doors open at nine.\n")

    def test_preview_lists_files(self):
        self.assertEqual(preview(self.archive), ["agenda.txt", "handouts/day 1.txt"])

    def test_import_preserves_content(self):
        target = self.root / "received"
        self.assertEqual(import_packet(self.archive, target), preview(self.archive))
        self.assertEqual((target / "handouts/day 1.txt").read_bytes(), b"Bring pencils.\n")

    def test_existing_destination_is_not_overwritten(self):
        target = self.root / "received"
        target.mkdir()
        (target / "keep.txt").write_text("local note")
        with self.assertRaises(FileExistsError):
            import_packet(self.archive, target)
        self.assertEqual(list(target.iterdir()), [target / "keep.txt"])


if __name__ == "__main__":
    unittest.main()
