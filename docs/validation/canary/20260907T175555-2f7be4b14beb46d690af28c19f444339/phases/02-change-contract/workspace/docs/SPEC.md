# Current contract
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.
Occupied forward targets report False, preserving position and heading immediately
before that command, and stop the batch immediately. Return that pose and outcomes
for attempted commands through the failed F, inclusive. Do not execute remaining
commands or include outcomes for them. Earlier successful moves and turns remain
in effect; stopping does not roll back the batch. Successful commands report True.
Unknown commands raise ValueError when reached; commands after a blocked F are not
reached or validated. A subsequent caller invocation can supply another batch.

This contract follows the [confirmed stop request](STOP_REQUEST.md), superseding
only continuation in the [occupied-cell request](OCCUPIED_REQUEST.md). The
[original request](ORIGINAL.md) and unrelated behavior remain authoritative.
The [previous contract](history/spec-before-stop.md) is historical; implementation
status is tracked in [the plan](PLAN.md).

## Acceptance examples

Inputs are start pose, commands, and occupied coordinates; results are final pose
and outcomes. These expectations apply to the pending implementation.

| Start | Commands | Occupied | Result |
|---|---|---|---|
| (0,0,0) | FRF | {(0,1)} | ((0,0,0), [False]) |
| (0,0,0) | RFFL | {(2,0)} | ((1,0,1), [True, True, False]) |
| (-2,-3,3) | FRF | {(-3,-3)} | ((-2,-3,3), [False]) |
| (0,0,0) | RF | {} | ((1,0,1), [True, True]) |
| (2,3,0) | L | {} | ((2,3,3), [True]) |
| (0,0,0) | empty | {(0,1)} | ((0,0,0), []) |
| (0,0,0) | F? | {(0,1)} | ((0,0,0), [False]); suffix is unattempted |
| (0,0,0) | ? | {} | ValueError |

After the first example, a new run from (0,0,0) with RF and the same occupied
coordinates returns ((1,0,1), [True, True]); the stop is local to one batch.
