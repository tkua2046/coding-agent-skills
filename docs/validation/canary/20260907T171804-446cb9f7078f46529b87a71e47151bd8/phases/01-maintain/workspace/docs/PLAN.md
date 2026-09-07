# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
Pending: expose batch outcomes in the text adapter; dependency: agreed batch
contract. Acceptance: FRF with (0,1) occupied displays failure then two successes.
Check the navigator suite and proposed adapter integration test before review.

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
