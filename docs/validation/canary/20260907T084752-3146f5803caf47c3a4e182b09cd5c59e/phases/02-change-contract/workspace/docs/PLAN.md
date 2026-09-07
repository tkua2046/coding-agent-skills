# Plan
Next: implement the confirmed stop-on-block contract in the navigator. This phase
revises planning only; neither pending stage below has been executed or verified.
Authority: [current contract](SPEC.md), [design and acceptance](DESIGN.md#acceptance),
and [confirmed request](STOP_REQUEST.md).

| Pending stage | Outcome and dependency | Acceptance and intended boundary |
| --- | --- | --- |
| Stop on blocked F | Amend navigator termination and affected tests; retain local state, occupied lookup, and pose invariants. Depends on the confirmed contract; account for the existing uncommitted maintenance candidate below without marking it accepted. | Cover first-command failure, a successful prefix retained before failure, omitted later commands, preserved west-facing pose, ordinary movement, and attempted unknown-command errors per design. One coherent implementation/test change, with usage documentation as needed; proposed commit only in a later authorized phase. |
| Text adapter outcomes | Expose returned pose and attempted outcomes. Depends on the implemented stop contract; adapter is not currently present. | FRF from (0,0,0) with (0,1) occupied displays unchanged pose and one failure only. Also verify earlier successes are displayed when blocking occurs later. Include proposed adapter integration coverage and usage documentation in one coherent later implementation boundary. |

For each future implementation boundary, implement and test, run the navigator
suite via `"$CANARY_PYTHON" -m unittest discover -s tests -v` and `git diff --check`,
then independent and human review of the candidate, fixes and affected rechecks.
The adapter stage adds the proposed integration test to discovery. These are
planned checks; no new test results or review acceptance are claimed here.
Follow [repository guidance](../AGENTS.md) and [development checks](../DEVNOTES.md).
Completion requires relevant acceptance checks and both reviews; preserve actual
results and reviewed candidate identities in stage/review records. No commits or
external actions are authorized in this planning phase.

## Completed stages (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
The former pending adapter acceptance (FRF displays failure then two successes)
is superseded by the stop request and the pending stages above. Completed D2 and
its review remain evidence of the earlier continuation contract only.

The maintenance report below is preserved as recorded for its original candidate.
Its next-action statement and successful checks predate this amendment and do not
establish acceptance of the stop contract or replace the current next stage.

## Bounded maintenance candidate (2026-09-07)

Implemented private helper rename and negative-coordinate westward blocked-move
regression; public behavior unchanged. Uncommitted; adapter stage remains pending.
Next action: independent and human review of this maintenance candidate; neither
review is complete and acceptance is pending. No open finding IDs. Independent
review could not start because the agent tool returned "no thread with id".

Candidate: base `59babeb8059a172db294c1a368f6332108904cf2` plus working-tree
changes to `navigator.py` and `tests/test_navigator.py`, identified by SHA256:

- `navigator.py`: `9fe50251aa7069ebe61b8616a2bbce146cc4a29f7ea413405161b75f22396899`
- `tests/test_navigator.py`: `b0ba1b8b9a1b3ed3b16625c16e7df6e3e3d716ab97abef59f163045cb02f05a2`

Checks: `"$CANARY_PYTHON" -m unittest discover -s tests -v` passed all 4 baseline
tests and all 5 candidate tests. `git diff --check` passed (exit 0); Git emitted
sandbox cache warnings. No additional lint/format gate is configured in the fixture.
Prior reports: [S0](history/completed.md), [D2](history/d2-review.md).
