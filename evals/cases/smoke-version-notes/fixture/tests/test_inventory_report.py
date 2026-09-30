import unittest
from inventory_report import summarize


class InventoryReportTests(unittest.TestCase):
    def test_default_csv_and_opt_in_json(self):
        source = "sku,quantity\n001,2\nA-7,0\n001,3\n"
        self.assertEqual(summarize(source), "sku,quantity\n001,5\nA-7,0\n")
        self.assertEqual(summarize(source, "json"), '[{"sku":"001","quantity":5},{"sku":"A-7","quantity":0}]\n')

    def test_invalid_input(self):
        for source in ("sku,quantity\nA,2\nB,-1\n", "sku,quantity\nA,1.5\n", "sku,quantity\nA,2,extra\n", "wrong,quantity\nA,2\n"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                summarize(source)

    def test_header_only(self):
        self.assertEqual(summarize("sku,quantity\n"), "sku,quantity\n")
        self.assertEqual(summarize("sku,quantity\n", "json"), "[]\n")


if __name__ == "__main__":
    unittest.main()
