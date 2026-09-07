# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed occupied-cell extension (pending implementation)

Authority: [original request](ORIGINAL.md) and [confirmed extension](OCCUPIED_REQUEST.md).
The paragraph above describes the implemented baseline; this extension is confirmed
behavior to deliver, not a claim that the code already supports it.

The caller supplies fixed occupied cells. An F whose destination is occupied
returns failure for that command, preserves position and heading, and allows the
remaining commands to execute. L and R continue to turn in place successfully.
There is no routing, persistence, moving-obstacle support or configuration file.
Final pose and per-command outcomes remain the return contract; unknown commands
still raise ValueError.

For example, from (0, 0, 1), with occupied cell (1, 0), F returns
((0, 0, 1), [False]). With the same inputs, FRF returns
((0, -1, 2), [False, True, True]): the blocked eastward move does not prevent
turning south and moving. With no occupied cells, existing behavior is preserved.

The optional API argument, lookup representation and valid-input conventions are
proposed engineering choices in [the design amendment](DESIGN.md#occupied-cell-amendment),
not additional caller-confirmed requirements.
