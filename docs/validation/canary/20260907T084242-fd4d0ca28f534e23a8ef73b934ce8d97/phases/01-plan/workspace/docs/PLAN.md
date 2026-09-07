# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Occupied-cell follow-up

Status: planned; design amendment review and plan review both pending. Next action:
perform those reviews against [D1.1](DESIGN.md#occupied-cell-amendment-d11) and this
plan. Implementation is reserved for a later task.

Authority: [original requirements](ORIGINAL.md), [current spec](SPEC.md),
[confirmed request](OCCUPIED_REQUEST.md), and [addendum](OCCUPIED_SPEC.md).
The completed S0 record is preserved in [historical acceptance](history/completed.md).

| Stage | Observable outcome / bounded scope | Dependencies / boundary reason | Acceptance / material risks | State |
|---|---|---|---|---|
| S1 | Optional caller-supplied occupied cells in `navigator.run`; blocked moves preserve pose, report failure, and permit later commands. Update navigation tests and README usage with the interface and a blocked-session example. | D1.1 and plan reviews, plus later implementation authorization. One coherent proposed commit includes lookup, behavior, regression checks, and usage so the new interface is usable at the boundary. | Meet the [acceptance examples](OCCUPIED_SPEC.md#acceptance-examples); verify omitted/empty occupancy, snapshot and caller-input preservation, repeat calls without state leakage, and unchanged unknown-command errors. Risks: accidentally appending `True` after blocking, checking full pose instead of coordinates, or retaining mutable caller occupancy. | Planned; not implemented, tested, or reviewed |

S1 is done when the public behavior and README agree with the reviewed contract,
the full [development check](../DEVNOTES.md) passes, and the implementation snapshot
has been reviewed with findings resolved. No dependency or configuration changes
are needed. The existing command is `python3 -m unittest discover -s tests -v`;
in this fixture use `"$CANARY_PYTHON" -m unittest discover -s tests -v`. New occupancy
coverage is proposed; the existing three-test baseline is [recorded separately](evidence/occupied-baseline.md).

Execution/review policy: follow [AGENTS.md](../AGENTS.md). For the later task,
implement and test, run the full check above and inspect the diff, review the
resulting snapshot, fix findings and rerun affected checks, then commit only if
authorized by that task. Record actual check results, reviewed snapshot identity,
reviewer and findings in the stage record. This planning task performs no stages,
reviews, or commits; historical acceptance is not approval of S1.
