# Navigation behavior

This target contract includes the [confirmed occupied-cell request](OCCUPIED_REQUEST.md).
Implementation status lives in [the plan](PLAN.md#delivery-status). The
[original request](ORIGINAL.md) and [previous specification](history/pre-occupied-documents.md)
are preserved.

The grid is unbounded, with integer coordinates and headings 0, 1, 2, 3 for
north, east, south, west. A caller supplies a pose and commands. Return the final
pose and one Boolean success outcome per processed valid command. L/R turn in
place and succeed. Unknown commands raise ValueError.

The caller may supply fixed occupied cells. F into an occupied cell fails,
reports False for that command, and preserves both position and heading.
Processing continues with the next command. F into a free cell advances one
cell and succeeds. Omitting occupied cells preserves existing behavior.

## Proposed interface defaults

Use an optional third argument, `run(pose, commands, occupied=())`. Supply a finite
iterable of integer `(x, y)` pairs, copied once for the run. Duplicates have no
additional effect. Occupancy applies to forward destinations only: an occupied
starting cell does not invalidate the supplied pose or prevent turns or departure.
No new malformed-input validation is specified. These are design defaults, distinct
from the confirmed collision requirements above.

## Acceptance examples

| Initial pose | Occupied cells | Commands | Final pose | Outcomes |
|---|---|---|---|---|
| (0, 0, 0) | omitted or empty | RF | (1, 0, 1) | [True, True] |
| (0, 0, 0) | {(0, 1)} | FFRF | (1, 0, 1) | [False, False, True, True] |
| (0, 0, 0) | {(0, 1)} | FL | (0, 0, 3) | [False, True] |
| (0, 0, 0) | {(0, 0)} | FRRF | (0, 1, 2) | [True, True, True, False] |
| (0, 0, 3) | {(-1, 0)} | F | (0, 0, 3) | [False] |
| (0, 0, 0) | {(0, 1)} | empty | (0, 0, 0) | [] |

After a blocked F, an unknown command still raises ValueError. Independent runs
do not share occupancy. Routing, persistence, moving obstacles, board boundaries
and configuration files are outside scope.
