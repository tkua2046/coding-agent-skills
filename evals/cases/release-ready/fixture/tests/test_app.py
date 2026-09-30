import unittest

from app import summary


class SummaryTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(summary([]), {"count": 0})

    def test_populated(self):
        self.assertEqual(summary(["a", "b"]), {"count": 2})
