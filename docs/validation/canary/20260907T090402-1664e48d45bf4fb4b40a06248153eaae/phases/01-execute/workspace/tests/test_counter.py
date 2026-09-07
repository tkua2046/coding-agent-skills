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

    def test_invalid_steps_preserve_state_and_allow_later_add(self):
        invalid_steps = (0, -1, -100, True, False, 1.0, 0.5,
                         float("nan"), float("inf"), "3", None,
                         [], {}, object(), 1 + 0j)
        for initial in (0, -7, 4):
            for step in invalid_steps:
                with self.subTest(initial=initial, step=step):
                    counter = Counter(initial)
                    with self.assertRaises(ValueError):
                        counter.add(step)
                    self.assertEqual(counter.value, initial)
                    self.assertEqual(counter.add(), initial + 1)
                    self.assertEqual(counter.value, initial + 1)

    def test_positive_steps_from_zero_and_negative_values(self):
        for initial, step, expected in ((0, 3, 3), (-7, 2, -5),
                                        (-7, 7, 0), (-7, 10, 3)):
            with self.subTest(initial=initial, step=step):
                counter = Counter(initial)
                self.assertEqual(counter.add(step=step), expected)
                self.assertEqual(counter.value, expected)

    def test_repeated_adds(self):
        counter = Counter()
        self.assertEqual(counter.add(), 1)
        self.assertEqual(counter.add(4), 5)
        self.assertEqual(counter.add(), 6)
        self.assertEqual(counter.value, 6)

    def test_arbitrary_precision_integer(self):
        counter = Counter(-1)
        self.assertEqual(counter.add(10**100), 10**100 - 1)
        self.assertEqual(counter.value, 10**100 - 1)

    def test_integer_subclass(self):
        class Step(int):
            pass

        counter = Counter(4)
        self.assertEqual(counter.add(Step(3)), 7)
        self.assertEqual(counter.value, 7)
