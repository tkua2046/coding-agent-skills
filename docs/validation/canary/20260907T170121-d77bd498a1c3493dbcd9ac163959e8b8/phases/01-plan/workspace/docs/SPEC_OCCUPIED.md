# Fixed occupied cells: specification addendum

Status: the behavioral request is confirmed in [OCCUPIED_REQUEST.md](OCCUPIED_REQUEST.md).
The interface and edge defaults below are proposed for design review; this
feature is not implemented. [SPEC.md](SPEC.md) describes the delivered baseline;
the [original requirements](ORIGINAL.md) remain preserved.

## Confirmed behavior

The caller supplies fixed occupied cells. Forward entry into an occupied cell
reports failure, preserves both position and heading, and permits subsequent
commands. Turns still work. No routing, persistence, moving obstacles, or
configuration file is requested. Preserve the baseline unbounded integer grid,
headings, return structure, and unknown-command error behavior.

## Proposed interface defaults

`run(pose, commands, occupied=())` accepts an iterable of `(x, y)` integer tuples.
Occupancy is copied once per run and never mutates the caller's collection.
Omission and an empty collection preserve existing behavior; duplicates have no
additional effect. Each processed valid command yields one Boolean outcome:
blocked forward is `False`, successful forward and turns are `True`.
Starting on an occupied coordinate is permitted; only forward destinations are
checked. Input validation beyond valid coordinate tuples is not specified here.

## Acceptance examples

These expected values are derived from the grid contract, not executed feature
tests. Headings are north=0, east=1, south=2, west=3.

| Pose; commands; occupied cells | Expected return / error | Purpose |
|---|---|---|
| `(0, 0, 1)`; `F`; `{(1, 0)}` | `((0, 0, 1), [False])` | Blocked eastward move preserves full pose. |
| `(0, 0, 1)`; `FRF`; `{(1, 0)}` | `((0, -1, 2), [False, True, True])` | A turn and later free move still execute. |
| `(0, 0, 1)`; `FFL`; `{(1, 0)}` | `((0, 0, 0), [False, False, True])` | Repeated failure does not terminate the session; left turn works. |
| `(0, 0, 0)`; `RF`; omitted or empty | `((1, 0, 1), [True, True])` | Existing calls retain behavior. |
| `(0, 0, 1)`; `F`; `{(0, 0)}` | `((1, 0, 1), [True])` | Proposed starting-cell rule permits leaving. |
| `(0, 0, 1)`; `F?`; `{(1, 0)}` | `ValueError("unknown command")` | Blocking does not hide a later invalid command; no normal return. |

Also verify that an occupied coordinate blocks entry regardless of heading,
changes to the source collection during command iteration do not change the
snapshot, and occupancy from one invocation does not affect another.
