# Plan

Status: YAML and occupied-cell implementation planned, not executed. Design, plan
and implementation reviews remain pending for this revision. Current outcome:
load and validate starting pose plus approximately 200,000 occupied cells once,
then preserve pose on blocked F and continue commands. Authorities:
[specification](SPEC.md), [design](DESIGN.md), [YAML request](YAML_REQUEST.md).
Next: resolve the design's [open contracts](DESIGN.md#open-contracts), particularly
schema/duplicates and the standard-library/YAML dependency conflict. Independent
movement work can proceed in a future authorized implementation; this phase only
revises documents.

## Pending work

| Stage | Outcome and scope | Dependencies and boundary | Acceptance and state |
|---|---|---|---|
| S1 | Optional fixed occupancy in `navigator.py`, immutable snapshot reuse and blocked-F continuation; corresponding tests and README direct API usage. | Builds on D1/S0. Finalize duplicate-cell and occupied-start policy. One coherent future feature/test/documentation commit boundary; no parser needed. Keep two-argument calls compatible. | Planned. Meet movement and ownership examples in [design acceptance](DESIGN.md#acceptance-and-validation); complete DEVNOTES suite. |
| S2 | Load YAML pose and occupancy atomically before commands, hand off normalized immutable data to S1, and demonstrate representative 200,000-cell operation. Include loader tests, README YAML usage and DEVNOTES dependency/check instructions if approved. | Depends on S1 and resolved schema, YAML language and dependency contracts. One coherent future loader/test/documentation boundary. Safe parser behavior, full-file validation and peak parsing memory are the main risks. | Planned, contract decisions pending. Sample yields blocked F and correct FRF; malformed final entry fails before any command consumption. Test resolved error/duplicate/value policies and one-load reuse; measure load time, peak/retained memory and movement separately. Complete regression suite. |

The two boundaries separate runnable direct movement from the new parsing and
validation contract; S1 alone does not complete the YAML request. Select and verify
a parser only after the dependency constraint is resolved and implementation is
authorized. If representative measurements expose a budget problem, revisit the
representation/loading choice before declaring S2 accepted; no hard budget has
been specified. Detailed cases stay in the design rather than duplicating them.

Each stage is done when implementation, tests and relevant usage/operations docs
agree and its performed review has no unresolved findings. Proposed commit
boundaries do not authorize commits. No implementation, installation, commit,
release or external action is authorized in this phase.

Execution/check policy: follow [DEVNOTES](../DEVNOTES.md). No additional review
policy is specified in the fixture. For future authorized implementation:
implement/test → complete documented checks → local snapshot review against the
specification → fix/recheck affected behavior → commit only when authorized.
No separate human or agent approval gate is introduced. Record actual checks,
reviewed snapshot identity and findings when performed. Design and plan reviews
are pending, not implied by drafting or consistency checks. Implementation reviews
for S1/S2 are also pending. The [fresh baseline](evidence/yaml-baseline.md) is not
feature acceptance; future feature and scale checks have not run.

## Completed work (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Historical acceptance remains in [completed S0](history/completed.md); it predates
occupied-cell support and is unchanged.
