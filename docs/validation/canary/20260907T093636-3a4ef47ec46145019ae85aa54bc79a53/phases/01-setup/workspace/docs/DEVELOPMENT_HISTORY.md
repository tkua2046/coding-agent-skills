# Exporter development history

Historical implementation notes and session evidence moved from README.
The session below is not current verification; see [DEVNOTES](../DEVNOTES.md)
for maintained contributor commands.

## Maintainer checkpoint, 2 September

Development used `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
The custom discovery pattern predates tools/check.py. At this checkpoint,
coverage was an optional manual sequence (`python3 -m coverage run tools/check.py`,
then `python3 -m coverage report` and `python3 -m coverage json`); the everyday
gate had not incorporated measurement. Current check and hook policy lives in
[DEVNOTES](../DEVNOTES.md).

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
