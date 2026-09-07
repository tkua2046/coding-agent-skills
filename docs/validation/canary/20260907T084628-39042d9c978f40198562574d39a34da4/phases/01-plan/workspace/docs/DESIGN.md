# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment

Status: proposed design for the [confirmed extension](SPEC.md#confirmed-occupied-cell-extension--pending-implementation);
implementation has not begun. Keep D1 and add a per-run occupied-coordinate set.
A blocked F yields False without changing pose; remaining commands execute.
Existing two-argument callers retain their behavior. Next step: the single pending
[implementation stage](PLAN.md#pending-stage-s1). This local change needs no new
abstraction or dependency.

### Interface and state

Propose `run(pose, commands, occupied=())`, accepting a finite iterable of integer
coordinate pairs represented as `(x, y)` tuples. Snapshot it into a local set once
at entry; duplicates have no effect. This supplies expected constant-time lookup
per F at O(n) construction time and O(u) space for u unique cells. Scanning the
caller's collection on every move is simpler in storage but costs O(n) per F and
can observe caller mutation; the snapshot fits fixed occupancy and local ownership.
Never mutate the caller's collection or retain it between runs.

Inspect `_target(pose)`'s candidate coordinates before assigning pose. Occupancy
compares `(x, y)`, independent of heading. Only a blocked F appends False; turns
and successful translations append True. Unknown commands still raise ValueError,
including after a blocked move. Each valid command has exactly one outcome.

The baseline does not validate pose inputs. This amendment assumes valid poses
and coordinate tuples and adds no coercion or specified malformed-occupancy error
contract. The target-only rule does not reject a starting pose on an occupied cell:
turning and departure to a free cell remain possible. These are proposed boundary
choices; no material decision blocks planning. Infinite iterables, concurrency,
dynamic occupancy and new input formats are outside this design.

### Acceptance and validation

Hand-derived examples (north increases y; east increases x):

| Initial pose / occupied / commands | Expected result |
|---|---|
| `(0, 0, 1)` / `{(1, 0)}` / `F` | `((0, 0, 1), [False])` |
| `(0, 0, 1)` / `{(1, 0)}` / `FRF` | `((0, -1, 2), [False, True, True])` |
| `(0, 0, 1)` / `{(1, 0)}` / `FFL` | `((0, 0, 0), [False, False, True])` |
| `(0, 0, 0)` / `{(0, 0)}` / `RF` | `((1, 0, 1), [True, True])` |
| `(0, 0, 3)` / `{(-1, 0)}` / `F` | `((0, 0, 3), [False])` |
| `(0, 0, 1)` / `{(1, 0)}` / `F?` | `ValueError`; no normal result |

Verify omitted and empty occupancy preserve baseline behavior, empty commands
return the starting pose with no outcomes, and blocking works in every heading.
Check duplicate and iterable input, caller collection preservation, and separate
runs with different occupancy to guard against state leakage.

Inspection found that `_target` already computes a candidate without mutation;
`run` currently assigns it unconditionally and appends True for every valid command.
The three existing tests cover basic movement, left wrap and unknown commands,
but no obstacle behavior. They passed in this phase; see
[baseline evidence](evidence/occupied-baseline.md). All extension checks above
remain proposed. D1's historical acceptance does not cover this amendment.
