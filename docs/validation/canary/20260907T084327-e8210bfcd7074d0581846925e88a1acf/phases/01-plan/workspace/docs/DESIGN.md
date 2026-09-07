# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment D1-O1

Status: proposed amendment; design review pending. D1 above remains the accepted
baseline, with [historical acceptance](history/completed.md) limited to S0.
Outcome: caller-supplied fixed cells block forward movement without ending a run.
Use an optional occupancy input, snapshot it once per run, and test the candidate
destination before updating pose. A blocked move returns a false outcome with the
entire pose unchanged; later commands still execute. Next: review this amendment
and the [pending implementation plan](PLAN.md); implementation is a later task.
Requirements: [confirmed request](OCCUPIED_REQUEST.md) and
[specification addendum](OCCUPIED_SPEC.md), which separates requirements from
proposed interface choices.

### Local extension and rationale

Inspection of [navigator.py](../navigator.py) shows `_target` already computes a
candidate pose without changing state. `run` currently assigns it immediately and
appends `True` for each valid command. Keep this movement/turn structure and add
the occupancy decision only on forward moves. No replacement navigation layer,
dependency, board boundary, routing, persistence or configuration is needed.

Propose `run(pose, commands, occupied=())`, accepting an iterable of integer
coordinate tuples. Existing two-argument calls and the return shape stay compatible.
Convert occupancy to a local `frozenset` once before consuming commands: duplicate
cells collapse, caller data is not mutated, and membership costs expected O(1)
per forward command after O(n) setup and O(u) storage for u unique cells. Repeated
linear search would avoid the copy but cost O(n) per move and would not reliably
support a one-shot iterable. The snapshot supplies the requested fixed occupancy;
there is no shared session state or live obstacle update interface.

Only a destination's `(x, y)` participates in membership. Heading is preserved on
both successful and blocked forward moves. A blocked move appends `False` exactly
once and processing continues; free moves and turns append `True` exactly once.
Turns never consult occupancy. Unknown commands still raise
`ValueError("unknown command")`, without returning partial results.

Proposed edge convention: a starting cell may be occupied; only entry into a
destination is blocked, so the caller can turn or leave that cell. This follows
the requested destination rule without adding a new initial-pose rejection.
Review this convention and the input shape as proposed choices, not additional
confirmed user requirements. Invalid occupancy values are outside the proposed
input contract; no new normalization or custom validation subsystem is planned.

### Acceptance and validation

The hand-derived [acceptance cases](OCCUPIED_SPEC.md#acceptance-examples) include
an eastward block followed by a turn and successful northward move: starting at
`(0, 0, 1)`, commands `FLF`, occupied `{(1, 0)}` yields
`((0, 1, 0), [False, True, True])`. The first command leaves `(0, 0, 1)` intact.

Retain the current checks and add tests for blocked pose preservation in every
heading, continued commands, turns, free movement, default/empty occupancy,
per-run isolation, snapshot/input ownership and the proposed starting-cell rule.
Use independently expected poses and outcomes from the specification; unknown
commands remain errors even after a block. Existing tests pass, as recorded in
[baseline evidence](evidence/occupied-baseline.md), but do not verify this feature.
No implementation or amendment review has occurred. No material code feasibility
unknown remains; interface conventions await the requested design review.
