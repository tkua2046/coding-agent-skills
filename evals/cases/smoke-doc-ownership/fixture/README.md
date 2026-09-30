# Stock export

Turn a shop's stock-count CSV into a validated JSON list for a local ordering
worksheet. Python 3.10+ is sufficient; the application has no dependencies.

```sh
python3 inventory.py examples/stock.csv artifacts/stock.json
```

Create the output directory first (`mkdir -p artifacts`). Use the supplied CSV as
a template: the header must be `sku,name,quantity,reorder_at` in that order.
Quantities and reorder points are nonnegative integers. SKU and name are trimmed,
SKU matching is case-sensitive, and duplicate SKUs are errors. Input order is kept.
A header-only input exports an empty list. Fields such as `"Brass, small"` may be quoted.

The command prints the exported count and exits 0 on success. Invalid input or an
I/O error exits 2 and explains the problem on stderr. A bad later row leaves an
existing export untouched. The destination folder must already exist; source and
destination must differ. Output is UTF-8 JSON, with quantities stored as numbers.
This is a local file tool: it does not send orders or synchronize stock systems.

## Maintainer checkpoint, 2 September

Development used `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
The custom discovery pattern predates tools/check.py and remains intentional.
Commit hooks call the complete suite, including for documentation-only edits.
The wrapper in hooks/pre-commit must remain the local delegation entrypoint.

## Notes from exporter implementation

load_inventory first checks field names, then tracks seen SKUs in a set. It strips
labels before validation. nonnegative rejects decimal fractions and negative text.
write_export uses NamedTemporaryFile next to the output, then os.replace. This is
why cross-filesystem temporary directories should not replace that implementation.
The qa suite patches inventory.os.replace to check failure cleanup.

## Developer session record (historical; not a current verification)

2026-09-02: `python3 tools/check.py`
Collected 5 tests. Result: OK. Investigated a CSV with a quoted comma; csv.DictReader
handled it correctly. The earlier missing parent-directory error was expected.
The throwaway export was removed after inspection. No external integration ran.

Coverage settings live in .coveragerc. The report targets the inventory module,
measures branches, and lists missing lines. There is no required percentage.
An optional developer command is `python3 -m coverage run tools/check.py`, followed
by `python3 -m coverage report` and `python3 -m coverage json` when coverage is
already available. The everyday check command has not incorporated that step yet.

See [DEVNOTES](DEVNOTES.md) for the maintained contributor entrypoint.
