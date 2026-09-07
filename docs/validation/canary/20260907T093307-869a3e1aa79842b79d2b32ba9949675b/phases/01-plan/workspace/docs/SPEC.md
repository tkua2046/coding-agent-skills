# Current specification

Status: occupied-cell behavior confirmed; implementation pending. Sources:
[original request](ORIGINAL.md) and [occupied-cell request](OCCUPIED_REQUEST.md).
The original source documents remain authoritative and unchanged.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances
one cell unless its destination is occupied. Callers may supply fixed occupied
cells. An F into an occupied cell reports failure, preserves both position and
heading, and allows subsequent commands to execute. L/R still turn in place.
Return the final pose and per-command success. Unknown commands raise ValueError.
No routing, persistence, moving obstacles, or configuration file is in scope.

For example, starting at (0, 0, 1) with (1, 0) occupied, F leaves the pose at
(0, 0, 1) and reports False. Continuing with LF turns north and moves to (0, 1, 0),
reporting True for each of those commands.

The optional argument and occupancy ownership choices are proposed in
[the design](DESIGN.md); they are not additional user-confirmed requirements.
Current code still implements unconditional forward movement, as recorded in
[baseline evidence](evidence/occupied-baseline.md).
