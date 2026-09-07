# Navigator design

Current amendment D3: the [confirmed stop request](STOP_REQUEST.md) changes a
blocked F to stop the batch with unchanged pose and outcomes through that failure.
Requirement confirmed; implementation and verification pending. D1 and occupancy
lookup from D2 remain in force. Callers must now allow fewer outcomes than commands.
Next: implement and verify D3 before the pending text adapter work in
[the plan](PLAN.md).

## Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Accepted D2 history
Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].

This continuation decision and example describe the previously accepted version,
preserved with [its review](history/d2-review.md); D3 supersedes them for current
behavior. The set lookup and check-before-assignment remain current.

## Current amendment D3

**Decision:** append False for a blocked F and end command processing immediately.
**Reason:** the user explicitly confirmed stop-on-block in STOP_REQUEST.md.
**Consequence:** preserve the pose immediately before failure, retain prior
successes, and return only attempted-command outcomes. The alternative, continuing
with later turns and moves, was accepted in D2 but is now superseded.
**Example:** from (0,0,0), FRF with (0,1) occupied returns
((0,0,0), [False]); neither R nor the final F runs.

The public signature and return shape stay unchanged; outcome length and final
pose change for batches with commands after a block. The current implementation
uses `continue`, and the existing FRF test expects D2, so both need updating.
The text adapter must display the returned outcomes without padding or attempting
the remaining commands. No adapter implementation is present in this fixture.

State remains local to each run. Occupancy remains a set copied from caller input;
blocked movement never assigns its candidate pose. Successful prefix state is
retained. Unknown commands reached before any block still raise ValueError;
an unknown command after a block is unattempted and cannot raise. No routing,
persistence, moving obstacles, configuration, or new public API is introduced.

## Acceptance

All expected results below are the confirmed contract, not newly verified results.

| Start pose | Commands | Occupied | Expected return or error |
|---|---|---|---|
| (0,0,0) | FRF | {(0,1)} | ((0,0,0), [False]) |
| (0,0,0) | RFFL | {(2,0)} | ((1,0,1), [True, True, False]); L is unattempted |
| (-2,-3,3) | F | {(-3,-3)} | ((-2,-3,3), [False]) |
| (0,0,0) | RF | {} | ((1,0,1), [True, True]) |
| (2,3,0) | L | {(2,3)} | ((2,3,3), [True]) |
| (0,0,0) | empty | {} | ((0,0,0), []) |
| (0,0,0) | ?F | {(0,1)} | ValueError at ? |
| (0,0,0) | F? | {(0,1)} | ((0,0,0), [False]); ? is unattempted |

## Validation and status

Proposed validation: replace continuation acceptance with stop acceptance, cover
successful prefixes and skipped suffixes, and retain unaffected movement, turning,
unknown-command, and negative-coordinate checks. Run the navigator suite and,
when the adapter exists, verify it displays only attempted-command outcomes.
Code and tests were inspected during planning; no implementation or test execution
is claimed. No behavior decision remains open for D3. Adapter presentation details
remain for its pending stage. Prior maintenance evidence in
[MAINTENANCE.md](MAINTENANCE.md) describes its captured D2 candidate and does not
verify this amendment.
