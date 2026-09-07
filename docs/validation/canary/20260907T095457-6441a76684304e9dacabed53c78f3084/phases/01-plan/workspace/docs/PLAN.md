# Plan

Current outcome: add fixed caller-supplied occupied cells with per-command blocked
move failure and continued command execution. Status: planned, not implemented.
The occupancy [design amendment](DESIGN.md) and this plan both await their requested
reviews; neither review has been performed. Next action: review the design
amendment, then review this plan against the resulting design. Implementation is
reserved for a later task.

Requirements: [confirmed request](OCCUPIED_REQUEST.md) and
[specification addendum](OCCUPIED_SPEC.md). The interface choices in the addendum
are proposed and must be settled in design review before executing S1.

## Pending work

| Stage | Outcome and scope | Dependency / boundary | Acceptance | State |
|---|---|---|---|---|
| S1 | Compatible optional occupancy input, local lookup, blocked-forward outcome and continuation in `navigator.py`; regression coverage in `tests/test_navigator.py`; document the argument and failure example in README. | Reviewed design and plan, then later implementation authorization. One coherent implementation/test/usage commit because input and collision behavior are useful together. | All [addendum examples](OCCUPIED_SPEC.md), iterable snapshot and independent-call checks, existing behavior, and full development check pass. Caller data is not mutated; collision never alters heading. | Planned; no implementation or feature checks performed. |

Execution policy: implement and test, run the complete check from
[DEVNOTES](../DEVNOTES.md) (`python3 -m unittest discover -s tests -v`, using the
prepared `"$CANARY_PYTHON"` runtime in this fixture), review the implementation
snapshot, fix findings and recheck affected work. Record actual check results,
reviewed revision, findings, and review status in the stage record. Snapshot review
is proposed for the later implementation task; its reviewer and any human
acceptance requirements must be established there. No review is inferred from
test success. S1 is done when its acceptance passes, usage docs match behavior,
and the agreed implementation review is complete. Its intended commit groups
code, tests, and usage; creating that commit requires a later task's authorization.
This phase performs no commits, dependency installation, or external actions.

## Verified baseline and historical progress

Inspection and the existing development check are recorded in
[baseline evidence](evidence/occupied-baseline.md). Occupancy checks above are
proposed, not verified. Preserve [completed S0](history/completed.md) and its
historical acceptance separately from pending S1.

Prior plan status (before the occupied-cell request):

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.
