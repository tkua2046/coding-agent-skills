# Intake baseline evidence

Runtime: `/Users/tk/Documents/coding-agent-skills/.venv/bin/python`

Python: `3.12.4 (main, Jun  6 2024, 18:26:44) [Clang 15.0.0 (clang-1500.3.9.4)]`

Both checks ran with `PYTHONDONTWRITEBYTECODE=1`; no packages were installed.

## Documented test suite, using the prepared runtime

Command (argument vector): `['/Users/tk/Documents/coding-agent-skills/.venv/bin/python', '-m', 'unittest', 'discover', '-s', 'tests', '-v']`

Exit status: **1**

stdout:
```text

```

stderr:
```text
test_known_legacy_issue (test_formatter.FormatterTests.test_known_legacy_issue) ... FAIL
test_spaces (test_formatter.FormatterTests.test_spaces) ... ok

======================================================================
FAIL: test_known_legacy_issue (test_formatter.FormatterTests.test_known_legacy_issue)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-_g65_wgu/worker/tests/test_formatter.py", line 11, in test_known_legacy_issue
    self.assertEqual(label("ß"), "ß")
AssertionError: 'SS' != 'ß'
- SS
+ ß


----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1)

```

## Read-only current-behavior probe

Command (argument vector): `['/Users/tk/Documents/coding-agent-skills/.venv/bin/python', '-c', 'from formatter import label\nfor value in [" a ", "ß", " Straße ", "", "  ", "MiXeD"]:\n    print(f"label({value!r}) = {label(value)!r}")\nfor value in [None, 42]:\n    try:\n        print(f"label({value!r}) = {label(value)!r}")\n    except Exception as exc:\n        print(f"label({value!r}) raises {type(exc).__name__}: {exc}")\n']`

Exit status: **0**

stdout:
```text
label(' a ') = 'A'
label('ß') = 'SS'
label(' Straße ') = 'STRASSE'
label('') = ''
label('  ') = ''
label('MiXeD') = 'MIXED'
label(None) raises AttributeError: 'NoneType' object has no attribute 'strip'
label(42) raises AttributeError: 'int' object has no attribute 'strip'

```

stderr:
```text

```
