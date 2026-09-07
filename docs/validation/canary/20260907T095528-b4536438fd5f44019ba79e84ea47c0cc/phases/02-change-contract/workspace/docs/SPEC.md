# Current behavior contract
Authority: [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and the subsequent [confirmed stop request](STOP_REQUEST.md). The stop request
supersedes continuation after a blocked move. Implementation is pending.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

`run(pose, commands, occupied=())` returns final pose and per-attempt outcomes.
Occupied forward targets report False, preserving position and heading immediately
before that command, and stop the batch immediately. Earlier successful moves and
turns remain applied; this is not a rollback to the starting pose. Return outcomes
through the failed command, including its False; omit outcomes for every command
not attempted. Successful commands report True. Turns do not consult occupancy.
Unknown commands raise ValueError only if reached; commands after a blocked F
are not attempted or validated. Fixed occupancy is caller supplied.

Decisive acceptance examples are in [the current design](DESIGN.md#acceptance).
The earlier continuation contract remains recorded in the original occupied-cell
request and [historical D2 acceptance](history/d2-review.md).
