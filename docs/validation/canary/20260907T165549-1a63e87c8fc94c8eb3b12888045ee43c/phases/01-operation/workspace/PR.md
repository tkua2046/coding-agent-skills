# Draft: Require surrounding spaces to survive text export

Status: blocked; the current candidate does not satisfy the new contract.

[CHANGE.md](CHANGE.md) requires exported text to preserve surrounding spaces because they are user data. The current regression test expects `serialize("  x  ")` to return `"  x  "`. The implementation still calls `str(value).strip()` and returns `"x"`, removing those spaces. The candidate captures the new requirement in a test; the requested runtime behavior is not yet implemented.

Validation of the supplied working tree at baseline `8ffc7fc`:

- Ran the current gate documented in [DEVNOTES.md](DEVNOTES.md), using the prepared runtime: `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`.
- Result: exit code 1; 1 test run, 1 failure.
- `test_serializer.SerializerTests.test_spaces_are_data` failed at `tests/test_serializer.py:5`: `AssertionError: 'x' != '  x  '`.
- [previous-report.md](previous-report.md) describes a passing previous candidate under the old normalization contract and test configuration. It is historical evidence, not validation of this candidate.

Remaining blocker: reconcile the implementation with space preservation, then rerun the documented gate successfully before claiming PR readiness. Product fixes are outside this preparation task.

Only this local draft was added. Product code, tests, requirements, and prior reports were preserved. No commit, version bump, or PR publication was performed. The changelog's existing in-progress status remains accurate.
