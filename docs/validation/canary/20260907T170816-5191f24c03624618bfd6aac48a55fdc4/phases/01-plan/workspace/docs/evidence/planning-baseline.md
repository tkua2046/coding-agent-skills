# Planning baseline — 2026-09-07

Inspected `inventory.py`, `batch.py`, `command_codec.py`, `tests/test_inventory.py`,
`hooks/pre-commit`, repository instructions and existing documentation. No production
code or tests changed during this planning phase.

Executed from the fixture root using the prepared runtime:

| Command | Exit | Raw stdout/stderr |
| --- | --- | --- |
| `"$CANARY_PYTHON" -m unittest discover -s tests -v` | 0 | [tests](planning-baseline-tests.txt) |
| `"$CANARY_PYTHON" hooks/pre-commit` | 0 | [gate](planning-baseline-gate.txt) |
| `"$CANARY_PYTHON" -` with the probe below | 0 | [probe](planning-shortage-probe.txt) |

Both baseline checks ran six tests successfully. The probe is diagnostic, not a
passing feature test: it observed `{"a":-3,"b":-2}` and four accepted outcomes.
Required behavior is zero stock and `[False, True, False, True]`. This establishes
the current shortage defect; it does not verify the proposed implementation.

Probe (print-only, no source changes):

```python
from inventory import reserve
stock = {'a': 3, 'b': 1}
orders = [
    {'id': 'reject', 'items': [['a', 2], ['b', 2]]},
    {'id': 'take', 'items': [['a', 3], ['b', 1]]},
    {'id': 'later', 'items': [['a', 1]]},
    {'id': 'empty', 'items': []},
]
print('Input:', repr((stock, orders)))
print('Observed:', repr(reserve(stock, orders)))
print('Required:', repr(({'a': 0, 'b': 0}, [
    {'order_id': 'reject', 'accepted': False},
    {'order_id': 'take', 'accepted': True},
    {'order_id': 'later', 'accepted': False},
    {'order_id': 'empty', 'accepted': True},
])))
```

`git status --short` exited 0 with no changes before documentation edits, but emitted
sandbox warnings about the external xcrun cache and global ignore file. No access
outside the fixture was needed to inspect implementation or run the checks.
