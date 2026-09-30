import tempfile
import unittest
from pathlib import Path
from transcript import Cue, load_cues, render_cues, timestamp


class TranscriptTests(unittest.TestCase):
    def test_load_preserves_order_and_text(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as tmp:
            path = Path(tmp) / "cues.tsv"
            path.write_text("start_ms\tend_ms\ttext\n0\t1500\t Hello! \n1000\t2000\tAgain\n")
            self.assertEqual(load_cues(path), [Cue(0, 1500, " Hello! "), Cue(1000, 2000, "Again")])

    def test_rejects_backward_interval(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as tmp:
            path = Path(tmp) / "bad.tsv"
            path.write_text("start_ms\tend_ms\ttext\n200\t100\tbad\n")
            with self.assertRaises(ValueError):
                load_cues(path)

    def test_rendering(self):
        self.assertEqual(timestamp(3723004), "01:02:03.004")
        self.assertEqual(render_cues([Cue(0, 1500, "Hello")]), "00:00:00.000 --> 00:00:01.500 Hello")
        self.assertEqual(render_cues([]), "")


if __name__ == "__main__":
    unittest.main()
