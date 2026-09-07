# Current contract
Authority: [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and subsequent [confirmed stop request](STOP_REQUEST.md). Stop behavior is confirmed;
implementation is pending. Earlier continuation semantics remain historical.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Attempted unknown commands raise ValueError. No persistence or
pathfinding. The caller supplies fixed occupied cells.

An occupied forward target reports False, preserves position and heading immediately
before that command, and stops the batch immediately. Return that pose and the
outcomes through the failed command, including earlier successes. Do not attempt
remaining commands or emit outcomes for them. Earlier successful moves are retained;
there is no batch rollback. Successful commands report True as before.

## Acceptance

Each result below is `(final_pose, outcomes)` from `run(pose, commands, occupied)`.

| Initial pose | Commands | Occupied cells | Expected result or error |
|---|---|---|---|
| `(0, 0, 0)` | `FRF` | `{(0, 1)}` | `((0, 0, 0), [False])`; R and final F are unattempted |
| `(0, 0, 0)` | `RFFL` | `{(2, 0)}` | `((1, 0, 1), [True, True, False])`; L is unattempted |
| `(-2, -3, 3)` | `FR` | `{(-3, -3)}` | `((-2, -3, 3), [False])` |
| `(0, 0, 0)` | `RF` | `{}` | `((1, 0, 1), [True, True])` |
| `(0, 0, 0)` | empty | `{}` | `((0, 0, 0), [])` |
| `(0, 0, 0)` | `?` | `{}` | raises `ValueError` |
| `(0, 0, 0)` | `F?` | `{(0, 1)}` | `((0, 0, 0), [False])`; unknown command is unattempted |
