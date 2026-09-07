# Plan
Current outcome: a blocked F ends the batch, preserves the pose at failure, and
returns only the attempted prefix of outcomes. The [stop request](STOP_REQUEST.md),
[current contract and acceptance](SPEC.md), and [revised design](DESIGN.md) govern
pending work. This revision is planning only; no stage below has been executed.

## Pending work
Next implementation outcome is P1. The maintenance candidate's independent and
human reviews remain pending as recorded below; its checks do not verify the new
contract. Keep that candidate and its frozen evidence distinct from future changes.

| Stage | Observable outcome and scope | Dependencies and acceptance | Done / proposed commit boundary |
| --- | --- | --- | --- |
| P1: stop blocked batches | Update navigator behavior and affected regression expectations together. Retain successful prefix effects and omit every unattempted suffix outcome. | Confirmed stop contract; no open behavior decision. Verify the SPEC acceptance cases, especially FRF, a successful prefix before failure, and an unknown command after failure. Preserve ordinary movement, turning and attempted-error coverage. | Implementation and relevant tests pass checks and review; one coherent navigator commit in the later implementation phase. |
| P2: expose outcomes in text adapter (existing pending stage, revised) | Display only attempted-command outcomes through the first failure. Update README usage with the delivered adapter. | Depends on P1. No adapter exists yet; settle invocation/output format before implementing it. FRF with (0,1) occupied displays one failure and no successes; RFFL with (2,0) occupied displays two successes then failure and nothing for L. | Adapter integration acceptance and navigator regression checks pass review; one coherent adapter commit in the later implementation phase. |

Follow [development guidance](../DEVNOTES.md): implement/test, run the navigator
suite with `"$CANARY_PYTHON" -m unittest discover -s tests -v` and `git diff --check`,
then independent and human review of the candidate, fixes and affected rechecks
before any later commit. Adapter integration checks are proposed, not existing.
Record actual results and reviewed candidate identity separately; prior maintenance
checks and historical acceptance do not establish acceptance of P1 or P2. No commits
or external actions belong to this planning phase.

## Prior progress and pending-work baseline (historical)
The continuation acceptance and adapter expectation below describe the pre-stop
baseline; P1/P2 above replace that pending scope. Completed history and prior
reports are retained unchanged.

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
Pending: expose batch outcomes in the text adapter; dependency: agreed batch
contract. Acceptance: FRF with (0,1) occupied displays failure then two successes.
Check the navigator suite and proposed adapter integration test before review.

## Bounded maintenance (2026-09-07)
Implemented: private helper rename and regression coverage for a blocked westward
move at a negative coordinate; public behavior unchanged. Checks passed: baseline
4 tests, current 5 tests (`"$CANARY_PYTHON" -m unittest discover -s tests -v`),
and `git diff --check`. [Evidence and frozen implementation diff](history/maintenance-checks.txt)
identify the candidate by base commit and file SHA256 hashes.

Next action: independent and human review of this maintenance candidate; neither
review is complete and acceptance remains pending. Independent review was attempted
but the agent tool failed with “no thread with id”; author inspection found no
issues (not independent review). Open finding IDs: none. No commit created.
The pending adapter stage has not advanced. Prior records remain available:
[S0](history/completed.md), [D2](history/d2-review.md).
