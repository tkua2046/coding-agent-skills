# Documents before YAML planning

Captured verbatim before the YAML amendment. Prior proposals and baseline reports are historical evidence, not new acceptance or review.

## docs/SPEC.md

# Navigation behavior

This target contract includes the [confirmed occupied-cell request](OCCUPIED_REQUEST.md).
Implementation status lives in [the plan](PLAN.md#delivery-status). The
[original request](ORIGINAL.md) and [previous specification](history/pre-occupied-documents.md)
are preserved.

The grid is unbounded, with integer coordinates and headings 0, 1, 2, 3 for
north, east, south, west. A caller supplies a pose and commands. Return the final
pose and one Boolean success outcome per processed valid command. L/R turn in
place and succeed. Unknown commands raise ValueError.

The caller may supply fixed occupied cells. F into an occupied cell fails,
reports False for that command, and preserves both position and heading.
Processing continues with the next command. F into a free cell advances one
cell and succeeds. Omitting occupied cells preserves existing behavior.

## Proposed interface defaults

Use an optional third argument, `run(pose, commands, occupied=())`. Supply a finite
iterable of integer `(x, y)` pairs, copied once for the run. Duplicates have no
additional effect. Occupancy applies to forward destinations only: an occupied
starting cell does not invalidate the supplied pose or prevent turns or departure.
No new malformed-input validation is specified. These are design defaults, distinct
from the confirmed collision requirements above.

## Acceptance examples

| Initial pose | Occupied cells | Commands | Final pose | Outcomes |
|---|---|---|---|---|
| (0, 0, 0) | omitted or empty | RF | (1, 0, 1) | [True, True] |
| (0, 0, 0) | {(0, 1)} | FFRF | (1, 0, 1) | [False, False, True, True] |
| (0, 0, 0) | {(0, 1)} | FL | (0, 0, 3) | [False, True] |
| (0, 0, 0) | {(0, 0)} | FRRF | (0, 1, 2) | [True, True, True, False] |
| (0, 0, 3) | {(-1, 0)} | F | (0, 0, 3) | [False] |
| (0, 0, 0) | {(0, 1)} | empty | (0, 0, 0) | [] |

After a blocked F, an unknown command still raises ValueError. Independent runs
do not share occupancy. Routing, persistence, moving obstacles, board boundaries
and configuration files are outside scope.

## docs/DESIGN.md

# Occupied-cell extension to D1

Add an optional occupied-cell iterable to each run, snapshot it into a set, and
check each forward destination before replacing the pose. This preserves local
state and existing two-argument calls while making collision a normal command
failure. For example, from (0, 0, 0) with (0, 1) occupied, FFRF returns
(1, 0, 1) and [False, False, True, True]: repeated failures preserve the pose,
then a turn and free move succeed.

Collision behavior is [confirmed](OCCUPIED_REQUEST.md). Interface and snapshot
defaults below are proposed design choices, ready for implementation planning;
they have not received new acceptance. D1's unrelated decisions remain accepted:
local per-run state, direction lookup, unbounded coordinates and ValueError for
unknown commands. See the [original D1 text](history/pre-occupied-documents.md)
and [completed S0 record](history/completed.md).
Requirements: [original](ORIGINAL.md), [target specification](SPEC.md).
Delivery and check evidence: [current plan](PLAN.md#delivery-status).

## Interface and state ownership

Use `run(pose, commands, occupied=())`, retaining the return shape and default
behavior. Accept a finite iterable of integer coordinate pairs; consume it once
into a private set before processing commands. This supports sets, lists and
one-shot iterables, collapses duplicates and prevents later caller mutation from
changing occupancy during command processing. It costs memory proportional to
distinct cells. Borrowing a mutable collection would couple session behavior to
the caller, contrary to fixed occupancy. No dependency is needed.

Only the candidate destination is checked. Permit a supplied starting pose in an
occupied cell, including turning and leaving it; returning into that cell fails.
This preservation default follows the request's restriction on forward entry
without adding initial-pose validation. Keep existing pose/command validation
behavior; malformed occupied input is outside the supported contract.

## Movement and failure

The existing `_target` helper calculates a full candidate pose without mutation.
Use that candidate's coordinates for membership; on collision retain the entire
old pose and append False exactly once. Otherwise adopt the candidate and append
True. Turns keep succeeding regardless of occupancy. Every subsequent command
follows the same rules, including ValueError for unknown commands.

There is no persistent or external state to repair. Retrying a blocked forward
move still fails while the same cell remains occupied; turning toward a free
destination allows progress in the same command stream. Occupancy belongs only
to this call and does not leak to later runs.

## Evidence and acceptance

Inspection of navigator.py shows forward movement currently adopts `_target`
unconditionally and every valid command appends True. The three existing tests
cover right-turn movement, left wraparound and unknown-command rejection; none
covers occupied cells. Use the [specification examples](SPEC.md#acceptance-examples),
plus iterable snapshot isolation, duplicate cells and independence between runs.
Preserve existing navigation tests. No routing, persistence, moving obstacles or
configuration interface is introduced.

## docs/PLAN.md

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
