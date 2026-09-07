# Occupied-cell specification addendum

Status: request requirements confirmed; interface decisions proposed, design
review pending. The unchanged [original request](ORIGINAL.md), [current baseline
specification](SPEC.md), and [occupied-cell request](OCCUPIED_REQUEST.md) remain
the source texts. This addendum describes the intended extension, not shipped behavior.

## Confirmed behavior

- Callers supply fixed occupied cells. Forward entry into one reports command
  failure and preserves position and heading.
- The same run continues with later commands; turns still work.
- No routing, persistence, moving obstacles, or configuration file support.
- Preserve the original unbounded grid, heading conventions, result shape, and
  unknown-command `ValueError` behavior.

## Proposed interface decisions

Use `run(pose, commands, occupied=())`; omission means no occupied cells. Accept
an iterable of integer coordinate tuples, including a one-shot iterable; snapshot
it at run entry without mutating caller data. Duplicate coordinates have no
additional effect. No special validation/error contract for malformed occupancy
is introduced. Existing pose/command validation behavior is unchanged.

Only a forward destination is tested. An initially occupied position does not
reject the run or prevent departure and turns. This resolves an unspecified edge
case consistently with the request's entry rule; it remains a proposed decision.
Separate calls have independent occupancy and pose state.

## Acceptance examples

These expected values are derived from north/east/south/west headings, not from
executing an obstacle implementation. Each result is `(final_pose, outcomes)`.

| Initial pose | Commands | Occupied cells | Expected result |
|---|---|---|---|
| `(0, 0, 1)` | `FRF` | `{(1, 0)}` | `((0, -1, 2), [False, True, True])` |
| `(0, 0, 1)` | `FF` | `{(1, 0)}` | `((0, 0, 1), [False, False])` |
| `(0, 0, 0)` | `RF` | omitted or empty | `((1, 0, 1), [True, True])` |
| `(0, 0, 0)` | `LRF` | `{(0, 0)}` | `((0, 1, 0), [True, True, True])` |
| `(-1, -1, 3)` | `F` | `{(-2, -1)}` | `((-1, -1, 3), [False])` |
| `(0, 0, 1)` | empty | `{(1, 0)}` | `((0, 0, 1), [])` |
| `(0, 0, 1)` | `F?` | `{(1, 0)}` | raises `ValueError` at `?`; no normal return |

Also verify a one-shot iterable containing duplicate `(1, 0)` coordinates behaves
like the set in the repeated-block example, caller collections remain unchanged,
and a following run without occupancy can move into `(1, 0)`.
