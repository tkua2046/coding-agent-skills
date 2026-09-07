# Plan

Current outcome: stop the batch on the first blocked F, preserve the pose at that
failure, and return outcomes only through its False. Then expose those outcomes in
the text adapter. Authority: [current contract](SPEC.md),
[design and acceptance](DESIGN.md#acceptance), and [confirmation](STOP_REQUEST.md).
This revision is planning only; all stages below remain pending.

## Pending delivery

| Order | Outcome and scope | Dependencies and acceptance | Done / intended boundary |
|---|---|---|---|
| 1 | Implement stop-on-block in the navigator and update affected regression coverage and usage documentation. | Confirmed stop contract; reconcile the existing uncommitted maintenance candidate before taking the implementation snapshot. Verify the design examples: immediate failure, successful prefix retained, negative coordinates, unattempted unknown suffix, attempted unknown error, and unaffected movement/turns. | Core behavior and relevant suite pass; reviewed snapshot and findings recorded under the review policy below. One coherent core code/test/documentation commit proposed for the later implementation phase. |
| 2 | Expose attempted-command outcomes in the text adapter. | Depends on stage 1's stop contract. FRF with (0,1) occupied displays one failure, omits both later outcomes, and preserves (0,0,0) if pose is displayed. Also verify successful prefixes and unobstructed batches through adapter integration coverage. | Navigator suite and adapter integration checks pass; reviewed snapshot recorded. One coherent adapter code/test/usage commit proposed for the later implementation phase. |

The pending adapter acceptance formerly expected failure then two successes. That
expectation is superseded; adapter implementation has not begun. No adapter exists
in the inspected fixture, so its usage surface must be defined when that stage is
implemented. The compatibility risk is callers assuming one outcome per input
command; usage documentation belongs in README.

For later implementation, follow [repository guidance](../AGENTS.md): implement
and test, run agreed checks, review the exact snapshot, fix and recheck affected
work, then commit only within that phase's authorization. Preserve the existing
independent and human review expectations; no new review or acceptance is claimed
here. Proposed checks: `"$CANARY_PYTHON" -m unittest discover -s tests -v` and
`git diff --check`, plus the adapter integration coverage in stage 2. Record actual
results and review identity separately. Prior maintenance checks establish only
that candidate's prior behavior, not the changed stop contract.

## Completed stages (historical)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
These completed outcomes are retained as history; the new request supersedes D2's
continuation contract without changing its historical acceptance. See the
[S0 record](history/completed.md) and [D2 review](history/d2-review.md).

## Prior maintenance report (preserved)

The following report describes the existing candidate before this planning
revision. Its next action concerns that candidate's review; the current feature
sequence is listed above. Its reported checks are not stop-behavior validation.

## Bounded maintenance: private helper rename

Implemented `_target` → `_next_pose` and a regression for a blocked westward
forward move from a negative coordinate. Public behavior is unchanged.
Candidate: base `461f20bffa3f4d8a5de62496c20095f3c49e727c` plus
[code/test diff](history/maintenance-next-pose.patch).

Checks: `"$CANARY_PYTHON" -m unittest discover -s tests -v` passed before
editing (4 tests) and on the candidate (5 tests). `git diff --check` passed.
No additional lint/format gate is configured in this fixture. Git emitted
sandbox cache warnings but returned success for diff operations.

Author inspection found no open findings. Independent and human review are
pending; no stage acceptance is claimed. Next action: review the candidate.
No commit was created; the pending adapter stage has not advanced.
Prior [S0 record](history/completed.md) and [D2 review](history/d2-review.md)
remain unchanged.
