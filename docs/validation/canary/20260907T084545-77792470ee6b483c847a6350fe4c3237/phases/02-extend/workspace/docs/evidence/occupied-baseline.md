# Occupied-cell planning baseline — 2026-09-07

Fresh-context inspection for document work only. Read fixture AGENTS.md, both
requested skills and their drafting/planning resources, README, DEVNOTES,
original and confirmed requests, current spec/design/plan, historical S0 record,
`navigator.py` and `tests/test_navigator.py`.

Verified code: `run(pose, commands)` has no occupancy input. F always assigns
`_target(pose)`; every recognized command appends True. L/R change heading only;
unknown commands raise ValueError. State is local to each call.

Actual baseline check, using the prepared runtime without writing bytecode:

```sh
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v
```

Exit status 0. All three existing tests passed:
`test_left_wraps`, `test_turn_and_forward`, `test_unknown_command`.
This establishes the existing baseline only; occupied-cell behavior is unimplemented
and was not tested. Historical S0 acceptance is a separate preserved record.

Initial `git status --short` produced no change entries but emitted sandbox
warnings about xcrun cache creation and access to the global git ignore file.
It is not treated as a clean-status guarantee. No permissions were requested.

Proposed feature checks and future delivery acceptance live in
[DESIGN](../DESIGN.md#validation-and-remaining-questions) and [PLAN](../PLAN.md).
No code or test edits, package installation, commits or external actions were
performed for this planning baseline.
