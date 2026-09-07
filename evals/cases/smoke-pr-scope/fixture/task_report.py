import argparse
import json
from pathlib import Path


def summarize(tasks):
    return f"{sum(task['status'] == 'open' for task in tasks)} open tasks"


def main():
    parser = argparse.ArgumentParser(description="Report open tasks")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    tasks = json.loads(args.input.read_text(encoding="utf-8"))
    print(summarize(tasks))


if __name__ == "__main__":
    main()
