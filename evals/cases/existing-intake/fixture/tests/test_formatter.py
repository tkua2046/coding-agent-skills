import unittest

from formatter import label


class FormatterTests(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(label(" a "), "A")

    def test_known_legacy_issue(self):
        self.assertEqual(label("ß"), "ß")
