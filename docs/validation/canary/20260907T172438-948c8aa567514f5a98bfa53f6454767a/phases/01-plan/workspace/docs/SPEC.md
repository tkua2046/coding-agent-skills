# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed extension: occupied cells (pending implementation)
Authority: [confirmed request](OCCUPIED_REQUEST.md); the [original request](ORIGINAL.md)
remains unchanged. Callers can supply fixed occupied cells. F into an occupied
cell returns a failure outcome and preserves both position and heading. Processing
continues with the next command. L/R still turn in place. No routing, persistence,
moving obstacles, or configuration file is included.

The existing final-pose/per-command-success return contract continues: a blocked
F contributes False; successful moves and turns contribute True. Unknown commands
still raise ValueError. With no occupied cells, existing behavior is preserved.
The proposed API and acceptance examples are in [the design](DESIGN.md).
