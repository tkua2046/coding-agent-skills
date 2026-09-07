# Stock export

Turn a shop's stock-count CSV into a validated JSON list for a local ordering
worksheet. Python 3.10+ is sufficient; the application has no dependencies.

```sh
mkdir -p artifacts
python3 inventory.py examples/stock.csv artifacts/stock.json
```

Use the [supplied CSV](examples/stock.csv) as a template: the header must be
`sku,name,quantity,reorder_at` in that order.
Quantities and reorder points are nonnegative integers. SKU and name are trimmed,
SKU matching is case-sensitive, and duplicate SKUs are errors. Input order is kept.
A header-only input exports an empty list. Fields such as `"Brass, small"` may be quoted.

The command prints the exported count and exits 0 on success. Invalid input or an
I/O error exits 2 and explains the problem on stderr. A bad later row leaves an
existing export untouched. The destination folder must already exist; source and
destination must differ. Output is UTF-8 JSON, with quantities stored as numbers.
This is a local file tool: it does not send orders or synchronize stock systems.

## Further reading

See [DEVNOTES](DEVNOTES.md) for contributor setup and checks, and the
[development history](docs/DEVELOPMENT_HISTORY.md) for implementation notes and
the historical session record.
