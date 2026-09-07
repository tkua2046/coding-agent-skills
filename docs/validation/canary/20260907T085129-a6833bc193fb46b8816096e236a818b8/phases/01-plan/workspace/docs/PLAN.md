# Implementation plan: settings migration

Status: proposed; plan review pending. [Requirements](ORIGINAL.md) · [proposed design](DESIGN.md). Design review also remains pending; this plan does not treat proposed decisions as approved.

Next action: resolve the design's input, persistence, completion and ownership decisions, then obtain design and plan reviews. Implementation belongs to a later task. No stages or commits are executed here.

## Stages at a glance

| Stage | Observable outcome / scope | Dependencies and boundary reason | Acceptance / material risk | State / intended boundary |
|---|---|---|---|---|
| S0: review readiness | Settle [open design decisions](DESIGN.md#validation-and-open-decisions), document supported filesystem guarantees and review the resulting design/plan | Required before implementation; original crash requirement cannot be weakened by assumption | Explicit review of lossy ID coercion, malformed-input compatibility, activation commit and host-crash scope; preserve historical review records tied to their reviewed revision | Pending design and plan reviews; no implementation commit |
| S1: compatible reader and validated conversion | Extend `settings.py` to read v2 and validate/convert v1 without activating files; add relevant reader/conversion tests and README usage | S0; yields a runnable reader for both representations while v1 remains selected | Normal/duplicate fixtures, empty and nested values, strict malformed-input cases, non-string IDs, exact type-sensitive equality from [acceptance](DESIGN.md#acceptance). Existing reader behavior on valid v1 retained | Planned; one coherent reader/validation commit, if later authorized |
| S2: durable activation and retry | Add explicit migration and selector handling, exclusive candidate creation, persisted validation, ordered sync and atomic selector replacement, caller success semantics; include crash/error/retry tests and usage/operations docs | S1; writing, activation and recovery ship together because a partial activation protocol risks original-data usability. Establish platform primitives before enabling activation | All remaining design acceptance cases, including candidate corruption, every write/sync/replace boundary, fresh-process interruption before/after commit, already-v2 retry and collision preservation. Assert original bytes, selector validity and full expected mapping on recovery | Planned; one coherent migration/recovery commit, split only if each intermediate state cannot activate unsafely |

S1 deliberately does not expose a migration API that pretends to activate data. S2 uses temporary test directories, never the checked-in live selector as a migration target. Runtime modules remain standard-library only. README owns public usage; DEVNOTES owns supported filesystem assumptions, uncertain completion recovery and retained-file operations. Design acceptance changes must be reflected in the design; private helper/test details belong in code.

## Execution and validation policy

Follow [fixture guidance](../AGENTS.md) and [development checks](../DEVNOTES.md). For a later authorized implementation: implement with relevant tests → run the complete unittest gate → review the concrete changed snapshot → fix and recheck affected behavior. No commit, install, external action or implementation is authorized in this phase. Future commits require the later task's authorization; the boundaries above are proposals. No autonomous design/plan review or reviewer approval is claimed. Record actual reviewer, reviewed revision/snapshot, findings and disposition when reviews occur; changed code requires affected checks/review to be refreshed.

Existing complete gate: `python3 -m unittest discover -s tests -v`. In this fixture use `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`. The [baseline run](evidence/migration-baseline.md) is actual evidence for v1 only. Future acceptance and fault-injection tests are proposed, not run. S1 is done when its observable contract and full gate pass with snapshot review recorded; S2 additionally requires the entire recovery contract to pass and supported durability limits to be documented. A passing process-kill test alone cannot close the power-loss question.

## Historical progress and review record

Preserved prior plan: “Complete: v1 reading. Pending: design and review v2 migration before execution.”

Current preparation: reader/data/tests inspected, proposed design and plan drafted, baseline checked. No implementation stages completed. Design review: pending. Plan review: pending. No historical review reports were present in the fixture file inventory; any later reports must retain their original reviewed scope and identity.
