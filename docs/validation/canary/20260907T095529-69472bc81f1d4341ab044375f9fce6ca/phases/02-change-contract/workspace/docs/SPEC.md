# Current contract
Confirmed by [the stop request](STOP_REQUEST.md); implementation is pending.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Attempted unknown commands raise ValueError. No persistence or
pathfinding. Occupied cells are fixed and supplied by the caller.

An occupied forward target reports False and immediately stops the command batch.
Return the pose immediately before that failed command (position and heading
unchanged) and outcomes for all attempted commands, including the failed F.
Earlier successful commands retain their effects. Do not attempt remaining
commands or include outcomes for them. Successful commands report True; batches
without a blocked move retain their existing behavior.

This supersedes continuation in the preserved [occupied-cell request](OCCUPIED_REQUEST.md)
and historical D2 acceptance. The [original request](ORIGINAL.md) remains preserved.
Concrete acceptance cases are in [the current design](DESIGN.md#acceptance).
