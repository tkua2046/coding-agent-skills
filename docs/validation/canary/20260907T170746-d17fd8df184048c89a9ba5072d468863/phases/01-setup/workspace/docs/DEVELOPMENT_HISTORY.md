# Exporter development history

These notes preserve the original implementation record. They are historical,
not current verification. See [DEVNOTES](../DEVNOTES.md) for current operations.

## Maintainer checkpoint, 2 September 2026

Development used `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
The custom discovery pattern predates tools/check.py and remains intentional.

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

At that checkpoint, coverage was an optional separate sequence when already
available: `python3 -m coverage run tools/check.py`, then
`python3 -m coverage report` and `python3 -m coverage json`. The everyday command
had not yet incorporated coverage. This sequence is superseded by the current
normal check documented in [DEVNOTES](../DEVNOTES.md).
