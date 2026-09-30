import unittest

from adjustments import net_change


class AdjustmentsTests(unittest.TestCase):
    def test_positive_adjustments(self):
        self.assertEqual(net_change([2, 3]), 5)

    def test_negative_adjustment_reduces_total(self):
        self.assertEqual(net_change([4, -1]), 3)
