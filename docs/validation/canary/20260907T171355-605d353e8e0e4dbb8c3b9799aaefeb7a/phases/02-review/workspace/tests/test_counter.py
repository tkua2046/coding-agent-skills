import unittest

from counter import Counter


class CounterTests(unittest.TestCase):
    def test_default(self):
        counter = Counter(4)
        self.assertEqual(counter.add(), 5)
        self.assertEqual(counter.value, 5)

    def test_positive_step(self):
        cases = [(4, 3, 7), (-8, 3, -5), (0, 1, 1),
                 (2**100, 2**100, 2**101)]
        for initial, step, expected in cases:
            with self.subTest(initial=initial, step=step):
                counter = Counter(initial)
                self.assertEqual(counter.add(step=step), expected)
                self.assertEqual(counter.value, expected)

    def test_integer_subclass(self):
        class Step(int):
            pass

        self.assertEqual(Counter().add(Step(3)), 3)

    def test_invalid_steps_preserve_value_and_allow_recovery(self):
        for step in [0, -2, True, False, 1.0, 0.5, float("nan"),
                     float("inf"), "2", None, [], {}, 1 + 0j, object()]:
            with self.subTest(step=step):
                counter = Counter(-4)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, -4)
                self.assertEqual(counter.add(2), -2)

    def test_negative_preserves_value(self):
        counter = Counter(4)
        with self.assertRaises(ValueError):
            counter.add(-1)
        self.assertEqual(counter.value, 4)
