import json, tempfile, unittest
from pathlib import Path
from report import summarize
class ReportTests(unittest.TestCase):
    def test_subtotals(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"catalog.json"
            p.write_text(json.dumps([{"sku":"a","price_cents":125}]))
            self.assertEqual(summarize([{"sku":"a","quantity":3}],p),[{"sku":"a","subtotal_cents":375}])
    def test_empty(self):
        self.assertEqual(summarize([],"missing.json"),[])
