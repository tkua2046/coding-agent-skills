# Check runner repair

Completed the setup operation in `skills/dev-workflow`. Only `tools/check.py` was repaired; unittest discovery, output, and the documented command path are retained. The runner now exits 0 only when at least one test ran and `result.wasSuccessful()` is true, otherwise 1.

## Actual before/after results

Every check subprocess used `"$CANARY_PYTHON" -B tools/check.py` from its fixture root. CANARY_PYTHON resolved to `/Users/tk/Documents/coding-agent-skills/.venv/bin/python`. Exit statuses below are the check subprocess statuses, not the evidence driver's status.

| Case | Test outcome before and after | Before exit | After exit |
| --- | --- | --- | --- |
| Existing application suite | 2 tests, 1 failure: 4 != 3 | 0 | 1 |
| Isolated passing suite | 1 test, OK | 0 | 0 |
| Isolated failing suite | 1 test, failure: 4 != 5 | 0 | 1 |
| Isolated empty suite | 0 tests, NO TESTS RAN | 0 | 1 |

The baseline was executed before the edit; the same evidence driver was executed after the edit. Controlled cases copied only the current runner into temporary directories inside this workspace, created synthetic unittest inputs, and removed those directories afterward. Existing application tests were never changed. No external fixture, package, service, or installed tooling was used.

## Before transcript

```text
=== existing fixture: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_negative_adjustment_reduces_total (test_adjustments.AdjustmentsTests.test_negative_adjustment_reduces_total) ... FAIL
test_positive_adjustments (test_adjustments.AdjustmentsTests.test_positive_adjustments) ... ok

======================================================================
FAIL: test_negative_adjustment_reduces_total (test_adjustments.AdjustmentsTests.test_negative_adjustment_reduces_total)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-h70f3g64/worker/tests/test_adjustments.py", line 11, in test_negative_adjustment_reduces_total
    self.assertEqual(net_change([4, -1]), 3)
AssertionError: 4 != 3

----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1)
EXIT_STATUS=0
=== passing: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_gate (test_gate.GateTest.test_gate) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
EXIT_STATUS=0
=== failing: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_gate (test_gate.GateTest.test_gate) ... FAIL

======================================================================
FAIL: test_gate (test_gate.GateTest.test_gate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-h70f3g64/worker/.check-evidence-3qq8a7zp/failing/tests/test_gate.py", line 4, in test_gate
    self.assertEqual(2 + 2, 5)
AssertionError: 4 != 5

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
EXIT_STATUS=0
=== empty: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===

----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
EXIT_STATUS=0
```

## After transcript

```text
=== existing fixture: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_negative_adjustment_reduces_total (test_adjustments.AdjustmentsTests.test_negative_adjustment_reduces_total) ... FAIL
test_positive_adjustments (test_adjustments.AdjustmentsTests.test_positive_adjustments) ... ok

======================================================================
FAIL: test_negative_adjustment_reduces_total (test_adjustments.AdjustmentsTests.test_negative_adjustment_reduces_total)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-h70f3g64/worker/tests/test_adjustments.py", line 11, in test_negative_adjustment_reduces_total
    self.assertEqual(net_change([4, -1]), 3)
AssertionError: 4 != 3

----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1)
EXIT_STATUS=1
=== passing: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_gate (test_gate.GateTest.test_gate) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
EXIT_STATUS=0
=== failing: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===
test_gate (test_gate.GateTest.test_gate) ... FAIL

======================================================================
FAIL: test_gate (test_gate.GateTest.test_gate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-h70f3g64/worker/.check-evidence-c1buj3bp/failing/tests/test_gate.py", line 4, in test_gate
    self.assertEqual(2 + 2, 5)
AssertionError: 4 != 5

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
EXIT_STATUS=1
=== empty: /Users/tk/Documents/coding-agent-skills/.venv/bin/python -B tools/check.py ===

----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
EXIT_STATUS=1
```

## Reproduction driver

This exact shell command produced each transcript (once before and once after repair):

```sh
"$CANARY_PYTHON" -B - <<'PY'
import pathlib
import shutil
import subprocess
import sys
import tempfile

root = pathlib.Path.cwd()
cases = {
    "passing": "import unittest\nclass GateTest(unittest.TestCase):\n    def test_gate(self):\n        self.assertEqual(2 + 2, 4)\n",
    "failing": "import unittest\nclass GateTest(unittest.TestCase):\n    def test_gate(self):\n        self.assertEqual(2 + 2, 5)\n",
    "empty": None,
}
def run(label, cwd):
    result = subprocess.run([sys.executable, "-B", "tools/check.py"], cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f"=== {label}: {sys.executable} -B tools/check.py ===")
    print(result.stdout, end="")
    print(f"EXIT_STATUS={result.returncode}")
run("existing fixture", root)
with tempfile.TemporaryDirectory(prefix=".check-evidence-", dir=root) as temp:
    for name, source in cases.items():
        cwd = pathlib.Path(temp) / name
        (cwd / "tools").mkdir(parents=True)
        (cwd / "tests").mkdir()
        shutil.copyfile(root / "tools/check.py", cwd / "tools/check.py")
        if source is not None:
            (cwd / "tests" / "test_gate.py").write_text(source)
        run(name, cwd)
PY
```

## Scope and remaining work

The known application defect described in DEVNOTES remains: negative adjustments are ignored, and the normal application check correctly fails. Fixing that application behavior is a separate task; no remaining runner work was identified for the requested cases.

README.md remains the user guide, DEVNOTES.md remains the contributor check reference, and AGENTS.md remains the agent scope reference. Those files, application code, and existing tests were preserved. No prior report was present or overwritten. RESULT.md owns this execution evidence.

No tooling was added, packages installed, hooks configured or executed, coverage configured or measured, or coverage threshold introduced. No commit, publication, or external service action was performed.

