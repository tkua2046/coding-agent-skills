# Occupied-cell implementation plan

Next: deliver optional fixed occupied cells in one runnable increment, with
blocked moves preserving the pose and later commands continuing. This depends on
the proposed [D1 amendment](DESIGN.md) and [API clarifications](SPEC_OCCUPIED.md).
For `(0, 0, 0)`, commands `FFRF`, and occupied `{(0, 1)}`, acceptance is
`((1, 0, 1), [False, False, True, True])`. Implementation belongs to a later task.

| Proposed outcome and scope | Dependency and boundary | Acceptance |
|---|---|---|
| S1: Extend `navigator.run` with optional fixed occupancy, preserving existing calls and errors; add regression tests and update README usage with blocked-move outcomes and a continuation example. Update current SPEC behavior when delivered, retaining original requirements and addendum provenance. | Uses existing `_target` and command loop; no packages or infrastructure. One proposed commit keeps behavior, tests, and public documentation usable together; no useful partial delivery requires a split. Resolve any changes arising from pending document reviews before executing affected choices. | Run the standard unittest suite, retaining all baseline cases and covering the addendum's failure, recovery, boundary, iterable, snapshot, and call-isolation examples. Cover occupied forward destinations in all four headings. Verify README examples against the delivered API. |

Sources: [original request](ORIGINAL.md), [current specification](SPEC.md),
[occupied request](OCCUPIED_REQUEST.md), [design](DESIGN.md), and
[acceptance examples](SPEC_OCCUPIED.md#acceptance-examples).

Execution/check policy: [AGENTS.md](../AGENTS.md) and
[DEVNOTES.md](../DEVNOTES.md). Standard check:
`python3 -m unittest discover -s tests -v`, using the supplied prepared runtime in
this fixture. This task authorizes documentation and local evidence only: no
implementation, commits, dependency installation, or external actions. Requested
design and plan reviews remain pending until performed; author self-checks do not
constitute reviews. No additional approval procedure is introduced here.

## Current status

- S1 is proposed and unimplemented. No feature checks have been run against an
  implementation of occupied cells.
- Design amendment review: pending, not performed. Plan review: pending, not
  performed. Historical D1 acceptance does not accept this amendment.
- Baseline inspection on 2026-09-07: read navigation code, all three tests,
  README, DEVNOTES, specifications, design, plan, and historical acceptance.
  No additional check configuration was found in the fixture file inventory.
- Actual baseline command: `"$CANARY_PYTHON" -m unittest discover -s tests -v`.
  Exit status 0; all 3 tests passed (`test_turn_and_forward`, `test_left_wraps`,
  `test_unknown_command`). This establishes existing behavior only.
- Initial `git status --short` produced no changed-file entries but emitted
  sandbox warnings about Git cache and user ignore paths; it is not used as
  evidence of feature correctness.

## Preserved progress

Complete: basic translation and turns, accepted as D1, with no pending stages
before this request. See the unchanged [S0 historical record](history/completed.md)
and the verbatim [previous plan](history/plan-before-occupied.md). These are
historical records, not new execution or review evidence.
