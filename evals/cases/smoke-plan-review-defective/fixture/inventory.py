"""Validate a stock-count CSV and replace its JSON export only after success."""
import argparse
import csv
import json
import os
from pathlib import Path
import sys
import tempfile

FIELDS = ["sku", "name", "quantity", "reorder_at"]


def nonnegative(value, field, line):
    text = (value or "").strip()
    if not text.isascii() or not text.isdecimal():
        raise ValueError(f"line {line}: {field} must be a nonnegative integer")
    return int(text)


def load_inventory(path):
    """Return validated rows in input order; reject duplicates across the file."""
    rows, seen = [], set()
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("header must be sku,name,quantity,reorder_at")
        for line, raw in enumerate(reader, 2):
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError(f"line {line}: expected four columns")
            sku, name = raw["sku"].strip(), raw["name"].strip()
            if not sku or not name:
                raise ValueError(f"line {line}: sku and name are required")
            if sku in seen:
                raise ValueError(f"line {line}: duplicate sku {sku}")
            seen.add(sku)
            rows.append({
                "sku": sku,
                "name": name,
                "quantity": nonnegative(raw["quantity"], "quantity", line),
                "reorder_at": nonnegative(raw["reorder_at"], "reorder_at", line),
            })
    return rows


def write_export(rows, destination):
    """Write beside the destination and replace it after serialization succeeds."""
    destination = Path(destination)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(rows, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.source.resolve() == args.destination.resolve():
            raise ValueError("source and destination must differ")
        rows = load_inventory(args.source)
        write_export(rows, args.destination)
    except (OSError, ValueError) as error:
        print(f"inventory: {error}", file=sys.stderr)
        return 2
    print(f"Exported {len(rows)} items to {args.destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
