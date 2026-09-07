# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Occupied-cell follow-up

Status: planned only, amended for YAML. Next action: resolve the
[D2 contract questions](DESIGN.md#validation-and-remaining-questions), assess the
amended design and select a parser compatible with the agreed schema before the
YAML stage. Requirements: [SPEC](SPEC.md), [occupied source](OCCUPIED_REQUEST.md)
and [YAML source](YAML_REQUEST.md). [D2](DESIGN.md#occupied-cell-amendment-d2)
remains proposed and unreviewed. This document-only phase executes no stage or
commit; later implementation requires separate authorization.

| Stage | Observable outcome / scope | Dependencies and boundary | Acceptance / risk | State |
|---|---|---|---|---|
| S0 | Basic translation and turns accepted as D1 | Existing completed work | [Historical acceptance](history/completed.md), preserved | Complete (historical) |
| S1 | Optional fixed occupancy; blocked F reports False without changing pose, later commands run. Implement with tests and README usage | S0 and assessed D2 movement/ownership choices. Retains the earlier coherent implementation/review/commit boundary; runnable Python API with YAML explicitly unavailable yet | Original eastward `FLF` example; compatibility, mutation isolation and independent runs; immutable loaded sets must be reusable without rebuilding | Planned, unexecuted |
| S2 | Load and fully validate starting pose and roughly 200,000 cells from YAML before movement; reuse normalized occupancy. Deliver loader, integration tests, example usage and operational/dependency documentation together | S1; resolve schema/value/duplicate/starting-cell/document-feature and API/error questions; select parser and address DEVNOTES standard-library-only policy in the authorized phase. Separate boundary isolates new input/dependency risks while completing the requested path | [D2 acceptance and validation](DESIGN.md#acceptance-and-failure-behavior): example YAML + FLF, invalid final cell consumes no commands, contextual errors, 200,000-cell startup/memory measurement and movement without I/O/rebuilding | Planned, blocked on contract decisions; unexecuted |

S1 is done when its assessed interface/ownership choices, blocked movement,
continuation and compatibility checks pass, README documents actual behavior,
and the repository gate passes. Do not claim YAML delivery at S1.

S2 is done when the resolved schema is recorded in SPEC, rationale in DESIGN,
usage in README and parser/setup/measurement operations in DEVNOTES; the full
load-to-movement path and failure-before-command checks pass; scale measurements
are recorded with versions and any limitations; and the repository gate passes.
No numeric performance threshold is invented. Review measured memory/time against
any subsequently agreed budget. Do not implement a YAML subset as a workaround for
the current no-installation restriction. Dependency evaluation is future work,
not evidence of an available or tested parser.

Execution policy: follow [repository guidance](../AGENTS.md) and the complete
[development gate](../DEVNOTES.md). For later authorized implementation: implement
with tests and usage docs, run the gate, review the resulting snapshot, fix and
rerun affected checks, then commit only if authorized. The fixture specifies no
separate reviewer, hook or human-approval requirement; do not claim an independent
review. No installation, remote action, release or PR work occurs in this phase.

Gate command (existing): `python3 -m unittest discover -s tests -v`; in this fixture
use `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`.
Additional occupancy/YAML cases and scale measurements are proposed, not passed.
Current [YAML baseline](evidence/yaml-baseline.md), prior
[occupied baseline](evidence/occupied-baseline.md) and S0 history remain separate.
Record future stage commands/results, reviewed snapshot identity and findings
separately; code changes invalidate affected checks. S1/S2 execution, design
review and plan review remain pending.
