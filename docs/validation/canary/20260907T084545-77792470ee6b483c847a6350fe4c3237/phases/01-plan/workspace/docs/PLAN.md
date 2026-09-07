# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Occupied-cell follow-up

Status: planned only. Next action: assess proposed D2 choices, then implement S1
in a separately authorized implementation phase. Requirements: [SPEC](SPEC.md)
and [confirmed source](OCCUPIED_REQUEST.md). Design:
[D2 amendment](DESIGN.md#occupied-cell-amendment-d2), not yet reviewed.
The current phase changes documents only; it executes no stage or commit.

| Stage | Observable outcome / scope | Dependencies and boundary | Acceptance / risk | State |
|---|---|---|---|---|
| S0 | Basic translation and turns accepted as D1 | Existing completed work | [Historical acceptance](history/completed.md), preserved | Complete (historical) |
| S1 | Optional fixed occupancy; blocked F reports False without changing pose, and later commands run. Update `navigator.py`, relevant tests and README usage together | Builds on S0 and proposed D2. One coherent implementation/review/commit boundary keeps lookup, failure handling and continuation usable together | [D2 acceptance and validation](DESIGN.md#acceptance-and-failure-behavior); main risks are accidental early termination, pose mutation on failure and borrowed mutable occupancy | Planned, unexecuted |

S1 is done when its public interface and ownership decisions match the assessed
design, the blocked-F/turn/free-F example passes, compatibility and isolation
checks pass, README describes the implemented optional argument, and the complete
repository test gate passes. Keep behavior in SPEC, rationale in DESIGN, usage
in README and operations in DEVNOTES. README remains accurate for current code
during this document-only phase.

Execution policy: follow [repository guidance](../AGENTS.md) and the complete
[development gate](../DEVNOTES.md). For later authorized implementation: implement
with tests and usage docs, run the gate, review the resulting snapshot, fix and
rerun affected checks, then commit only if authorized. The fixture specifies no
separate reviewer, hook or human-approval requirement; do not claim an independent
review. No installation, remote action, release or PR work is planned.

Gate command (existing): `python3 -m unittest discover -s tests -v`. In this
fixture use the prepared runtime as recorded in [baseline evidence](evidence/occupied-baseline.md).
Additional occupancy cases are proposed additions to that suite, not checks
already passed. Record future S1 commands/results, reviewed snapshot identity
and findings separately from S0 and this baseline; a code change invalidates
affected check results. No S1 execution or review evidence exists yet.
