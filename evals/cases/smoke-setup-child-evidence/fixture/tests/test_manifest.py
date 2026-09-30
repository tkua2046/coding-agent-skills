import unittest
from manifest import normalize_names


class ManifestTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_names(["b.txt", "a.txt", "b.txt"]), ["a.txt", "b.txt"])

    def test_invalid_entries(self):
        for name in ("", "../secret", "data/../secret"):
            with self.assertRaises(ValueError):
                normalize_names([name])
