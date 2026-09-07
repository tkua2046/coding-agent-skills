# Current design: stop on blocked forward movement

Status: behavior confirmed in [STOP_REQUEST.md](STOP_REQUEST.md); implementation
and verification remain pending. Amend batch termination only: retain D1 state
ownership and D2 occupied-set lookup and pose preservation. A blocked F appends
False and ends the batch immediately, returning the pose at that failure and the
attempted outcomes. Next: implement the navigator amendment before the pending
text adapter work in [PLAN.md](PLAN.md).

## Decision and compatibility

The [current contract](SPEC.md) replaces continuation with immediate termination
because the caller confirmed this public behavior change. Keep the same run
arguments and `(pose, outcomes)` return shape; outcomes can now be shorter than
the input commands. Callers, including the text adapter, must not assume one
outcome per supplied command or display successes for commands never attempted.

Keep state local, convert caller-supplied occupied coordinates to a set, and check
the forward target before assigning pose. No rollback of earlier successful
commands is needed. Commands after a blocked F are not processed, including
unknown commands; attempted unknown commands still raise ValueError. No new
dependency, persistence, routing, or configuration is needed.

Inspection verified that navigator.py currently continues on a blocked F and
tests/test_navigator.py expects continuation for FRF. The text adapter is not yet
present. These are implementation gaps, not evidence for the new behavior.

## Acceptance

Inputs below use `run(pose, commands, occupied)`; expected results follow the
confirmed contract and are proposed checks, not test-run results.

| Pose | Commands | Occupied | Expected result |
| --- | --- | --- | --- |
| (0,0,0) | FRF | {(0,1)} | ((0,0,0), [False]); R and final F unattempted |
| (0,0,0) | FRFFL | {(2,1)} | ((1,1,1), [True, True, True, False]); L unattempted, earlier movement retained |
| (-2,-3,3) | FR | {(-3,-3)} | ((-2,-3,3), [False]); position and west heading preserved |
| (0,0,0) | RF | {} | ((1,0,1), [True, True]) |
| (0,0,0) | F? | {(0,1)} | ((0,0,0), [False]); unknown command unattempted |
| (0,0,0) | ? | {} | ValueError |

The adapter must display the returned pose and only attempted outcomes: the first
row displays (0,0,0) and one failure, with no entries for R or the final F.
Validate the amended navigator suite and, once implemented, adapter integration
coverage. No unresolved behavior decision blocks the navigator amendment; adapter
text formatting remains an implementation choice within existing usage conventions.

## Accepted design D1 (preserved)
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Accepted D2 (historical continuation contract)

Continuation below is superseded by the confirmed stop request. The
[D2 review](history/d2-review.md) applies to that earlier contract only.

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].
