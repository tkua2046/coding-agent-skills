# Plan
Status: planning only; D3 implementation and adapter delivery remain pending.
Next: implement stop-on-block in the navigator against the confirmed
[current contract](SPEC.md) and [D3 design](DESIGN.md#d3-stop-on-block), sourced from
the [stop request](STOP_REQUEST.md).

## Completed history

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
These completed outcomes remain historical; see [S0](history/completed.md) and
[D2 review](history/d2-review.md). The former pending adapter acceptance displayed
failure then two successes for FRF with (0,1) occupied; D3 supersedes that acceptance.

## Pending work

| Stage | Outcome and scope | Dependencies / risk | Acceptance and done condition | Intended boundary / state |
|---|---|---|---|---|
| D3 navigator | Stop immediately on blocked F; return preserved pose and attempted outcomes; update affected regression coverage and usage documentation as needed | Confirmed D3; reconcile the existing maintenance candidate and its pending reviews without losing its helper rename or westward regression. Risk: obsolete continuation assertions and accidental batch rollback | Verify [contract examples](SPEC.md#acceptance), including earlier successes and unattempted suffixes; navigator suite and review gate pass | One coherent navigator behavior/tests/documentation increment; planned |
| Text adapter | Expose only the returned batch outcomes in text | D3 navigator complete; adapter does not yet exist. Risk: assuming one outcome per supplied command | FRF from `(0, 0, 0)` with `{(0, 1)}` displays one failure and no later successes; RFFL with `{(2, 0)}` displays two successes then failure. Proposed adapter integration coverage and navigator suite pass; review gate passes | One coherent adapter/integration/documentation increment; planned |

## Checks and review boundaries

Use [development operations](../DEVNOTES.md). Existing check:
`"$CANARY_PYTHON" -m unittest discover -s tests -v`; also run `git diff --check`.
Adapter integration coverage is proposed, not an existing check. Implement/test,
run these checks, obtain independent agent and human snapshot review, address
findings and recheck affected changes before any future authorized commit, following
the review policy recorded in [maintenance](MAINTENANCE.md). Record actual results
and reviewed candidate identity in the relevant stage record during execution.

The prior maintenance report and evidence remain tied to their captured candidate;
its pending approvals do not establish approval of D3. This revision executes no
stage, claims no test results or new acceptance, creates no commits, and performs
no external actions.
