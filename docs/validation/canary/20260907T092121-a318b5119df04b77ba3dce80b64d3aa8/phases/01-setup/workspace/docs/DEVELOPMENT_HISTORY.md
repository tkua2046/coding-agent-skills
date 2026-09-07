# Exporter development history

Historical material moved from README; not current verification.
See [DEVNOTES](../DEVNOTES.md) for maintained contributor operations.

## Implementation notes

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


## Tooling at the September 2 checkpoint

Development also used `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
Coverage was optional via `python3 -m coverage run tools/check.py`, followed by
`python3 -m coverage report` and `python3 -m coverage json` when available.
The everyday check had not yet incorporated coverage.
