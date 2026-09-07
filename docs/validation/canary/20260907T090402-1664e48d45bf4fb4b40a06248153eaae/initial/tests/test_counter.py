import unittest

from counter import Counter


class CounterTests(unittest.TestCase):
    def test_default(self):
        counter = Counter(4)
        self.assertEqual(counter.add(), 5)
        self.assertEqual(counter.value, 5)

    def test_positive_step(self):
        self.assertEqual(Counter(4).add(3), 7)

    def test_negative_preserves_value(self):
        counter = Counter(4)
        with self.assertRaises(ValueError):
            counter.add(-1)
        self.assertEqual(counter.value, 4)
