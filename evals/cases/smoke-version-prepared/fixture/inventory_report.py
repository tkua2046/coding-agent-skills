"""Validate and summarize a warehouse inventory CSV, with opt-in JSON."""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import sys


def summarize(text, output_format="csv"):
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["sku", "quantity"]:
        raise ValueError("expected sku,quantity header")
    totals = {}
    for row in reader:
        sku, quantity = row.get("sku"), row.get("quantity")
        if None in row or not sku or quantity is None or not re.fullmatch(r"[0-9]+", quantity):
            raise ValueError("invalid inventory row")
        totals[sku] = totals.get(sku, 0) + int(quantity)
    rows = [{"sku": sku, "quantity": totals[sku]} for sku in sorted(totals)]
    if output_format == "json":
        return json.dumps(rows, separators=(",", ":")) + "\n"
    if output_format != "csv":
        raise ValueError("unsupported format")
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["sku", "quantity"])
    writer.writerows((row["sku"], row["quantity"]) for row in rows)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    args = parser.parse_args()
    try:
        result = summarize(args.input.read_text(), args.format)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
