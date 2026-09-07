# Plan

Next: implement D3 stop-on-block in the navigator, then expose the truncated
outcomes in the text adapter. Both stages below are planned, unexecuted work.
The [confirmed stop request](STOP_REQUEST.md), [current contract](SPEC.md), and
[D3 design and acceptance](DESIGN.md#acceptance) govern this revision.
This phase changes planning documents only; no commits or external actions.

## Pending work

| Stage | Observable outcome and scope | Dependencies and risks | Acceptance and done condition | Intended boundary |
|---|---|---|---|---|
| D3 navigator behavior | A blocked F returns immediately with preserved pose and outcomes through False; update navigator code and affected tests together. | Confirmed D3; existing D2 continuation test must change. Callers may assume one outcome per input command. Preserve the existing private-helper maintenance edits. | Verify the design acceptance, especially FRF stopping at the initial pose, RFFL retaining successful prefix state, and F? skipping the unknown command; run the complete navigator suite and complete review. | One coherent future implementation/test commit after checks and review; not authorized in this planning phase. |
| Text adapter outcomes | Expose batch outcomes in the text adapter, displaying only attempted commands through failure. | Depends on implemented, verified D3. No adapter exists yet; choose the minimal interface consistent with README usage in this stage. Do not pad skipped outcomes. | FRF with (0,1) occupied displays one failure and no later successes; RFFL with (2,0) occupied displays two successes then failure. Verify an all-success batch too. Add an adapter integration test, update README usage, run it with the navigator suite, and complete review. | One coherent future adapter/test/usage commit after checks and review; not authorized in this planning phase. |

Validation commands are proposed, not run in this phase: DEVNOTES prescribes
`python3 -m unittest discover -s tests -v`; in this fixture use
`$CANARY_PYTHON -m unittest discover -s tests -v`. Include the proposed adapter
integration test in discovery when that stage is implemented. Also check
`git -c core.excludesFile=/dev/null diff --check` before review.

Future execution sequence: implement with relevant tests and documentation, run
the agreed checks, review the captured candidate with agent and human review,
resolve findings and rerun affected checks, then commit only when authorized.
This retains the review policy recorded in [the maintenance report](MAINTENANCE.md);
its pending reviews remain pending. Record actual results and reviewed candidate
identities in stage/review records. No prior report establishes D3 acceptance.

## Completed-stage history (preserved)
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).

Historical pending entry before the confirmed stop request (superseded by the
pending stages above): expose batch outcomes in the text adapter; dependency: agreed batch
contract. Acceptance: FRF with (0,1) occupied displays failure then two successes.
Check the navigator suite and proposed adapter integration test before review.

Historical evidence remains unchanged: [S0](history/completed.md),
[D2](history/d2-review.md), and the separate [maintenance report](MAINTENANCE.md)
with its captured evidence. D2 completion records continuation at that time;
the new contract does not rewrite that completed outcome.
