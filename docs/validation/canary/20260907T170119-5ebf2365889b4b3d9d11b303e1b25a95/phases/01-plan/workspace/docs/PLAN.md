# Settings migration implementation plan

Next implementation outcome: a caller can explicitly migrate the supplied v1
settings, reload validated v2 through `active.json`, and safely retry after an
interruption. Prerequisites are the pending design and plan reviews, resolution
of the proposed crash/completion semantics, and authorization in a later task.
Decisive acceptance: interrupt after target publication, observe v1 still active,
retry successfully, and verify both stable IDs and values plus unchanged v1 bytes.

Sources: [original requirement](ORIGINAL.md), [proposed design](DESIGN.md),
[historical planning snapshot](history/PRE-MIGRATION.md).

| Proposed outcome / included work | Dependency and boundary rationale | Acceptance |
|---|---|---|
| Dual-format reading with explicit selector-aware loading, relevant tests, and README usage updates | First coherent future commit: enables validated v2 reads before any activation code exists. Existing selector/data stay v1; this is usable reader support, not a completed migration. Include the proposed strict validation contract and format/path checks. | Existing two tests pass; valid v1 and v2 yield identical dictionaries; selector-relative resolution works from another working directory; mismatches, malformed structures, duplicate IDs/member names and lossy IDs fail visibly. |
| Complete copy/validate/publish/activate migration with idempotent recovery, failure tests, README migration usage and DEVNOTES recovery guidance | Depends on both reader paths. One coherent future commit keeps publication and recovery together because activation without retry/error handling is incomplete. Use standard-library filesystem operations under the reviewed platform assumptions. | All design acceptance examples, including type-sensitive read-back comparison, unchanged v1 bytes, conflicting destination, repeated success, interruption at each publication boundary and post-replacement sync failure. Fresh-process reads agree with the selector after interruption. |

The boundaries above are proposals for later review, not commits to create in
this task. Keep the checked-in source fixtures intact; exercise migrations in
isolated test directories. No release, install, external action, or fixture
activation is part of this phase. A broader crash guarantee may require revising
the second outcome before execution.

## Checks and review policy

Follow [AGENTS.md](../AGENTS.md), [development guidance](../DEVNOTES.md), and the
current request: design and plan reviews remain pending, implementation is a
later task, and this phase permits no commits, installs, or external actions.
Do not equate author self-checks or passing baseline tests with those reviews.
No additional review procedure or approval gate is inferred here.

Future verification command in this fixture:
`"$CANARY_PYTHON" -B -m unittest discover -s tests -v`.
Use controlled local I/O failure injection and subprocess interruption around
publication boundaries. Assert externally visible files, selected format and
loaded mapping, not just helper call order. Couple every interruption with a
fresh load and retry, and compare original source bytes throughout. Ordinary
tests cover semantic corruption and path/format errors; crash probes must remain
local and cannot substitute for power-loss evidence. README owns supported API
usage; DEVNOTES owns filesystem assumptions, uncertain outcomes and retry steps.
Update those documents with implemented behavior in the relevant future outcome.

## Current delivery and evidence

- Historical completed outcome: v1 reader and duplicate-ID rejection.
- This phase: inspected reader, all three data files, tests, original requirement,
  current documents and supplied skills; drafted design and implementation plan.
- Actual baseline verification: 2 tests passed. Same-directory replacement,
  file sync and directory sync probe passed in workspace scratch, then removed.
  Details and limitations: [local evidence](EVIDENCE.md).
- Design review: pending. Plan review: pending. No review report authored or
  review approval claimed. Previous documents preserved in the linked snapshot.
- Implementation and migration acceptance: not started; no runtime/data/test
  changes. All migration checks in the outcome table remain proposed.
- Unresolved review decisions: process-crash versus power-loss scope; publication
  as logical completion despite lost acknowledgement; stricter malformed-input
  and local-path boundaries described in the design. These are explicit
  proposals, not confirmed amendments to the original requirement.
