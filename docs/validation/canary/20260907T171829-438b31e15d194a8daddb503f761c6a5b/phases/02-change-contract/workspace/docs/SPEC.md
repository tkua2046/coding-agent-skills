# Current behavior contract
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.
The caller supplies fixed occupied cells. An occupied forward target reports False,
preserves the pose immediately before that command, and stops the batch immediately.
Return that pose and outcomes through the failed command, including its False.
Earlier successful moves and turns remain applied. Do not attempt remaining commands
or emit outcomes for them; an unknown command in that unattempted suffix does not
raise. An attempted unknown command still raises ValueError.

Unblocked moves and turns report True. With no block, all commands are processed;
an empty batch returns the supplied pose and an empty outcome list. A later run can
accept commands normally; a blocked batch does not create persistent stopped state.

## Acceptance examples

| Initial pose | Commands | Occupied cells | Returned pose | Outcomes |
|---|---|---|---|---|
| (0,0,0) | FRF | {(0,1)} | (0,0,0) | [False] |
| (0,0,0) | RFFL | {(2,0)} | (1,0,1) | [True, True, False] |
| (0,0,0) | F? | {(0,1)} | (0,0,0) | [False] |
| (0,0,0) | RF | {(0,1)} | (1,0,1) | [True, True] |
| (-2,-3,3) | F | {(-3,-3)} | (-2,-3,3) | [False] |

An attempted `?` raises ValueError. After the first example, a new run from the
returned pose with `RF` and the same occupied cells returns (1,0,1), [True, True].

Sources: [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and [confirmed stop request](STOP_REQUEST.md). The stop request supersedes prior
continuation behavior. [Prior D2 artifacts](history/d2-artifacts.md) preserve that
history. Implementation and validation status live in [the plan](PLAN.md).
