import unittest

from task_report import summarize


class SummaryTests(unittest.TestCase):
    def test_counts_only_open_tasks(self):
        self.assertEqual(summarize([{"status": "closed"}, {"status": "open"}]), "1 open tasks")

    def test_empty_list(self):
        self.assertEqual(summarize([]), "0 open tasks")
