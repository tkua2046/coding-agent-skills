# Design: fixed occupied cells
Status: occupied-cell extension proposed; implementation has not started. The
[confirmed request](OCCUPIED_REQUEST.md) adds caller-supplied fixed cells to the
existing navigator. Keep D1's local state and direction lookup; check a candidate
forward destination against a run-local set before changing pose. A blocked move
returns False without changing pose, and subsequent commands continue. Deliver this
small local extension in [one pending stage](PLAN.md); no new dependencies are needed.

## Interface and ownership
Proposed signature: `run(pose, commands, occupied=())`, retaining the existing
`(final_pose, outcomes)` return shape and all two-argument calls. Accept an iterable
of `(x, y)` integer tuples and snapshot it as a set once per run, before processing
commands. Duplicates have no effect; caller-owned collections are not mutated.
The snapshot keeps membership fixed during a run, with O(n) setup/storage and
expected O(1) membership checks. Repeated scanning would avoid set storage but
repeat work for every F and complicate support for one-shot iterables.

F computes the candidate with the existing direction lookup. Only an unoccupied
candidate replaces pose. A blocked candidate appends False and continues; successful
F and L/R append True. Turns do not consult occupancy. Unknown commands retain
ValueError behavior. No board bounds or shared session state are introduced.

Proposed input assumption: callers provide valid coordinate tuples, as they already
provide valid poses. No new validation/error taxonomy is needed for malformed cells.
Occupancy is a destination constraint: if the initial position is listed, the run
can turn or leave it; returning into it is blocked. These API/input choices are design
proposals, not additional user-confirmed requirements. No material blocker remains
for the requested forward-move contract.

## Acceptance and validation
Headings remain 0=north, 1=east, 2=south, 3=west.

| Input | Expected return / behavior |
| --- | --- |
| `run((0, 0, 1), "F", {(1, 0)})` | `((0, 0, 1), [False])`: position and heading preserved |
| `run((0, 0, 1), "FFLF", {(1, 0)})` | `((0, 1, 0), [False, False, True, True])`: repeated block, turn, then successful move |
| `run((0, 0, 0), "RF")` with omitted or empty occupancy | `((1, 0, 1), [True, True])`, preserving D1 |
| `run((0, 0, 0), "RF", {(0, 0)})` | `((1, 0, 1), [True, True])`: initial occupancy does not prevent departure |
| `run((0, 0, 1), "F?", {(1, 0)})` | raises ValueError on `?` after processing the blocked F |

Implementation checks should also cover negative-coordinate destinations, both turn
directions, duplicate/iterable input, caller collection preservation, and isolation
between runs. These are proposed checks; [baseline evidence](evidence/occupied-baseline.md)
only verifies the existing movement/turn/error tests. README usage must be updated
when the API is implemented. Operations remain in DEVNOTES; no new operational
procedure is required. Routing, persistence, moving cells, and configuration files
remain outside scope.

## Accepted design D1 (preserved)
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.
