# Plan

Current outcome: add caller-supplied fixed occupied cells, report blocked forward
moves without changing pose, and continue commands. Status: planning only;
occupied-cell design review and plan review are pending and have not been
performed. Implementation belongs to a later task.

Next action: review the proposed [D1 amendment](DESIGN.md) and this plan against
the [confirmed request](OCCUPIED_REQUEST.md) and [spec addendum](SPEC_OCCUPIED.md).
The existing D1 acceptance does not cover this amendment.

| Stage | Observable outcome / scope | Dependencies and boundary | Acceptance | State |
|---|---|---|---|---|
| S1 | Optional occupied cells in `navigator.py`, with blocked outcomes, continued commands, regression coverage in `tests/test_navigator.py`, and caller usage in `README.md`. Promote the agreed addendum into the current behavior specification when delivered. | Amendment and plan reviews, resolving any findings, then a later implementation task. One coherent implementation commit keeps the new interface, behavior, tests, and docs together. Main risks are changing pose on failure, stopping the session, or retaining mutable caller state. | Satisfy the addendum examples and D1 regressions; verify blocked motion in all directions, default/empty compatibility, snapshot isolation and separate runs. Run the complete existing unittest gate. | Planned; unexecuted |

Execution policy: follow [repository guidance](../AGENTS.md) and the complete
check command in [DEVNOTES](../DEVNOTES.md). In the later implementation task:
implement and test, run the full gate, review the resulting code snapshot, fix
findings and rerun affected checks, then commit only if authorized in that task.
No code-review performer or human-acceptance policy is specified in this fixture;
record actual reviewer and reviewed snapshot when review occurs, without claiming
acceptance in advance. No commit, installation, or external action is part of
this planning task.

S1 is done when the agreed behavior and usage are delivered, the full gate passes,
and snapshot review findings are resolved. Keep actual results and reviewed
identities in the stage record. The intended commit boundary is the whole S1
outcome, not a separate documentation-only delivery.

Baseline: [existing checks and inspection](evidence/occupied-baseline.md).
The existing command was executed using the prepared `CANARY_PYTHON` runtime;
the same suite with future occupied-cell coverage is proposed, not yet verified.

## Completed history (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Historical acceptance: [completed S0](history/completed.md). It remains evidence
only for the pre-occupancy outcome.
