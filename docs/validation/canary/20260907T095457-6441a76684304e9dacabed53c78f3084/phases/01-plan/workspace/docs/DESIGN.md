# Navigator design

Current outcome: extend the accepted navigator with caller-supplied fixed occupied
cells. D1 remains accepted; the occupancy amendment below is proposed and its
design review is pending. Requirements: [original](ORIGINAL.md),
[confirmed request](OCCUPIED_REQUEST.md), and [addendum](OCCUPIED_SPEC.md).

Use a per-run immutable coordinate lookup and check a forward destination before
changing pose. A blocked move returns `False` for that command, leaves the entire
pose unchanged, and allows subsequent commands. Existing two-argument calls keep
their behavior. Next: perform the amendment design review and the separate
[plan](PLAN.md) review; implementation belongs to a later task.

## Accepted design D1 (preserved)

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Historical acceptance: [completed S0](history/completed.md). That acceptance does
not cover this amendment.

## Proposed occupancy amendment

The current `navigator.py` computes forward destinations in `_target` and assigns
them immediately in `run`; every recognized command currently appends `True`.
Retain the direction lookup and turn arithmetic. Propose the compatible interface
`run(pose, commands, occupied=())`, accepting an iterable of integer `(x, y)` tuples.
Snapshot it into a local `frozenset` once per run. This avoids caller mutation and
one-shot iterable consumption affecting successive membership checks, collapses
duplicates, and gives expected constant-time membership at a linear setup and
storage cost. Scanning the supplied iterable on every move is simpler only for
tiny reusable collections and fails for exhausted iterators; no new dependency or
shared obstacle registry is justified.

For `F`, compute the candidate using the existing translation, check its `(x, y)`,
and accept the full candidate only if free. Append `False` on a collision and
`True` on a successful move or turn. The invariant is that failure changes neither
position nor heading. Do not catch unknown-command `ValueError` as a collision.
Occupancy constrains entry destinations only; turns remain available even if the
initial cell is listed. Input conventions and this starting-cell interpretation
are proposed decisions, not additional confirmed user requirements; see the
[addendum](OCCUPIED_SPEC.md).

## Acceptance and validation

From `(0, 0, 1)` with occupied `{(1, 0)}`, `FRF` must return
`((0, -1, 2), [False, True, True])`: east is blocked, right faces south, then
south is free. This checks failure, unchanged heading, and continuation together.
Repeated `FF` at the same starting pose returns
`((0, 0, 1), [False, False])`. Check all remaining contract examples in the
[addendum](OCCUPIED_SPEC.md), retain baseline tests, and use the
[development check](../DEVNOTES.md).

[Baseline evidence](evidence/occupied-baseline.md) verifies only the existing
three tests, not occupancy. No material code feasibility unknown remains after
inspection. Proposed interface/input choices await design review; malformed
occupancy validation is outside this amendment. Routing, persistence, moving
obstacles, and configuration files remain outside scope.
