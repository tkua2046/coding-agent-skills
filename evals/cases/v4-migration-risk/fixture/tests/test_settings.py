import unittest

from settings import load


class SettingsTests(unittest.TestCase):
    def test_load(self):
        self.assertEqual(
            load("data/settings-v1.json"), {"theme": "dark", "timeout": 30}
        )

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            load("data/settings-v1-duplicate.json")
