# Grid navigation: D1 with occupied-cell amendment

Allow callers to supply fixed occupied coordinates through an optional third
argument, proposed as `run(pose, commands, occupied=())`. Before a forward move,
check its destination: an occupied destination produces `False` and leaves the
entire pose unchanged. Continue processing commands so callers can turn and move
away. Existing two-argument calls retain their behavior. For example, from
`(0, 0, 0)` with occupied `{(0, 1)}`, `FRF` returns
`((1, 0, 1), [False, True, True])`.

Decision: D1 remains accepted; this local amendment is proposed. Requirements:
[original](ORIGINAL.md), [confirmed request](OCCUPIED_REQUEST.md), and
[specification addendum](SPEC_OCCUPIED.md). Delivery and review status:
[current plan](PLAN.md). The [original accepted D1](history/design-d1.md) is
preserved verbatim; [historical acceptance](history/completed.md) covers D1 only.

## Boundaries and consequences

Keep state local to each run; no global session. A caller supplies pose and
commands. Retain the direction lookup, unbounded integer coordinates, and turns
that change only heading. Unknown commands still raise `ValueError` and stop
the call; an occupied destination is an ordinary failed command, not an exception.
The return shape remains final pose plus one Boolean per processed valid command.

Proposed input policy: accept an iterable of integer coordinate pairs and take a
set snapshot once at entry. This supports ordinary lists, sets and generators,
avoids consuming an iterator during repeated membership checks, and gives fixed
membership for the run without changing caller data. It costs memory proportional
to distinct occupied cells. Reading caller storage directly would avoid the copy
but would weaken the fixed-membership contract. No new package or persistent state
is needed. Existing pose/command validation is unchanged; malformed occupied
inputs have no new diagnostic guarantee in this amendment.

Only forward destinations are checked. A starting cell may itself be occupied:
turning or leaving it is permitted; later movement back into it is blocked. This
is a proposed interpretation of the request's destination rule, made explicit in
the addendum. Turns always succeed and blocked moves never change heading.

No routing, bounded board, moving obstacles, persistence or configuration file is
introduced. A failed move has no external effects; retrying it with the same pose
and occupied set fails again, while a following turn can enable progress.

## Validation

Use the requirement-derived examples in [the addendum](SPEC_OCCUPIED.md) for
blocked movement, continuation, turns, retry and compatibility. Existing tests
cover a right turn followed by movement, left wraparound and unknown-command
rejection; they do not exercise occupied cells. Planned tests must also establish
snapshot semantics, caller-input preservation and isolation between calls.
Baseline results and future checks live in [the plan](PLAN.md).
