import os
import sys
import unittest

sys.path.insert(0, os.getcwd())
from navigator import run


class MaintenanceContract(unittest.TestCase):
    def test_runtime_still_continues(self):
        self.assertEqual(
            run((0, 0, 0), "FRF", {(0, 1)}), ((1, 0, 1), [False, True, True])
        )

    def test_west_negative_and_empty(self):
        self.assertEqual(run((-2, -3, 3), "F", {(-3, -3)}), ((-2, -3, 3), [False]))
        self.assertEqual(run((4, 5, 2), "", {(4, 4)}), ((4, 5, 2), []))


unittest.main()
