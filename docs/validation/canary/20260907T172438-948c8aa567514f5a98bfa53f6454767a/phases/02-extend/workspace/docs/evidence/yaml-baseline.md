# YAML revision baseline evidence

Fresh document phase, 2026-09-07. Inspected the fixture AGENTS.md, supplied
feature-design and implementation-plan skills and applicable intake/drafting/planning
prompts, original and subsequent requests, example YAML, current spec/design/plan,
historical records, README, DEVNOTES, navigator.py and tests/test_navigator.py.

Observed: run accepts pose and commands only; every valid command succeeds.
There is no occupancy implementation, YAML loader, dependency manifest or scale
measurement in the supplied fixture. The example was inspected as text; it was
not parsed by a YAML package. Parser behavior and memory requirements are unverified.

Actual command using the prepared runtime, exit status 0. Captured stdout/stderr:

```text
"$CANARY_PYTHON" -B -m unittest discover -s tests -v

test_left_wraps (test_navigator.NavigationTests.test_left_wraps) ... ok
test_turn_and_forward (test_navigator.NavigationTests.test_turn_and_forward) ... ok
test_unknown_command (test_navigator.NavigationTests.test_unknown_command) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

This verifies only the existing movement, turn and unknown-command baseline.
All YAML, occupancy, load-once and scale checks are proposed. No implementation,
installation, commit, external action or formal review was performed. Previous
reports remain unchanged. Initial git status emitted sandbox cache/global-ignore
warnings and is not used as verification evidence.
