import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from inventory import load_inventory, main, write_export

HEADER = "sku,name,quantity,reorder_at\n"


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "stock.csv"
        self.output = Path(self.temp.name) / "stock.json"

    def csv(self, body):
        self.source.write_text(HEADER + body, encoding="utf-8")
        return self.source

    def test_normalized_rows_and_order(self):
        rows = load_inventory(self.csv(' B2 ,"Brass, small",12,3\nA1,Álbum,0,0\n'))
        self.assertEqual(rows, [
            {"sku": "B2", "name": "Brass, small", "quantity": 12, "reorder_at": 3},
            {"sku": "A1", "name": "Álbum", "quantity": 0, "reorder_at": 0},
        ])

    def test_invalid_rows(self):
        for body in (
            "A1,Widget,-1,2\n", "A1,Widget,1,2.5\n", "A1,Widget,１,2\n",
            "A1,Widget,1,2\n A1 ,Again,9,2\n", ",Widget,4,2\n",
            "A1,,4,2\n", "A1,Widget,4\n", "A1,Widget,4,2,extra\n",
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                load_inventory(self.csv(body))

    def test_header_and_empty_inventory(self):
        self.source.write_text("name,sku,quantity,reorder_at\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "header"):
            load_inventory(self.source)
        self.assertEqual(load_inventory(self.csv("")), [])

    def test_cli_success_and_failure_preserve_export(self):
        self.csv("A1,Widget,4,2\n")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([str(self.source), str(self.output)]), 0)
            self.assertEqual(json.loads(self.output.read_text())[0]["quantity"], 4)
            original = self.output.read_bytes()
            self.csv("A1,Widget,4,2\nB2,Bad,-1,2\n")
            self.assertEqual(main([str(self.source), str(self.output)]), 2)
            self.assertEqual(self.output.read_bytes(), original)
            self.assertEqual(main([str(self.source), str(self.source)]), 2)

    def test_replace_failure_cleans_temporary_and_preserves_destination(self):
        self.output.write_text("previous\n", encoding="utf-8")
        with patch("inventory.os.replace", side_effect=OSError("read-only")):
            with self.assertRaises(OSError):
                write_export([], self.output)
        self.assertEqual(self.output.read_text(), "previous\n")
        self.assertEqual(list(Path(self.temp.name).iterdir()), [self.output])
