# Plan: settings v2 migration

Status: planned only. Design review pending; plan review pending. Implementation
is deferred to a later task. Next: resolve and review the choices in
[DESIGN](DESIGN.md#validation-and-open-decisions), then review this plan against
[ORIGINAL](ORIGINAL.md) and the proposed [SPEC](SPEC.md).

Historical progress retained verbatim:

> Complete: v1 reading. Pending: design and review v2 migration before execution.

## Ordered delivery boundaries

| Stage | Observable outcome / scope | Dependency / boundary reason | Acceptance / done condition | State and proposed commit boundary |
|---|---|---|---|---|
| S1: compatible readers and validation | Extend `settings.py` for v2 and selector reading, add migration-specific validation; preserve direct v1 compatibility. Include tests and README usage. | Reviewed contract choices and later implementation authorization. Dual reading must work before any activation. | Existing tests plus direct v1/v2 equivalence, selector-relative paths, format mismatch, strict duplicate parsing and typed-value cases in [SPEC](SPEC.md#decisive-acceptance-examples) pass. No migration API advertised yet. | Planned; one coherent reader/validation commit in a future authorized task. |
| S2: publication and recovery | Deliver migration with retained source, validated staged output, atomic selector switch, safe retry and collision errors. Include fault tests, README migration usage and DEVNOTES operations/recovery guidance. | S1 and resolved storage guarantees. Target publication and activation form one outcome so an incomplete migration API is never exposed. | All SPEC examples pass, including fresh-process interrupted retry and uncertain completion. Verify source bytes and complete old/new selection at write/sync/rename boundaries; full suite passes. Docs explain supported storage, exclusive writer coordination, retained source, collisions and explicit recovery. | Planned; one migration/recovery commit with its tests and documentation. |

Tests use isolated directories. Do not migrate checked-in data or change its
selector as part of implementing the feature. No dependency, release, PR,
external action or automatic source cleanup is planned.

## Execution and review record

Repository policy: [AGENTS](../AGENTS.md), [DEVNOTES](../DEVNOTES.md). This phase is
documents and local evidence only, with no commits. Neither requested document
review has been performed or implicitly approved.

In a later authorized task: implement a stage with tests, run relevant checks and
the full standard-library suite, review the code/test/document snapshot under the
then-agreed policy, fix findings and rerun affected checks, and commit only if
authorized. The fixture supplies no further code/human review gate; establish that
policy in the implementation task without treating document review as code acceptance.

Existing command: `"$CANARY_PYTHON" -m unittest discover -s tests -v`, using the
prepared runtime in place of DEVNOTES' `python3`. Both baseline tests passed;
[evidence](evidence/migration-baseline.md) records limits. Future stage checks use
the same discovery command after adding planned tests. Fault injection and
subprocess recovery checks remain proposed, not executed.

Record future stage results, reviewed snapshot identities and finding dispositions
here or in linked evidence. Preserve historical progress and prior reports.
