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
        for step in (0, -1, -100, True, False, 1.0, 0.5, float('nan'),
                     float('inf'), '2', None, [], {}, 1 + 0j, object()):
            with self.subTest(step=step):
                counter = Counter(-7)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, -7)
                self.assertEqual(counter.add(3), -4)
                self.assertEqual(counter.value, -4)

    def test_initial_integer_values_and_repeated_calls(self):
        for initial, expected in ((-10, -6), (0, 4), (10, 14)):
            with self.subTest(initial=initial):
                counter = Counter(initial)
                counter.add()
                self.assertEqual(counter.add(step=3), expected)
                self.assertEqual(counter.value, expected)

    def test_default_initial_value(self):
        counter = Counter()
        self.assertEqual(counter.add(), 1)
        self.assertEqual(counter.value, 1)

    def test_integer_subclass(self):
        class Step(int):
            pass

        counter = Counter(4)
        self.assertEqual(counter.add(Step(3)), 7)
        self.assertEqual(counter.value, 7)

    def test_arbitrary_precision_integers(self):
        counter = Counter(-(10 ** 100))
        self.assertEqual(counter.add(10 ** 100 + 9), 9)
        self.assertEqual(counter.value, 9)
