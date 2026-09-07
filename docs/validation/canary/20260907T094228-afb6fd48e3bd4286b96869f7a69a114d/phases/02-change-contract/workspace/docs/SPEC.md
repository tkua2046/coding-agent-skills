# Current confirmed contract
Authority: [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and the subsequent [stop request](STOP_REQUEST.md). The stop request supersedes
continuation after a blocked move. Implementation is pending.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Attempted unknown commands raise ValueError. No persistence or
pathfinding. Occupied cells are fixed and supplied by the caller.

An occupied forward target reports False and immediately stops the batch,
preserving the position and heading immediately before that failed command.
Earlier successful commands remain applied; there is no batch rollback.
Return that pose and outcomes through and including the failed command. Commands
after it are not attempted and have no outcomes (including unknown commands).
Without a blocked move, all commands run under the existing rules.

## Acceptance
Headings 0, 1, 2, 3 are north, east, south, west. Each row is a separate run.

| Initial pose | Commands | Occupied cells | Expected return or error |
| --- | --- | --- | --- |
| (0,0,0) | FRF | {(0,1)} | ((0,0,0), [False]) |
| (0,0,0) | RFFL | {(2,0)} | ((1,0,1), [True, True, False]) |
| (-2,-3,3) | FR | {(-3,-3)} | ((-2,-3,3), [False]) |
| (0,0,0) | RF | {} | ((1,0,1), [True, True]) |
| (2,3,0) | L | {} | ((2,3,3), [True]) |
| (0,0,0) | F? | {(0,1)} | ((0,0,0), [False]); ? is not attempted |
| (0,0,0) | ?F | {(0,1)} | ValueError on ? |

The former continuation contract remains recorded in the original occupied-cell
request and [D2 history](history/d2-review.md).
