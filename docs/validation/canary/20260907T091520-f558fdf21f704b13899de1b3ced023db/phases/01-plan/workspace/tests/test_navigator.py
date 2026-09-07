import unittest

from navigator import run


class NavigationTests(unittest.TestCase):
    def test_turn_and_forward(self):
        self.assertEqual(run((0, 0, 0), "RF"), ((1, 0, 1), [True, True]))

    def test_left_wraps(self):
        self.assertEqual(run((2, 3, 0), "L"), ((2, 3, 3), [True]))

    def test_unknown_command(self):
        with self.assertRaises(ValueError):
            run((0, 0, 0), "?")
