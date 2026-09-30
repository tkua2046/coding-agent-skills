# Stock export

Validate a shop's stock-count CSV and export a JSON list for a local worksheet.
Python 3.10+ is sufficient; no dependencies or services are required.

```sh
mkdir -p artifacts
python3 inventory.py examples/stock.csv artifacts/stock.json
```

The CSV header is `sku,name,quantity,reorder_at`; quantities are nonnegative
integers, names are required and SKUs must be unique (case-sensitive after trim).
The exporter keeps input order and replaces the destination only after validation.
An invalid file exits 2 without replacing an existing export. The destination's
parent must exist. A header-only input produces `[]`.

The proposed ordering filter is described in [the request](docs/ORIGINAL.md),
[design](docs/DESIGN.md), and [plan](docs/PLAN.md). It is not implemented yet.
Contributors: [DEVNOTES](DEVNOTES.md).
