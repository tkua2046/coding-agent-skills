# Plan: settings v2 migration

Status: proposed; plan review pending, implementation not started.
Authority: [original requirement](ORIGINAL.md); proposal: [design](DESIGN.md).
Next action: resolve the design's open decisions in the requested design review,
then perform the separate plan review. Both reviews remain pending by user request.
This plan does not authorize implementation, commits, installation or external actions.

## Delivery boundaries

| Stage | Observable outcome and scope | Dependency / boundary reason | Acceptance and done condition | State |
| --- | --- | --- | --- | --- |
| S1: compatible validated reading | Extend `settings.py` with v2 reading and selector loading, plus strict validation usable by migration. Keep current direct v1 loading behavior. Add relevant tests and update README usage for these implemented readers. No activation or migration command yet. | Reviewed design and plan, then a later implementation task. Settle input and selector contracts first; readers must work before any caller can switch. | Existing v1 tests pass; v2 returns the hand-derived fixture map; selector resolution works from another working directory; mismatched versions, duplicate v2 keys and malformed selected data fail explicitly. Nested typed values and empty settings are preserved. Reader-only limitation documented. One coherent reader/validation commit boundary for later authorization. | Planned |
| S2: durable migration and retry | Add the full source-preserving candidate/validation/selector protocol with recovery tests in the same change. Document explicit migration usage in README and interruption, retry, storage assumptions and orphan handling in DEVNOTES. | S1; settle exclusive-writer and filesystem support assumptions. Keep activation with crash/retry coverage so an incomplete protocol is never presented as usable. | All [design acceptance examples](DESIGN.md#acceptance) pass, including rejected duplicates/non-string IDs, original-byte preservation, independent round-trip comparison, injected persistence failures, subprocess interruption and fresh-process retry on both sides of commit. Repeating a successful migration leaves selector/target unchanged. One coherent migration/recovery commit boundary for later authorization. | Planned |

The proposed public API is `load_active(selector_path)` and `migrate(selector_path)`;
review may change these before S1. There is no application caller in the fixture:
accept integration through the selector reader and document how a caller adopts it.
Do not invent an application or automatically migrate on ordinary reads.

## Execution and review policy

Follow [fixture guidance](../AGENTS.md) and [development checks](../DEVNOTES.md).
No additional hook or code-review policy is supplied. For the later authorized task:
implement/test each coherent stage, run the complete unittest suite with the prepared
runtime, record the exact snapshot/check results, review the implementation snapshot,
fix findings and rerun affected checks plus the suite. Record who reviewed which
snapshot; do not label an unperformed review as passed. Commits require scope in
that later task; no commits or code execution stages occur during this planning phase.

Existing check, verified for baseline:
`"$CANARY_PYTHON" -B -m unittest discover -s tests -v`.
Use the same suite command after extending tests; crash and failure tests are
proposed and do not exist today. Test subprocesses should use the prepared runtime
and isolated directories inside the authorized workspace, never mutate fixture data.
Use synchronization at protocol boundaries rather than timing-only sleeps. Compare
expected values independently, and read persisted state in a fresh process after
termination. Storage-platform verification is required before claiming power-loss
support; unsupported durability semantics block that claim rather than weakening
the source-preservation requirement silently.

## Evidence and history

- Historical plan, retained verbatim: “Complete: v1 reading. Pending: design and review v2 migration before execution.”
- Baseline v1 reading remains complete; migration stages remain planned.
- [Fresh-context inspection and local evidence](evidence/migration-baseline.md).
- Design review: pending. Plan review: pending. Implementation review: not started.
- No historical review reports were present in the inspected fixture; none were rewritten.
