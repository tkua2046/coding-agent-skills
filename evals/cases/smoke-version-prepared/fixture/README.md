# Inventory Report
Summarize warehouse stock adjustments by SKU. Repeated SKUs are summed and sorted; quantities must be nonnegative integers, and an invalid row rejects the whole input. The default CSV format remains compatible. The completed JSON option preserves string SKUs (including leading zeroes) and integer totals.

```sh
python3 inventory_report.py examples/stock.csv
python3 inventory_report.py examples/stock.csv --format json
```

The distributable is a Python zip application with the same arguments. It needs only Python's standard library. Contributor/release commands are in DEVNOTES.md.
