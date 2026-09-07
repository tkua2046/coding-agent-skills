import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from transcript import Cue, find_cues, load_cues, render_cues, timestamp


ROOT = Path(__file__).resolve().parents[1]


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

    def test_find_cues_uses_unicode_casefold_and_literal_phrase(self):
        cues = [
            Cue(0, 1000, "Die Straße."),
            Cue(1000, 2000, "Die Strasse!"),
            Cue(2000, 3000, " padded phrase "),
        ]

        self.assertEqual(find_cues(cues, "STRASSE."), [cues[0]])
        self.assertEqual(find_cues(cues, " phrase "), [cues[2]])
        self.assertEqual(find_cues(cues, "phrase "), [cues[2]])
        self.assertEqual(find_cues(cues, "Strasse?"), [])

    def test_find_cues_does_not_match_across_cues(self):
        cues = [Cue(0, 1000, "one half"), Cue(1000, 2000, "other half")]

        self.assertEqual(find_cues(cues, "half other"), [])

    def test_find_cues_merges_context_in_source_order_without_mutation(self):
        cues = [
            Cue(0, 1000, "before"),
            Cue(1000, 2000, "match"),
            Cue(2000, 3000, "between"),
            Cue(3000, 4000, "match"),
            Cue(4000, 5000, "after"),
        ]
        original = list(cues)

        result = find_cues(cues, "MATCH", context=1)

        self.assertEqual(result, cues)
        self.assertEqual(len(result), 5)
        self.assertEqual(cues, original)
        self.assertIs(result[1], cues[1])
        self.assertIs(result[3], cues[3])

    def test_find_cues_validates_arguments_before_searching(self):
        for phrase in ("", " \t\n", None, 12):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                find_cues([], phrase)
        for context in (-1, 1.5, True, "1"):
            with self.subTest(context=context), self.assertRaises(ValueError):
                find_cues([], "valid", context=context)

    def test_cli_find_with_context_uses_existing_rendering(self):
        result = self.run_cli("--find", "STRASSE", "--context", "1")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "00:00:00.000 --> 00:00:01.000 Before\n"
            "00:00:01.000 --> 00:00:02.000 Die Straße.\n"
            "00:00:02.000 --> 00:00:03.000 After\n",
        )
        self.assertEqual(result.stderr, "")

    def test_cli_without_search_still_renders_full_transcript(self):
        result = self.run_cli()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "00:00:00.000 --> 00:00:01.000 Before\n"
            "00:00:01.000 --> 00:00:02.000 Die Straße.\n"
            "00:00:02.000 --> 00:00:03.000 After\n",
        )
        self.assertEqual(result.stderr, "")

    def test_cli_no_matches_succeeds_silently(self):
        result = self.run_cli("--find", "missing")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_cli_rejects_invalid_search_options_cleanly(self):
        cases = [
            (("--context", "1"), "--find"),
            (("--find", "anything", "--context", "-1"), "context"),
            (("--find", "   "), "phrase"),
        ]
        for arguments, error_text in cases:
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn(error_text, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def run_cli(self, *arguments):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            path = Path(tmp) / "cues.tsv"
            path.write_text(
                "start_ms\tend_ms\ttext\n"
                "0\t1000\tBefore\n"
                "1000\t2000\tDie Straße.\n"
                "2000\t3000\tAfter\n",
                encoding="utf-8",
            )
            return subprocess.run(
                [sys.executable, str(ROOT / "transcript.py"), str(path), *arguments],
                capture_output=True,
                text=True,
                check=False,
            )


if __name__ == "__main__":
    unittest.main()
