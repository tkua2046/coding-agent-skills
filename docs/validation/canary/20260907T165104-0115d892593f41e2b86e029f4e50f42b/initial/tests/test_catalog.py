import unittest
from catalog import total_quantities
class CatalogTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total_quantities([{"quantity": 0}, {"quantity": 7}]), 7)
