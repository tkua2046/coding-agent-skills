import unittest

from counter import Counter


class CounterTests(unittest.TestCase):
    def test_default(self):
        counter = Counter(4)
        self.assertEqual(counter.add(), 5)
        self.assertEqual(counter.value, 5)

    def test_positive_step(self):
        counter = Counter(4)
        self.assertEqual(counter.add(3), 7)
        self.assertEqual(counter.value, 7)

    def test_negative_preserves_value(self):
        counter = Counter(4)
        with self.assertRaises(ValueError):
            counter.add(-1)
        self.assertEqual(counter.value, 4)

    def test_invalid_steps_preserve_value_and_allow_recovery(self):
        invalid_steps = (0, -3, True, False, 1.0, 0.5, "2", None,
                         [], {}, object(), complex(1, 0))
        for step in invalid_steps:
            with self.subTest(step=step):
                counter = Counter(-4)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, -4)
                self.assertEqual(counter.add(), -3)
                self.assertEqual(counter.value, -3)

    def test_initial_values_and_large_steps(self):
        for initial, step, expected in ((-5, 2, -3), (0, 1, 1),
                                        (5, 10**100, 10**100 + 5)):
            with self.subTest(initial=initial, step=step):
                counter = Counter(initial)
                self.assertEqual(counter.add(step=step), expected)
                self.assertEqual(counter.value, expected)

    def test_repeated_calls_and_default_initial_value(self):
        counter = Counter()
        self.assertEqual(counter.add(), 1)
        self.assertEqual(counter.add(step=4), 5)
        self.assertEqual(counter.add(), 6)
        self.assertEqual(counter.value, 6)

    def test_integer_subclass_step(self):
        class Step(int):
            pass

        counter = Counter(2)
        self.assertEqual(counter.add(Step(3)), 5)
        self.assertEqual(counter.value, 5)
