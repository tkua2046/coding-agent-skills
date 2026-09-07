# Development history

Historical notes moved from README; these are not current verification.

## Maintainer checkpoint, 2 September 2026

Development used `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
The custom discovery pattern predates tools/check.py and remains intentional.
At that checkpoint, coverage was a separate optional sequence:
`python3 -m coverage run tools/check.py`, `python3 -m coverage report`,
and `python3 -m coverage json`.
Current operations are maintained in [DEVNOTES](../DEVNOTES.md).

## Developer session record

2026-09-02: `python3 tools/check.py`
Collected 5 tests. Result: OK. Investigated a CSV with a quoted comma; csv.DictReader
handled it correctly. The earlier missing parent-directory error was expected.
The throwaway export was removed after inspection. No external integration ran.


See also [implementation notes](DESIGN.md).
