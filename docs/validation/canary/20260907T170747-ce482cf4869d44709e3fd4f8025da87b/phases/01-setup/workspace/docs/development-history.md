# Exporter development history

Historical implementation notes and the original session record, moved from
README. These are not current verification results. For current operations, see
[DEVNOTES](../DEVNOTES.md).

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

## Earlier coverage workflow (superseded)

At the 2 September checkpoint, the everyday check did not include coverage.
The optional command was `python3 -m coverage run tools/check.py`, followed by
`python3 -m coverage report` and `python3 -m coverage json` when coverage was
already available. The normal command now integrates coverage; use the current
[contributor instructions](../DEVNOTES.md#checks-and-coverage).
