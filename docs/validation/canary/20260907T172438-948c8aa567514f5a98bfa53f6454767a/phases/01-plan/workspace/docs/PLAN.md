# Plan
Next: S1, fixed occupied cells. Status: planned, not executed. Implement the
[confirmed behavior](SPEC.md) using the [proposed design](DESIGN.md), preserving
the completed movement/turning work. This document phase changes no implementation.

| Stage | Outcome and scope | Dependencies / risk | Acceptance and boundary |
| --- | --- | --- | --- |
| S1 — pending | Optional caller occupancy in `navigator.py`; snapshot lookup, blocked F outcome, continued processing, and unchanged turns. Add behavioral coverage in `tests/test_navigator.py` and the optional argument/example in README. | Builds on S0/D1. Main risks are advancing pose on failure, stopping after failure, and changing existing two-argument behavior. Use the design's explicit input assumptions. | Meet the design acceptance examples and ownership/compatibility checks; pass the full existing unittest command with the added checks. One coherent implementation/tests/usage commit boundary is proposed for a later authorized implementation phase. |

Use the [development check instructions](../DEVNOTES.md): implement and test, run
the full unittest discovery check, review the resulting snapshot against S1, fix
findings and rerun affected checks. Record actual results and review findings with
the stage before marking it complete. No independent reviewer or human approval
gate is specified by the fixture. Commits are outside this document-only request;
the proposed boundary does not authorize one. No installation or external action
is required.

Done means the occupied-cell contract and old navigation behavior are verified,
usage matches the implemented API, and snapshot review has no unresolved findings.
[Baseline evidence](evidence/occupied-baseline.md) is not S1 completion evidence.

## Completed history (preserved)
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

The original [S0 acceptance record](history/completed.md) remains historical and
does not cover occupied cells.
