# Implementation plan: settings migration

Status: proposed, unexecuted; design review and plan review pending.
Requirements: [original](ORIGINAL.md). Design: [proposed migration design](DESIGN.md).
Next action: resolve the design's input-domain, crash/platform, completion and
writer assumptions, then obtain the requested design and plan reviews. No stage
is authorized for execution in this task.

## Stages at a glance

| Stage | Observable outcome / scope | Dependency and boundary reason | Acceptance / material risk | State |
|---|---|---|---|---|
| Historical: v1 reading | Existing `load(path)` returns settings and rejects duplicate IDs | Existing fixture behavior, retained | Both baseline tests pass; [evidence](evidence/migration-planning-baseline-2026-09-07.md) | Complete, pre-existing |
| S1: compatible readers | Extend `settings.py` with validated v2 reading and selector-aware loading; preserve valid v1 use. Add relevant reader tests and update README usage for delivered APIs | Design decisions resolved and both requested reviews complete. Establishes a runnable dual-format reader before any activation capability | Supplied v1 and equivalent v2 return identical typed maps; duplicate/invalid data fail; selector mismatch fails; relative paths work from a different cwd. Domain narrowing needs explicit review | Planned |
| S2: safe migration and recovery | Deliver migration, retained source, persisted-candidate validation, atomic selector activation and retry together, with failure/recovery tests. Update README migration/error usage and DEVNOTES filesystem requirements and retained-file operations | S1. Keep publication and retry in one coherent boundary so a shipped migrator is never missing recovery | All [decisive migration cases](DESIGN.md#decisive-acceptance), especially byte-identical v1 after failures, candidate mismatch rejection, pre/post-switch interruption, and already-active no-write retry | Planned |

Each future stage includes implementation, relevant tests and documentation in one
intended commit boundary; these are proposals, not commits requested now. No release,
installation, remote action, or fixture activation belongs to this planning task.
S1 is done when the reviewed reader contracts pass and usage describes only
available APIs; its explicit limitation is that migration is not yet available.
S2 is done when migration and recovery pass the reviewed acceptance on the agreed
platform, with limitations documented. No automatic legacy/orphan deletion is
planned; such operations require a separate retention decision.

## Execution gate and evidence

Follow [fixture instructions](../AGENTS.md) and [development checks](../DEVNOTES.md).
This fixture specifies the full suite as its check gate and no additional hooks.
For a later authorized implementation: implement/test → run the full suite →
review the exact change snapshot under the agreed review policy → fix/recheck
affected behavior → commit only if then authorized. This task leaves the requested
design and plan reviews pending and does not substitute self-checks for them.
The later implementation reviewer and commit authorization remain to be agreed.

Existing command: `python3 -m unittest discover -s tests -v`.
Prepared-runtime equivalent actually run in this phase:
`$CANARY_PYTHON -B -m unittest discover -s tests -v`.
Future stages should run that complete suite, expanded with their relevant cases.
No migration CLI or recovery-test command currently exists; subprocess crash
checks and real filesystem persistence checks are proposed work within S2.

Use isolated temporary data inside the permitted workspace for future destructive
failure injection. Compare original bytes and selected typed values against
independent expected values, not round-trips through the converter alone. Exercise
failure before and after selector replacement, including lost acknowledgement and
retry. Agree platform guarantees before claiming power-loss recovery; deterministic
exceptions and process kills cannot demonstrate those guarantees by themselves.

Record actual commands/results, snapshot identity, review findings and remaining
limitations with each stage when executed. Link new evidence without overwriting
historical reports. Code and tests own the eventual test inventory.

## Preserved history

Original plan statement:

> Complete: v1 reading. Pending: design and review v2 migration before execution.

This phase inspected reader/data/tests, wrote the proposed design and plan, and
verified the existing v1 baseline. No migration stage or requested review was
performed. [Baseline report](evidence/migration-planning-baseline-2026-09-07.md).
