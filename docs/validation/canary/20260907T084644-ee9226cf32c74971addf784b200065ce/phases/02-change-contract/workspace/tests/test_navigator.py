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

    def test_block_preserves_pose_and_continues(self):
        self.assertEqual(
            run((0, 0, 0), "FRF", {(0, 1)}),
            ((1, 0, 1), [False, True, True]),
        )

    def test_blocked_forward_facing_west_at_negative_coordinate(self):
        self.assertEqual(
            run((-2, -3, 3), "F", {(-3, -3)}),
            ((-2, -3, 3), [False]),
        )
