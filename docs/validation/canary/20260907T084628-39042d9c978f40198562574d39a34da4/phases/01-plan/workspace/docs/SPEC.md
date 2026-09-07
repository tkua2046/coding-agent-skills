# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed occupied-cell extension — pending implementation

Authority: [confirmed request](OCCUPIED_REQUEST.md); preserve the
[original request](ORIGINAL.md). The paragraph above describes the delivered baseline.

Callers may supply fixed occupied cells. F targeting an occupied cell returns
False for that command and preserves the entire pose, including heading. Later
commands still run. Unblocked moves and turns return True; turns work in place
regardless of occupied cells. Final pose and ordered per-command outcomes retain
their existing return structure. All other baseline behavior remains in force.
Routing, persistence, moving obstacles and configuration files are outside scope.

Decisive example: from `(0, 0, 1)` with occupied cell `(1, 0)`, commands `FRF`
produce `((0, -1, 2), [False, True, True])`: east is blocked, R faces south,
and the next F succeeds. The blocked F alone produces
`((0, 0, 1), [False])`.

The optional argument and input representation are proposed in the
[design amendment](DESIGN.md#occupied-cell-amendment); they are design choices,
not additional caller-confirmed requirements.
