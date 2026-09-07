# Current design: stop on blocked forward movement

The [confirmed request](STOP_REQUEST.md) changes the [current contract](SPEC.md):
a blocked F preserves the current pose, appends False and immediately ends the
batch. Return only attempted-command outcomes. This local amendment is planned,
not implemented or newly accepted. Next: implement and verify the core contract,
then expose it in the text adapter, as ordered in the [plan](PLAN.md).

## Decision and consequences

Retain D1's local state and direction lookup and D2's occupied-coordinate set and
check before pose assignment. End iteration at the first blocked F. Preserve prior
successful effects; this is not a rollback to the batch's starting pose. No new
abstraction or dependency is needed. Unaffected movement, turns, and attempted
unknown-command errors retain their behavior.

Continuation was the accepted D2 behavior; the confirmed request now requires
stopping. This public compatibility change means outcomes can be shorter than the
input commands. Callers and the pending text adapter must report only the attempted
prefix, including its final failure, without synthesizing results for the suffix.
Later commands, including unknown commands, must not be processed or validated.

## Acceptance

Inputs below call `run(pose, commands, occupied)`; outputs are `(pose, outcomes)`.

| Pose | Commands | Occupied | Expected result |
|---|---|---|---|
| (0,0,0) | FRF | {(0,1)} | ((0,0,0), [False]) |
| (0,0,0) | FRFFL | {(2,1)} | ((1,1,1), [True, True, True, False]) |
| (-2,-3,3) | FR | {(-3,-3)} | ((-2,-3,3), [False]) |
| (0,0,0) | F? | {(0,1)} | ((0,0,0), [False]); no error |
| (0,0,0) | ? | {} | raises ValueError |
| (0,0,0) | RF | {} | ((1,0,1), [True, True]) |
| (2,3,0) | L | {} | ((2,3,3), [True]) |
| (0,0,0) | empty | {} | ((0,0,0), []) |

The text adapter must display just one failure for the first case, no results for
R or the later F, and the unchanged pose if it displays pose.

## Validation and status

Inspection confirms `navigator.py` still continues after a block and
`tests/test_navigator.py` still asserts D2's FRF result. The negative-coordinate
single-block regression remains valid. No adapter exists in this fixture yet.
The examples above are proposed acceptance checks, not executed results. Update
core regressions and add adapter integration coverage during their respective
stages. No material design question remains open for the confirmed stop behavior.

## Accepted history (prior contract)

### Accepted design D1

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].

That continuation decision and example are historical, superseded by the stop
request above. The [D2 review](history/d2-review.md) remains evidence only for its
original reviewed behavior.
