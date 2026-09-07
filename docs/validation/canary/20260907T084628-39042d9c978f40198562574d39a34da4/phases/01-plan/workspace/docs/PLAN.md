# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Pending stage S1

Status: planned, unexecuted. Next action in a later implementation phase: deliver
fixed occupancy using the [design amendment](DESIGN.md#occupied-cell-amendment)
and [confirmed contract](SPEC.md#confirmed-occupied-cell-extension--pending-implementation).
This phase permits documents and evidence only; no implementation or commits.

| Stage | Outcome and scope | Dependency / boundary | Acceptance and done condition |
|---|---|---|---|
| S1 — fixed occupied cells | Extend `navigator.py` with optional occupancy, local lookup and blocked-move outcomes; add behavioral coverage in `tests/test_navigator.py`; update README usage when delivered. | Builds on completed S0/D1. One coherent implementation/test/documentation boundary: callers can use the entire feature with continuation and compatibility together. | Meet the design's acceptance examples and invariants, including unchanged heading on failure, subsequent commands, legacy callers and independent runs. Pass the complete existing unittest gate with the new coverage; record results and snapshot review findings, fix findings and rerun affected checks. |

Follow [repository guidance](../AGENTS.md) and the complete check command in
[DEVNOTES](../DEVNOTES.md): `python3 -m unittest discover -s tests -v` (use the
prepared `CANARY_PYTHON` runtime in this fixture). No installs or external actions.
For later execution, implement/test → complete checks → local snapshot review →
fix/recheck. Record the reviewed snapshot identity and findings with stage evidence.
No additional human or agent approval requirement is specified. The intended
future commit boundary is all of S1 together, only if commits are subsequently
authorized; none are authorized now. Do not mark S1 complete from baseline checks.

Baseline verification: [current-phase evidence](evidence/occupied-baseline.md).
Historical completion remains [S0](history/completed.md); its acceptance and D1
remain unchanged. README describes the currently delivered interface until S1.
