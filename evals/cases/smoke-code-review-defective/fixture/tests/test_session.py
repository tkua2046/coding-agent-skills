import unittest
from session import Session

class SessionTests(unittest.TestCase):
    def test_next(self):
        state = Session()
        state.apply("next")
        self.assertEqual((state.cursor, state.selection), (5, "closed"))

    def test_reject_preserves_cursor(self):
        state = Session()
        with self.assertRaises(ValueError):
            state.apply("bogus")
        self.assertEqual(state.cursor, 4)
