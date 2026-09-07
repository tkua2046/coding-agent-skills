import unittest
from session import Session

class SessionTests(unittest.TestCase):
    def test_rejection_and_next(self):
        session = Session()
        with self.assertRaises(ValueError):
            session.apply("jump")
        self.assertEqual((session.cursor, session.selection), (4, "open"))
        session.apply("next")
        self.assertEqual((session.cursor, session.selection), (5, "closed"))
