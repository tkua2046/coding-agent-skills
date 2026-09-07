# Current design: stop on blocked forward movement
The [confirmed stop request](STOP_REQUEST.md) changes the batch contract: return
the pose at the first blocked F with outcomes only through that failure. This
revision is planning only; the inspected code and continuation test still implement
D2. Next: implement the navigator change, then update the pending text adapter
under the [plan](PLAN.md). No unresolved behavior decision blocks the navigator.

## Revised failure decision
Retain run-local state, the direction lookup, caller-supplied occupied coordinates
converted to a set, and checking the candidate before assigning pose. On a blocked
F, record False and end the batch immediately. Successful prefix commands retain
their effects; failure preserves both position and heading at the point of failure.
Do not process or validate the remaining commands. Attempted unknown commands
still raise ValueError.

Stopping follows the user's confirmation and replaces D2 continuation. The return
shape stays `(pose, outcomes)`, but callers must now allow fewer outcomes than
input commands. The text adapter must display only attempted-command outcomes.
No new abstraction, dependency, persistence, routing, or board boundary is needed.

For `(0,0,0)`, FRF and occupied `{(0,1)}`, return `((0,0,0), [False])`.
For RFFL and occupied `{(2,0)}`, return `((1,0,1), [True, True, False])`:
the first move and turn remain applied and the final L is never attempted.
The [current acceptance cases](SPEC.md#acceptance) also cover negative coordinates,
unblocked behavior, and unknown commands before versus after a stop.

Validation is proposed: replace the continuation expectation, verify preserved
prefix effects and skipped suffixes, retain movement/turn/error coverage, and
check adapter output against the same contract. Inspection verified that no text
adapter exists in this fixture; its invocation and output format remain to be
specified before that stage. No implementation or new behavioral test run is
claimed by this revision.

## Accepted history (superseded only for continuation)
### Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].
