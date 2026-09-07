import csv
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

from task_report import summarize, write_csv

ROOT = Path(__file__).resolve().parents[1]


class SummaryTests(unittest.TestCase):
    def test_counts_only_open_tasks(self):
        self.assertEqual(summarize([{"status": "closed"}, {"status": "open"}]), "1 open tasks")

    def test_empty_list(self):
        self.assertEqual(summarize([]), "0 open tasks")


class ExportTests(unittest.TestCase):
    def test_filters_and_preserves_order_and_cell_content(self):
        tasks = [
            {"id": "B", "title": 'Café, "north"\nstock', "status": "open"},
            {"id": "X", "title": "Closed task", "status": "closed"},
            {"id": "A", "title": "Second task", "status": "open"},
        ]
        stream = io.StringIO()
        write_csv(tasks, stream)
        self.assertEqual(list(csv.reader(io.StringIO(stream.getvalue()))), [
            ["id", "title"], ["B", 'Café, "north"\nstock'], ["A", "Second task"]
        ])

    def test_empty_export_has_header(self):
        for tasks in ([], [{"id": "X", "title": "Done", "status": "closed"}]):
            with self.subTest(tasks=tasks):
                stream = io.StringIO()
                write_csv(tasks, stream)
                self.assertEqual(stream.getvalue(), "id,title\n")

    def test_cli_and_shipped_example_match_source_data(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "task_report.py"), str(ROOT / "examples/tasks.json"), "--csv"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(result.stderr, "")
        sample = (ROOT / "examples/open-tasks.csv").read_text(encoding="utf-8")
        self.assertEqual(result.stdout, sample)
        tasks = json.loads((ROOT / "examples/tasks.json").read_text(encoding="utf-8"))
        self.assertEqual(list(csv.reader(io.StringIO(sample))), [
            ["id", "title"], [tasks[0]["id"], tasks[0]["title"]],
            [tasks[2]["id"], tasks[2]["title"]], [tasks[3]["id"], tasks[3]["title"]],
        ])

    def test_cli_preserves_summary_without_flag(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "task_report.py"), str(ROOT / "examples/tasks.json")],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout, "3 open tasks\n")
        self.assertEqual(result.stderr, "")
