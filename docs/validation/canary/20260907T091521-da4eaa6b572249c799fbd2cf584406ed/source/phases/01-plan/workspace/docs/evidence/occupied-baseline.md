# Occupied-cell planning baseline — 2026-09-07

Scope: local fixture inspection and existing checks only; no implementation,
external services, dependency installation or commits. This is new evidence and
does not replace [historical S0 acceptance](../history/completed.md).

Read `AGENTS.md`, both requested skills and their drafting/planning prompts,
original/current/occupied requirements, accepted design, existing plan and history,
README, DEVNOTES, `navigator.py`, and `tests/test_navigator.py`.

Observed: `_target` computes the forward candidate; `run(pose, commands)` assigns
it without a collision check, turns locally, rejects unknown commands, and
returns an all-true outcome list for valid commands. There is no occupancy input.

Executed `"$CANARY_PYTHON" -m unittest discover -s tests -v` using the prepared
runtime. Exit status 0:

```text
test_left_wraps (test_navigator.NavigationTests.test_left_wraps) ... ok
test_turn_and_forward (test_navigator.NavigationTests.test_turn_and_forward) ... ok
test_unknown_command (test_navigator.NavigationTests.test_unknown_command) ... ok

Ran 3 tests in 0.000s

OK
```

Initial `git status --short` printed no changed-file entries; `git log -1` reported
`76a9632 Fixture baseline`. Both commands exited 0, with sandbox warnings about
unavailable xcrun cache/global ignore paths; no permissions were expanded.

Limits: these tests establish the existing baseline only. Occupancy examples are
hand-derived proposed acceptance checks, not results from implemented behavior.
Requested design and plan reviews remain pending.
