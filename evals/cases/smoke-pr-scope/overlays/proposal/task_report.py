import argparse
import csv
import json
import sys
from pathlib import Path


def summarize(tasks):
    return f"{sum(task['status'] == 'open' for task in tasks)} open tasks"


def write_csv(tasks, stream):
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["id", "title"])
    for task in tasks:
        if task["status"] == "open":
            writer.writerow([task["id"], task["title"]])


def main():
    parser = argparse.ArgumentParser(description="Report open tasks")
    parser.add_argument("input", type=Path)
    parser.add_argument("--csv", action="store_true", help="Export open task IDs and titles")
    args = parser.parse_args()
    tasks = json.loads(args.input.read_text(encoding="utf-8"))
    if args.csv:
        write_csv(tasks, sys.stdout)
    else:
        print(summarize(tasks))


if __name__ == "__main__":
    main()
