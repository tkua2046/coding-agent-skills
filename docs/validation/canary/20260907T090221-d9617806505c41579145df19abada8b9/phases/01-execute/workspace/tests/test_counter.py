import unittest

from counter import Counter


class CounterTests(unittest.TestCase):
    def test_default(self):
        counter = Counter(4)
        self.assertEqual(counter.add(), 5)
        self.assertEqual(counter.value, 5)

    def test_positive_step(self):
        counter = Counter(4)
        self.assertEqual(counter.add(step=3), 7)
        self.assertEqual(counter.value, 7)

    def test_negative_preserves_value(self):
        counter = Counter(4)
        with self.assertRaises(ValueError):
            counter.add(-1)
        self.assertEqual(counter.value, 4)

    def test_invalid_steps_preserve_state_and_allow_recovery(self):
        for step in (0, -100, True, False, 1.0, 0.5, "2", None, [], {}, object()):
            with self.subTest(step=step):
                counter = Counter(-4)
                with self.assertRaises(ValueError):
                    counter.add(step)
                self.assertEqual(counter.value, -4)
                self.assertEqual(counter.add(), -3)
                self.assertEqual(counter.value, -3)

    def test_initial_values_and_repeated_additions(self):
        for initial in (-10, 0, 10):
            with self.subTest(initial=initial):
                counter = Counter(initial)
                self.assertEqual(counter.add(1), initial + 1)
                self.assertEqual(counter.add(3), initial + 4)
                self.assertEqual(counter.value, initial + 4)

    def test_unbounded_integer_step(self):
        counter = Counter()
        step = 10 ** 100
        self.assertEqual(counter.add(step), step)
        self.assertEqual(counter.value, step)

    def test_integer_subclass_step(self):
        class Step(int):
            pass

        counter = Counter()
        self.assertEqual(counter.add(Step(2)), 2)
        self.assertEqual(counter.value, 2)
