# Occupied-cell specification addendum

The [original requirements](ORIGINAL.md), [current behavior](SPEC.md), and
[confirmed occupied-cell request](OCCUPIED_REQUEST.md) retain their source text.
Requested behavior below is confirmed; interface choices are proposed by the
[design amendment](DESIGN.md) and have not been accepted or implemented.

## Confirmed behavior

Callers can supply fixed occupied cells. A forward move into one reports failure
and preserves both position and heading. Processing continues, and turns work.
There is no routing, persistence, moving-obstacle, or configuration-file scope.

## Proposed interface clarifications

- Extend the API to `run(pose, commands, occupied=())`; omission or an empty
  iterable preserves existing behavior. Occupied entries are integer `(x, y)`
  tuples, supplied through an iterable and snapshotted before commands execute.
- Keep `(final_pose, outcomes)` as the return shape. Each recognized command adds
  one Boolean; only a blocked forward move adds `False`. Unknown commands still
  raise `ValueError`, including after a blocked move.
- Duplicates have no extra effect. The input collection is not modified, later
  caller mutations do not affect that run, and subsequent calls have no inherited
  occupancy. `None` is not an empty-occupancy alias.
- Occupancy concerns destinations only; an occupied starting cell is allowed.
  No new validation behavior for malformed inputs is specified.

## Acceptance examples

Headings remain north/east/south/west as 0/1/2/3. Examples assume the proposed API.

| Case | Pose; commands; occupied cells | Expected result |
|---|---|---|
| Block preserves pose and heading | `(0, 0, 0)`; `F`; `{(0, 1)}` | `((0, 0, 0), [False])` |
| Repeated failure and continuation | `(0, 0, 0)`; `FFRF`; `{(0, 1)}` | `((1, 0, 1), [False, False, True, True])` |
| Left turn after failure | `(0, 0, 0)`; `FLF`; `{(0, 1)}` | `((-1, 0, 3), [False, True, True])` |
| Negative destination | `(0, 0, 3)`; `F`; `{(-1, 0)}` | `((0, 0, 3), [False])` |
| Compatibility | `(0, 0, 0)`; `RF`; omitted or empty | `((1, 0, 1), [True, True])` |
| Empty commands | `(2, 3, 2)`; empty; `{(2, 3)}` | `((2, 3, 2), [])` |
| Leave occupied start; block re-entry | `(0, 0, 0)`; `FRRF`; `{(0, 0)}` | `((0, 1, 2), [True, True, True, False])` |
| Unknown after failure | `(0, 0, 0)`; `F?`; `{(0, 1)}` | Raises `ValueError` |

Also verify an iterable yielding duplicate `(0, 1)` entries blocks the same way
as a set. For snapshot semantics, use a command iterator that clears the caller's
initial `{(0, 1)}` before yielding `F`: the move still fails. A separate run without
occupied cells succeeds. A normal run leaves the caller's supplied set unchanged.
