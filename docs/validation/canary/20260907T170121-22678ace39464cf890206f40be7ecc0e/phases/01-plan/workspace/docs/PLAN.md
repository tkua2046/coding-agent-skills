# Implementation plan: settings v2 migration

Status: planned only; **design review and plan review pending**. No stages executed.
Next: review [DESIGN](DESIGN.md) and resolve its input, activation and durability
boundaries, then review this plan. Implementation belongs to a later authorized task.
Authority: [ORIGINAL](ORIGINAL.md), [proposed contract and A1–A8](SPEC.md).

## Delivery stages

Each row is an intended coherent code/test/document commit boundary for later work,
not a request to commit now. Consequential design revisions must update affected
pending stages before execution.

| Stage | Observable outcome / scope | Dependencies / boundary reason | Acceptance / done condition | State |
|---|---|---|---|---|
| S1: Read both formats safely | Extend `settings.py` and tests with direct v2 reading, selector-aware reading and strict migration-input validation. README documents supported reads. No migration writes yet. | Document reviews and later implementation authorization. Establish decoding before mutation; dual-format reading is independently usable. | Existing tests pass; A2–A4 validation and A8 selected-file errors pass where applicable; A1 mappings agree for supplied v1/v2 test inputs. Relative selection works regardless of working directory and rejects format mismatch. No reads alter data. | Planned |
| S2: Validated, recoverable activation | Add explicit migration, exclusive destination creation, persisted comparison, ordered syncs, atomic selector replacement and retry. Include I/O fault tests. README owns invocation/API; DEVNOTES owns platform assumptions, retained files and recovery instructions. | S1. Keep output creation and activation together so no partial public migrator is advertised. | A1–A8 pass in normal/fault-injected tests, including pre/post-replacement distinctions and final directory-sync failure reconciliation. Source bytes unchanged, values compared with types, repeated success writes nothing. Unrelated files never overwritten/deleted. Required platform sync behavior checked; unsupported operations fail before publication. | Planned |
| S3: Crash acceptance and handoff | Subprocess interruption/restart checks during target writing, after durable target publication, after selector staging and after replacement. Update DEVNOTES from actual recovery evidence. | S2. Exercise the complete protocol beyond exceptions; S2 is not migration-ready until this stage passes. | A5/A7 pass through fresh processes: selected data valid, v1 bytes unchanged, retry yields exactly original IDs/values, orphans unselected. Full suite passes. Required power-loss guarantees have platform evidence or remain an explicit release blocker. | Planned |

## Checks and later execution policy

Follow [fixture guidance](../AGENTS.md) and [operations](../DEVNOTES.md). No additional
hooks or code-review policy were supplied. In a later authorized task: implement/test
each coherent stage → run the full standard-library suite → inspect the exact diff
and record findings → fix and rerun affected checks → obtain any then-required
review/commit authorization. This is not permission to implement or commit now.
No installations, services, releases or PR work are planned.

Verified baseline command in this environment:

```sh
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v
```

That command is also proposed for the enlarged suite; future coverage does not exist
today. Use temporary directories inside the allowed workspace, never migrate the
checked-in data during tests. Fault checks inspect source bytes and selection state,
not just raised exceptions. Unit/process tests alone cannot prove power-loss safety.

## Evidence and review record

- Historical completed outcome: v1 reading, preserved below; its two tests pass.
- This phase: inspected reader/data/tests, ran bounded input probes, drafted contract,
  design and plan. [Baseline evidence](evidence/migration-baseline.md).
- Design review: pending. Plan review: pending. No review reports were present in
  the inspected fixture; none were removed or rewritten.
- S1/S2/S3 execution, implementation checks and code review: not performed. Append
  future outcomes, checked snapshots and findings here or link reports, preserving
  history when pending stages change.

## Preserved prior plan

Original `docs/PLAN.md` text before this drafting phase:

> # Current plan
> Complete: v1 reading. Pending: design and review v2 migration before execution.
