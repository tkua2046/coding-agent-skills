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

    def test_invalid_steps_preserve_state_and_allow_recovery(self):
        for step in (0, -1, -100, True, False, 1.0, 0.5, "2", None,
                     complex(1, 0), [], {}):
            with self.subTest(step=step):
                counter = Counter(-4)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, -4)
                self.assertEqual(counter.add(6), 2)
                self.assertEqual(counter.value, 2)

    def test_initial_values_and_repeated_additions(self):
        for initial, expected in ((-5, -2), (0, 3), (4, 7)):
            with self.subTest(initial=initial):
                counter = Counter(initial)
                self.assertEqual(counter.add(step=2), expected - 1)
                self.assertEqual(counter.add(), expected)
                self.assertEqual(counter.value, expected)

    def test_arbitrary_precision_integers(self):
        counter = Counter(-(10 ** 100))
        self.assertEqual(counter.add(10 ** 100 + 7), 7)
        self.assertEqual(counter.value, 7)

    def test_integer_subclass(self):
        class Step(int):
            pass

        counter = Counter()
        self.assertEqual(counter.add(Step(3)), 3)
        self.assertEqual(counter.value, 3)
