import unittest
from stock import adjust


class StockTests(unittest.TestCase):
    def test_direct_adjustment_preserves_input(self):
        original = {"A": 4, "B": 9}
        self.assertEqual(adjust(original, "A", 7), {"A": 7, "B": 9})
        self.assertEqual(original, {"A": 4, "B": 9})

    def test_rejects_invalid_quantity(self):
        for value in (-1, True, "7"):
            with self.assertRaises(ValueError):
                adjust({"A": 4}, "A", value)
