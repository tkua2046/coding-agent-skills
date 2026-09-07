# Implementation plan: settings v2 migration

Status: planned; plan review pending, design review pending. No stages executed.
Authority: [original](ORIGINAL.md), [proposed contract](SPEC.md),
[proposed design](DESIGN.md). Next action: resolve the design's consequential open
decisions in design review, then review this plan. Implementation is a later task.

Historical progress, preserved from the preceding plan:
> Complete: v1 reading. Pending: design and review v2 migration before execution.

## Delivery boundaries

| Stage and observable outcome | Dependencies and boundary reason | Acceptance and material risks | Status / intended boundary |
|---|---|---|---|
| S1: Read either selected format safely. Extend `settings.py` with v2 and marker reading, reusable strict migration validation, and relevant tests. Update README for the implemented read APIs. | Design and plan reviews resolved, later implementation authorized. An independently usable read-only stage prepares callers before activation can occur. No migration API or write behavior advertised yet. | Existing v1 tests pass; v2 fixture mapping, malformed/duplicate-key rejection, marker/version mismatch, and relative path resolution match SPEC. Review distinction between legacy v1 reads and strict migration preflight. | Planned; one coherent reader/validation/test/documentation change for review and eventual commit. |
| S2: Explicit migration publishes validated v2 and supports safe retry. Implement the complete publication protocol with tests, migration usage in README, and recovery instructions in DEVNOTES. | S1. Keep source preservation, destination validation, marker activation and retry together: a partial migration writer would lack a safe usable contract. Resolve filesystem durability requirements before claiming them. | All SPEC acceptance examples, deterministic I/O/validation failures, subprocess interruption before/after activation, and repeated retries pass on temporary fixture copies. Source bytes never change. Check unknown outcome after final sync failure and no writes on valid-v2 retry. | Planned; one complete migration/test/operations change for review and eventual commit. |

S2 must keep migration disabled until the caller can read v2. Within this fixture
the S1 dependency supplies that ordering; deployment across multiple applications
is outside scope. No source deletion, cleanup command, package installation,
remote publication or multi-process locking is planned.

## Execution and review policy

Follow [fixture guidance](../AGENTS.md) and [development checks](../DEVNOTES.md).
This phase writes documents and evidence only; requested design and plan reviews
remain pending and no commits are authorized. The two reviews are distinct from
future code review and human acceptance. Do not interpret this draft as approval
to implement.

For a later authorized implementation task: implement the selected stage and its
tests/docs, run the complete unittest discovery gate, review the resulting code
snapshot under the agreed review policy, fix findings and rerun affected checks,
then seek human acceptance as required by that task. Commit only if separately
authorized. No hooks or additional repository commit gates were found in the
fixture. Record actual commands, outcomes, reviewed snapshot identity and findings
when that work occurs; no future review results are implied here.

Existing gate: `"$CANARY_PYTHON" -m unittest discover -s tests -v` in this prepared
environment (DEVNOTES uses `python3` generally). Planned additional coverage is
described in SPEC, not yet runnable as migration tests. Filesystem durability
evidence must be platform-specific if power-loss support is selected in review.

## Evidence and review record

- V1 reading: historically complete; both existing tests passed in this fresh
  context. [Baseline evidence](evidence/migration-baseline.md).
- Design review: pending. Plan review: pending. No review reports superseded.
- S1/S2 implementation, code checks and code reviews: not started.
