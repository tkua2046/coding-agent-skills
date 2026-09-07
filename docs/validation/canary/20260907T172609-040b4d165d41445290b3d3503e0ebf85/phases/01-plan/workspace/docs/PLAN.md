# Plan

Next deliverable: caller-supplied fixed occupied cells, with blocked forward moves
preserving the complete pose and command processing continuing. It depends on the
[confirmed request](OCCUPIED_REQUEST.md) and proposed defaults in [the design](DESIGN.md),
with no separate technical prerequisite. Decisive acceptance is FFRF from
(0, 0, 0), with (0, 1) occupied, producing (1, 0, 1) and
[False, False, True, True].

## Pending outcome

| Outcome / scope | Dependency and boundary | Acceptance evidence |
|---|---|---|
| S1: deliver optional per-run occupancy with collision failure and continued commands; include implementation, meaningful regression tests and README caller usage together | Extends accepted D1/S0. One coherent future commit boundary because API, failure behavior and usage form one local usable outcome; no partial stage or external dependency is needed | All [spec examples](SPEC.md#acceptance-examples), unchanged two-argument behavior and existing regressions pass. Verify fixed snapshot behavior using caller mutation during command iteration, one-shot iterable input, duplicates and isolation across runs. README documents the optional argument and False collision outcome. |

## Execution and review policy

Follow [AGENTS.md](../AGENTS.md) and [DEVNOTES.md](../DEVNOTES.md).
The standard gate is `python3 -m unittest discover -s tests -v`; this fixture uses
the prepared runtime as shown below. Inspect the resulting diff for contract,
scope and documentation consistency. The fixture specifies no additional review
approval or hook gate. Document self-checks are not independent code review or
human acceptance. This phase authorizes documents and local evidence only: no
implementation, commits, installation or external actions. S1 and its tests remain
proposed for a later implementation phase.

## Delivery status

- S0 complete: basic translation and turns, accepted as D1. Existing navigation
  tests cover turns and movement. This completed outcome is retained in the
  [historical record](history/completed.md); the [previous plan](history/pre-occupied-documents.md)
  stated no pending stages before this request.
- S1 pending; no implementation has been performed. Spec and design describe the
  requested extension; README continues to describe the implemented API.
- Baseline verified on 2026-09-07 with
  `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`:
  all 3 existing tests passed (exit 0). This is baseline evidence only, not
  occupied-cell acceptance.
- Inspected navigator.py, tests/test_navigator.py, README, DEVNOTES, AGENTS and
  fixture file/check configuration. No additional check configuration was found.
  Read-only Git inspection returned revision
  cab0e6fb96fd7e5731dde0960e61440ae2b0b7a7 and no status entries before edits,
  but emitted sandbox cache/global-ignore warnings; it is not additional test
  evidence.

Original requirements and confirmed request remain unchanged. The
[pre-amendment document capture](history/pre-occupied-documents.md) preserves
the prior specification, accepted design and completed plan text without
relabeling them as acceptance of occupied-cell behavior.
