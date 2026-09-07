# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed extension: occupied cells (pending implementation)

Authority: [original request](ORIGINAL.md) and preserved
[confirmed occupied-cell request](OCCUPIED_REQUEST.md). The paragraph above
describes the implemented baseline; the following behavior is required next.

- Callers can supply fixed occupied cells.
- F into an occupied cell reports failure, preserving position and heading.
  The session continues accepting subsequent commands.
- Turns still work. Free forward moves retain existing behavior.
- Routing, persistence, moving obstacles and configuration files are out of scope.

Acceptance: starting at (0, 0, east), with (1, 0) occupied, F fails and leaves
(0, 0, east). A following L succeeds, then F succeeds to (0, 1, north).
The combined outcomes are [False, True, True].

The optional argument, collection ownership and edge-case defaults are proposed
engineering decisions in [the design](DESIGN.md#occupied-cell-amendment-d2);
they are not additional confirmed user requirements.
