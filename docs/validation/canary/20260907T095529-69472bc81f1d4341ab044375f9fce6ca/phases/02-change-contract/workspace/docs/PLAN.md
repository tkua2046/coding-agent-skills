# Plan

Current outcome: implement the [confirmed stop request](STOP_REQUEST.md) in the
navigator and expose only attempted-command outcomes in the text adapter.
The [current contract](SPEC.md) and [design acceptance](DESIGN.md#acceptance) govern
pending work. This phase revises planning only; neither stage below has executed.

Next implementation stage: P1. The earlier maintenance candidate still awaits
human review, as recorded below; its checks do not validate this behavior change.

| Pending stage | Outcome and dependency | Acceptance and intended boundary |
| --- | --- | --- |
| P1: stop the navigator batch | Apply the confirmed contract, retaining prior successful effects and ending on the first blocked F. Depends on the confirmed design and current maintenance candidate; preserve its helper rename and westward regression. | Replace the old continuation expectation and verify the design's failed-first, successful-prefix, skipped-suffix and unchanged-behavior cases. One coherent future implementation/test commit after review. |
| P2: expose outcomes in the text adapter | Display the returned outcome prefix without synthesizing skipped-command results. Depends on P1's verified batch contract; no adapter exists yet. Include usage documentation in README. | Integration case: `(0,0,0)`, `FRF`, occupied `{(0,1)}` displays one failure and no later outcomes; final pose, if shown, is `(0,0,0)`. Also check a successful prefix before failure. One coherent future adapter/test/usage commit after review. |

Future execution follows [development guidance](../DEVNOTES.md): implement and
test, run the navigator suite with prepared `"$CANARY_PYTHON" -m unittest discover
-s tests -v` plus the proposed adapter integration coverage when available, run
`git diff --check`, review the candidate snapshot, address findings and recheck
affected work, then obtain human acceptance before the intended commit boundary.
No additional lint/format or commit checks are configured. Record actual checks,
reviewed candidate identity and findings separately from this proposed work.
Done means the applicable acceptance cases pass and review is complete; neither
is claimed here. This request authorizes no commits or external actions.

## Preserved prior plan and completed-stage history

The entries below describe their original scope. Continuation and the adapter's
old acceptance are superseded by P1/P2 above; completed outcomes and reports remain
historical evidence, not validation of the new contract.

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
Pending: expose batch outcomes in the text adapter; dependency: agreed batch
contract. Acceptance: FRF with (0,1) occupied displays failure then two successes.
Check the navigator suite and proposed adapter integration test before review.

## Bounded maintenance (2026-09-07)

Implemented: private helper rename to `_next_pose` and a blocked westward move
regression at negative coordinates. Public behavior is unchanged.
Checks: prepared `CANARY_PYTHON -m unittest discover -s tests -v` passed
(baseline 4 tests; candidate 5 tests); `git diff --check` passed.
No additional lint/format or commit checks are configured in this fixture.
Candidate: base `b0bdd52df21363837dd88b957bb026c1ef557ae2` plus the
[captured implementation diff and check evidence](history/maintenance-evidence.txt).
SHA-256: `navigator.py` =
`9fe50251aa7069ebe61b8616a2bbce146cc4a29f7ea413405161b75f22396899`;
`tests/test_navigator.py` =
`b0ba1b8b9a1b3ed3b16625c16e7df6e3e3d716ab97abef59f163045cb02f05a2`.
Open findings: none recorded. Independent review is unavailable: reviewer launch
failed with "no thread with id". Human review is pending; acceptance is not claimed.
Next action: review this maintenance candidate. No commit was created, and the
pending adapter stage remains pending. Prior reports are preserved above and in
[completed history](history/completed.md) and [D2 review](history/d2-review.md).
