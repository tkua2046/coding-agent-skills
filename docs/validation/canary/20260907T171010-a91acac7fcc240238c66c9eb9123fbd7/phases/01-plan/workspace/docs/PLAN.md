# Plan

Status: occupied-cell implementation planned, not executed. Next outcome: S1 adds
fixed caller-supplied occupancy, failure without pose change, and continued command
processing. Authorities: [specification](SPEC.md) and [design amendment](DESIGN.md#occupied-cell-amendment).

## Pending work

| Stage | Outcome and scope | Dependencies and boundary | Acceptance and state |
|---|---|---|---|
| S1 | Extend `navigator.py` with optional occupancy and blocked-F outcomes; add regression checks in `tests/test_navigator.py`; update README usage for the implemented interface. | Builds on completed D1/S0. One coherent implementation/test/documentation boundary because occupancy lookup and failure/continuation behavior must work together. Main risks are pose mutation on failure, premature command termination and breaking two-argument calls. | Planned. Meet the [design examples and ownership checks](DESIGN.md#acceptance-and-validation), preserve unknown-command errors and pass the complete suite in DEVNOTES. |

S1 is done only when the implementation, usage documentation and checks agree and
the review has no unresolved findings. Its intended future commit boundary contains
the feature, relevant tests and README change together. No implementation, commit,
installation, release or external action is authorized by this planning phase.

Execution/check policy: follow [DEVNOTES](../DEVNOTES.md). No additional review
policy is specified in the fixture. For a future authorized implementation, use
implement/test → complete documented checks → local snapshot review against the
specification → fix/recheck affected behavior → commit only when authorized.
No separate human or agent approval gate is introduced. Record actual checks,
reviewed snapshot identity and findings with the stage when performed; none has
been performed for S1. [Baseline evidence](evidence/occupied-baseline.md) is not
feature acceptance.

## Completed work (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Historical acceptance remains in [completed S0](history/completed.md); it predates
occupied-cell support and is unchanged.
