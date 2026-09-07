# Navigation design: occupied-cell amendment to D1

Add optional caller-supplied occupied coordinates to each run. Snapshot them once
and reject a forward target before assigning the new pose, returning `False` for
that command and continuing the run. This preserves position and heading on a
blocked move and keeps obstacle state local. From `(0, 0, 0)` with `{(0, 1)}`
occupied, `FRF` returns `((1, 0, 1), [False, True, True])`.

Decision: D1 remains accepted; this local amendment is proposed. Behavior is
confirmed by [the request](OCCUPIED_REQUEST.md); interface and edge semantics are
proposed in the [specification addendum](SPEC_OCCUPIED.md).
[Delivery and review status](PLAN.md) owns pending work. The original
[accepted D1 text](history/design-d1.md) is preserved verbatim.

## Approach and consequences

Propose `run(pose, commands, occupied=())`, accepting an iterable of integer
coordinate pairs. Existing two-argument calls retain their behavior and return
shape. Use a per-run immutable set snapshot: duplicates collapse, generators work,
and caller mutations during command processing cannot change the fixed cells.
This costs O(k) setup time and storage for k supplied cells and provides expected
constant-time membership checks. A live caller collection would allow changes
during a run; no new board or session abstraction is needed.

Use the existing direction lookup to compute the candidate pose. Check only its
coordinate pair; assign it only if unoccupied. A blocked forward command contributes
exactly one `False`. Successful forward moves and turns contribute `True`; turns
ignore occupancy. Unknown commands still raise `ValueError`. Occupied cells never
carry state between calls, and the caller's collection is not modified.

Only the destination is checked. Starting on an occupied cell is allowed: turns
and movement out still work, but re-entry is blocked. No new pose, coordinate, or
heading validation framework is proposed; valid occupied entries are hashable
integer `(x, y)` tuples. Malformed inputs are outside this addition's contract.

Unbounded coordinates, local state, heading conventions, and programmer-error
handling from D1 remain unchanged. Routing, persistence, moving obstacles, and
configuration files are out of scope.

## Repository grounding and acceptance

[`navigator.py`](../navigator.py) currently advances every `F` through `_target`
and appends `True` for all recognized commands. The extension needs a guarded
forward update and a failed-command outcome without stopping the loop.
[`tests/test_navigator.py`](../tests/test_navigator.py) covers a turn followed by
forward movement, left wraparound, and unknown-command rejection. The addendum
defines acceptance examples for the implementation stage. Actual baseline results
are recorded only in the [plan status](PLAN.md#current-status).
