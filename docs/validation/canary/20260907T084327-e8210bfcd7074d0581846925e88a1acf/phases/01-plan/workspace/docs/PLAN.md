# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Occupied-cell follow-up

Status: planned only. Next action: perform the requested design amendment review
and plan review; both are pending. Implementation belongs to a later task.
Scope: [confirmed request](OCCUPIED_REQUEST.md),
[specification addendum](OCCUPIED_SPEC.md), and
[D1-O1 design amendment](DESIGN.md#occupied-cell-amendment-d1-o1).
S0 remains complete; [its historical acceptance](history/completed.md) is not
acceptance of this feature.

| Stage | Observable outcome / scope | Dependencies and boundary | Acceptance / risk | State |
|---|---|---|---|---|
| S1 | Caller-supplied fixed occupancy blocks forward moves, preserving pose and continuing commands. Extend `navigator.py`, cover behavior in `tests/test_navigator.py`, update README usage and current SPEC behavior. | D1-O1/interface convention review and plan review, then later implementation task. One coherent implementation/test/documentation commit is sufficient for this local behavior. | All [acceptance cases](OCCUPIED_SPEC.md#acceptance-examples), existing compatibility checks, and the complete local unittest gate. Main risks: reporting success for a block, ending command processing, mutating pose before checking, or leaking occupancy across runs. | Planned; no implementation or feature checks performed. |

The complete repository check gate is documented in [DEVNOTES](../DEVNOTES.md):
`python3 -m unittest discover -s tests -v`. In this fixture use the equivalent
`"$CANARY_PYTHON" -m unittest discover -s tests -v`; no dependency installation is
needed. The [baseline run](evidence/occupied-baseline.md) passed only the existing
movement/turn/error checks. The same command against added feature tests is
proposed and has not run.

For later execution: implement and test S1, run the complete gate, review the
resulting code/test/documentation snapshot, fix findings and recheck affected
behavior, then commit only when authorized. This proposes a code snapshot review;
the fixture defines no additional reviewer identity or human acceptance rule.
S1 is done only when its contract passes, usage/current-spec documentation matches
the delivered API, and the snapshot review is complete. Record actual check
results, reviewed snapshot identity and findings with S1 when performed. This
planning task creates no commit and does not execute that sequence.

Review record for this amendment: design review **pending**; plan review
**pending**; implementation and code review **not started**. Prior completed work
and reports remain unchanged. Draft consistency checks and baseline execution do
not count as the requested reviews.
