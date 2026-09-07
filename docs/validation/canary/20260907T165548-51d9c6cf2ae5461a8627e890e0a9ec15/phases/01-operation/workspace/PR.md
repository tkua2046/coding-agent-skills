# Draft: Preserve surrounding spaces in exported text

Snapshot: local fixture at `10f1835a6bc143acfe1bf81c706582e2ada922a6` (Fixture baseline), validated on 2026-09-07. No staged or unstaged tracked changes were reported before preparing this draft.

## Behavior and scope

[CHANGE.md](CHANGE.md) changes the required behavior from normalized strings to preserving surrounding spaces because spaces are user data. The current regression test expects `serialize("  x  ")` to return `"  x  "`.

The implementation still uses `str(value).strip()` and actually returns `"x"`. Space preservation is therefore an intended behavior change, not a completed product change. This preparation adds only a local PR draft; product code, tests, source requirements and prior reports remain unchanged.

## Validation

Ran the mandatory gate from [DEVNOTES.md](DEVNOTES.md), `python -m unittest discover -s tests -v`, using the supplied prepared runtime:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
```

Result: exit code 1; one test ran and failed:

```text
FAIL: test_spaces_are_data (test_serializer.SerializerTests.test_spaces_are_data)
AssertionError: 'x' != '  x  '
Ran 1 test in 0.000s
FAILED (failures=1)
```

The passing result in [previous-report.md](previous-report.md) belongs to the previous candidate's normalization contract and test configuration. It is preserved as historical evidence and does not establish readiness for this candidate. No remote CI validation was performed.

## Remaining blockers

The implementation does not satisfy the current space-preservation requirement, and the mandatory gate is failing. Product implementation must be reconciled with that requirement and the current gate rerun before this change is ready. Product fixes are outside this preparation's authorized scope.

No commit, push, PR publication, release or version bump was performed.
