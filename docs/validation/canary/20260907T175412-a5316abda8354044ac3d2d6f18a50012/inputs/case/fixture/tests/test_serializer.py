import unittest
from serializer import serialize
class SerializerTests(unittest.TestCase):
    def test_spaces_are_data(self):
        self.assertEqual(serialize("  x  "), "  x  ")
