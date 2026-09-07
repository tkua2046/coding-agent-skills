# Current design: stop on blocked forward movement

The [confirmed stop request](STOP_REQUEST.md) changes the batch contract: a blocked
F preserves the current pose, appends False, and ends the batch immediately.
Only attempted commands produce outcomes. This is a planning revision; code and
tests still implement D2 continuation. Next: implement and verify the navigator
change, then update the pending text adapter as described in [the plan](PLAN.md).

## Decision and consequences

Retain D1 state ownership, direction lookup and unbounded coordinates, and D2's
occupied-coordinate set and check before assigning pose. Change only batch
termination on a blocked F. Earlier successful moves and turns remain applied;
there is no batch rollback. No new dependency or abstraction is needed.

The public return shape remains `(pose, outcomes)`, but outcomes can now be shorter
than the supplied commands. Callers and the pending adapter must use the returned
prefix without inventing outcomes for skipped commands. Continuation was previously
accepted but is superseded by the user's confirmation. Unknown commands still
raise ValueError when attempted; an unknown command after the stopping failure is
not attempted and does not raise.

## Acceptance

Inputs use `run(pose, commands, occupied)`; outputs are `(pose, outcomes)`.

| Pose | Commands | Occupied | Expected result |
| --- | --- | --- | --- |
| `(0,0,0)` | `FRF` | `{(0,1)}` | `((0,0,0), [False])`; neither R nor the final F runs |
| `(0,0,0)` | `RFFL` | `{(2,0)}` | `((1,0,1), [True, True, False])`; retain prior movement and turn, omit L |
| `(-2,-3,3)` | `F` | `{(-3,-3)}` | `((-2,-3,3), [False])`; preserve position and heading |
| `(0,0,0)` | `RF` | `{}` | `((1,0,1), [True, True])`; unblocked behavior unchanged |
| `(0,0,0)` | empty | `{}` | `((0,0,0), [])` |
| `(0,0,0)` | `?` | `{}` | raises ValueError |
| `(0,0,0)` | `F?` | `{(0,1)}` | `((0,0,0), [False])`; no error from the unattempted suffix |

Adapter acceptance: the blocked `FRF` case displays only the failure, with no
successes or placeholders for the skipped commands. If displaying final pose,
it uses `(0,0,0)`.

## Validation and status

Inspection verified that `navigator.py` currently continues after a blocked move,
and `tests/test_navigator.py` explicitly expects that continuation. The existing
westward regression remains valid. No text adapter exists in this fixture yet.
Future validation will replace the continuation expectation, cover the cases
above and verify the adapter's truncated output. No implementation or runtime
verification of the new behavior occurred in this planning phase. No unresolved
contract decision blocks implementation; adapter presentation follows README's
usage ownership when implemented.

## Preserved accepted history (superseded only for continuation)

### Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].
