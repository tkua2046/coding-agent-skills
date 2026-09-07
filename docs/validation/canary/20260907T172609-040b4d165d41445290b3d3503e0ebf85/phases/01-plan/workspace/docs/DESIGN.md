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
