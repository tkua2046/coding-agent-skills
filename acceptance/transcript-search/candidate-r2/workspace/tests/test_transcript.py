import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from transcript import Cue, find_cues, load_cues, main, render_cues, timestamp


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

    def test_find_is_unicode_case_insensitive_and_literal(self):
        cues = [
            Cue(0, 100, "Die Straße, damals"),
            Cue(100, 200, "STRASSE damals"),
            Cue(200, 300, "Strasse damals"),
        ]

        self.assertEqual(find_cues(cues, "STRASSE,"), [cues[0]])
        self.assertEqual(find_cues(cues, "straße"), cues)

    def test_find_does_not_span_cues(self):
        cues = [Cue(0, 100, "oral"), Cue(100, 200, "history")]

        self.assertEqual(find_cues(cues, "oral history"), [])

    def test_find_adds_context_once_in_source_order(self):
        cues = [
            Cue(0, 100, "before"),
            Cue(100, 200, "repeated match"),
            Cue(200, 300, "between"),
            Cue(300, 400, "repeated match"),
            Cue(400, 500, "after"),
        ]
        original = list(cues)

        self.assertEqual(find_cues(cues, "match", context=1), cues)
        self.assertEqual(cues, original)

    def test_find_keeps_equal_cues_at_different_positions(self):
        repeated = Cue(0, 100, "match")
        cues = [repeated, repeated]

        result = find_cues(cues, "match")

        self.assertEqual(result, cues)
        self.assertEqual(len(result), 2)

    def test_find_returns_empty_for_no_matches(self):
        self.assertEqual(find_cues([Cue(0, 100, "Hello")], "absent", context=2), [])

    def test_find_preserves_significant_phrase_whitespace(self):
        cues = [Cue(0, 100, "a phrase here"), Cue(100, 200, "phrase here")]

        self.assertEqual(find_cues(cues, " phrase"), [cues[0]])

    def test_find_rejects_invalid_phrase_even_with_no_cues(self):
        for phrase in ("", " \t\n", None):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                find_cues([], phrase)

    def test_find_rejects_invalid_context_even_with_no_cues(self):
        for context in (-1, 1.0, "1", True, False):
            with self.subTest(context=context), self.assertRaises(ValueError):
                find_cues([], "phrase", context=context)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parents[1]
        )
        self.path = Path(self.temp_directory.name) / "cues.tsv"
        self.path.write_text(
            "start_ms\tend_ms\ttext\n"
            "0\t1000\tOpening\n"
            "1000\t2000\tThe Main Story\n"
            "2000\t3000\tClosing\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_directory.cleanup()

    def run_main(self, *arguments):
        stdout = io.StringIO()
        stderr = io.StringIO()
        argv = ["transcript.py", str(self.path), *arguments]
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    main()
                except SystemExit as error:
                    status = error.code
                else:
                    status = 0
        return status, stdout.getvalue(), stderr.getvalue()

    def test_find_with_context_uses_existing_rendering(self):
        status, stdout, stderr = self.run_main("--find", "main", "--context", "1")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(
            stdout,
            "00:00:00.000 --> 00:00:01.000 Opening\n"
            "00:00:01.000 --> 00:00:02.000 The Main Story\n"
            "00:00:02.000 --> 00:00:03.000 Closing\n",
        )

    def test_find_with_no_matches_has_empty_stdout(self):
        status, stdout, stderr = self.run_main("--find", "absent")

        self.assertEqual((status, stdout, stderr), (0, "", ""))

    def test_full_transcript_command_is_unchanged(self):
        status, stdout, stderr = self.run_main()

        self.assertEqual(status, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Opening\n", stdout)
        self.assertIn("The Main Story\n", stdout)
        self.assertIn("Closing\n", stdout)

    def test_context_zero_without_find_is_allowed(self):
        status, stdout, stderr = self.run_main("--context", "0")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, "")
        self.assertIn("The Main Story", stdout)

    def test_invalid_search_arguments_are_clean_errors(self):
        cases = [
            (("--context", "1"), "--context requires --find"),
            (("--find", "story", "--context", "-1"), "nonnegative integer"),
            (("--find", "   "), "non-whitespace text"),
        ]
        for arguments, message in cases:
            with self.subTest(arguments=arguments):
                status, stdout, stderr = self.run_main(*arguments)
                self.assertNotEqual(status, 0)
                self.assertEqual(stdout, "")
                self.assertIn(message, stderr)
                self.assertNotIn("Traceback", stderr)


if __name__ == "__main__":
    unittest.main()
