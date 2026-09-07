# Occupied-cell planning evidence

Inspected in this document phase: AGENTS.md, both supplied skills and their drafting
prompts, original/confirmed requirements, current spec/design/plan, S0 history,
README, DEVNOTES, `navigator.py`, and `tests/test_navigator.py`.

Observed: `run` accepts only pose and commands. F always installs `_target(pose)`;
every valid command appends True. L/R update heading locally. Unknown commands
raise ValueError. There is no occupancy lookup or failure-path coverage.

Actual baseline check using the prepared runtime:

```text
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
test_left_wraps ... ok
test_turn_and_forward ... ok
test_unknown_command ... ok
Ran 3 tests in 0.000s
OK
```

These results establish only existing behavior; all occupied-cell checks in the
design/plan remain proposed. No packages were installed and no code was changed.
The git status invocation emitted sandbox warnings about cache/global-ignore
access, so it is not used as verification evidence.
