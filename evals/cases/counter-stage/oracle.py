import os
import sys
import unittest

sys.path.insert(0, os.getcwd())
from counter import Counter


class CounterContract(unittest.TestCase):
    def test_valid_and_legacy(self):
        for initial in (-10, 0, 8):
            counter = Counter(initial)
            self.assertEqual(counter.add(), initial + 1)
            self.assertEqual(counter.add(7), initial + 8)
            self.assertEqual(counter.value, initial + 8)

    def test_reject_without_mutation(self):
        for step in (True, False, 0, -1, -100, 1.0, 2.5, "2", None, [], {}):
            with self.subTest(step=step):
                counter = Counter(11)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, 11)
                self.assertEqual(counter.add(2), 13)


unittest.main()
