# Check runner repair evidence

Used the setup operation in `skills/dev-workflow`. Changed only
`tools/check.py`: retain unittest discovery and the existing command path,
capture the runner result, and return 0 only when `testsRun > 0` and
`wasSuccessful()` is true; otherwise return 1.

## Actual before/after results

All runs used the prepared runtime through
`"$CANARY_PYTHON" -B tools/check.py`, from the applicable fixture root.
Exit statuses below are the check subprocess statuses, not a surrounding
command's status. Baseline runs were performed before editing the runner.

| Suite | Observed output before and after | Before exit | After exit |
| --- | --- | --- | --- |
| Existing application tests | `Ran 2 tests`; `FAILED (failures=1)` | 0 | 1 |
| Isolated passing test | `Ran 1 test`; `OK` | 0 | 0 |
| Isolated failing test | `Ran 1 test`; `FAILED (failures=1)` | 0 | 1 |
| Empty tests directory | `Ran 0 tests`; `NO TESTS RAN` | 0 | 1 |

The existing suite reported these same outcomes before and after:

```text
test_negative_adjustment_reduces_total ... FAIL
test_positive_adjustments ... ok
AssertionError: 4 != 3
Ran 2 tests in 0.000s
FAILED (failures=1)
```

For each isolated scenario, a temporary directory inside this workspace held
an exact copy of the runner at `tools/check.py` and a `tests` directory.
The passing/failing cases each supplied `test_probe.py` with one
`unittest.TestCase` method, asserting `2 + 3 == 5` or `4 == 3`, respectively.
The empty case supplied no test file. Each invoked the same command path
via `subprocess.run`, capturing output and return code. The after-run harness
asserted return codes 0, 1, and 1 and itself exited 0. Temporary fixtures
were removed automatically; no tooling or permanent tests were added.

## Scope and remaining work

The runner repair is complete. The normal application check remains red
because the known negative-adjustment defect is outside this task. Repairing
that application behavior is separate remaining work; the failing assertion
now propagates to the command's exit status.

Application code, tests, existing documentation, and supplied skills were
preserved. No prior reports were present. This report owns the repair evidence;
README and DEVNOTES retain their existing roles and contents. No packages,
tooling, hooks, coverage policy, commits, or publishing were added or performed.
The fixture has no hook or coverage configuration; neither was verified.
