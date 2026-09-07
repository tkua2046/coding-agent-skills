# Occupied-cell specification addendum

Status: occupied-cell behavior confirmed by [the original feature request](OCCUPIED_REQUEST.md);
interface conventions below proposed, review pending. This addendum describes
future behavior, not the current implementation. Preserve [original requirements](ORIGINAL.md)
and [current baseline behavior](SPEC.md).

Fixed cells supplied by the caller block a forward move whose destination is
occupied. That command reports failure, preserves position and heading, and does
not prevent subsequent commands. Turns continue to work. Coordinates remain
unbounded; routing, persistence, moving obstacles and configuration files are out
of scope. Existing command meanings and unknown-command errors remain in force.

## Proposed interface conventions

- Extend the entrypoint to `run(pose, commands, occupied=())`. Occupancy is an
  iterable of `(x, y)` integer tuples; omission means no occupied cells. The return
  remains `(final_pose, outcomes)`, with one boolean per valid processed command:
  `False` for blocked forward movement, `True` for free movement or a turn.
- Occupancy is fixed from a snapshot taken before command iteration. Duplicate
  cells have no additional effect. Caller collections are not modified, and no
  occupancy carries over to another call.
- Occupying the initial position is allowed: only forward destinations are
  checked. No additional guarantees for malformed occupancy input are introduced.

These are design proposals applying the confirmed requirement to the current API;
they are not recorded user clarifications. There are no additional user decisions
needed to draft the plan; their review remains pending.

## Acceptance examples

Expected results are derived from north/east/south/west headings `0/1/2/3`, not
from a new implementation. Each row is a separate run unless stated otherwise.

| Start | Commands | Occupied | Expected result / behavior |
|---|---|---|---|
| `(0, 0, 1)` | `F` | `{(1, 0)}` | `((0, 0, 1), [False])`; both position and heading unchanged |
| `(0, 0, 1)` | `FLF` | `{(1, 0)}` | `((0, 1, 0), [False, True, True])`; turn and move after failure |
| `(0, 0, 1)` | `FF` | `{(1, 0)}` | `((0, 0, 1), [False, False])`; repeated failure continues |
| `(0, 0, 0)` | `RF` | omitted or empty | `((1, 0, 1), [True, True])`; existing callers preserved |
| `(-2, -3, 2)` | `F` | `{(-2, -4)}` | `((-2, -3, 2), [False])`; negative cells are valid |
| `(0, 0, 0)` | `LRF` | `{(0, 0)}` | `((0, 1, 0), [True, True, True])`; proposed initial-cell convention |
| `(0, 0, 1)` | `F?` | `{(1, 0)}` | `ValueError("unknown command")`; no partial return |
| `(2, 3, 0)` | empty | `{(2, 4)}` | `((2, 3, 0), [])` |

Also verify that duplicate coordinates supplied through a one-shot iterable block
the same destination; the caller's collection remains unchanged; a command
generator changing the source collection after iteration begins does not alter
the snapshot; and a later call with omitted occupancy can enter a previously
blocked cell. Exercise all four heading/destination pairs to cover the shared
blocked-pose invariant.
