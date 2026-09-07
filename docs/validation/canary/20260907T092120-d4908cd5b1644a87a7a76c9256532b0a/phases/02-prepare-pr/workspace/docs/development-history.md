# Development history

Historical notes moved from README; these are not current verification results.
For current operations, see [DEVNOTES](../DEVNOTES.md).

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


At this checkpoint, coverage was optional via `python3 -m coverage run tools/check.py`,
then `python3 -m coverage report` and `python3 -m coverage json`. The everyday
check command had not yet incorporated coverage. Current instructions are in
[DEVNOTES](../DEVNOTES.md#checks-and-coverage).
