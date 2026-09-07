# Plan

Next: deliver stop-on-block behavior in the navigator, using the confirmed
[contract](SPEC.md) and [design](DESIGN.md). The confirmation is available and
there is no unresolved prerequisite. Decisive acceptance: FRF from (0,0,0) with
{(0,1)} occupied returns ((0,0,0), [False]). Adapter delivery follows this contract
change so it exposes only attempted-command outcomes.

| Pending outcome / scope | Dependency and boundary | Acceptance evidence to obtain |
|---|---|---|
| Navigator stops on blocked F; update affected tests and README usage together. | Confirmed stop request; usable public API change can be validated independently of the absent adapter. | Navigator suite covers the SPEC examples, replacing continuation expectations, including preserved successful prefix, negative coordinates, unattempted suffix, and a subsequent independent batch. |
| Expose batch outcomes in the text adapter, with integration coverage and README usage. | Navigator stop behavior above; retains the existing adapter delivery boundary. No text adapter exists in the fixture yet. | FRF with (0,1) occupied displays one failure and no later successes; RFFL with (2,0) occupied displays two successes then failure, with no outcome for L. Displayed outcomes match the navigator's returned prefix. |

## Execution and review policy

Follow [AGENTS.md](../AGENTS.md) and [DEVNOTES.md](../DEVNOTES.md). Planned checks:
run the navigator suite and adapter integration coverage using the prepared runtime,
`"$CANARY_PYTHON" -m unittest discover -s tests -v`, before review. No additional
approval gate is introduced. This phase authorizes planning only, with no
implementation, commits, package installation or external actions.

## Current delivery status

Both rows are pending. Code and tests still implement accepted historical D2
continuation; the stop contract has not been implemented or tested. Planning
inspection covered navigator.py, tests/test_navigator.py and repository guidance.
No runtime checks were run in this planning phase. Prior acceptance remains
historical evidence, not validation of the new behavior.

## Completed-stage history (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).

The [prior plan](history/plan-before-stop.md) preserves the superseded pending
adapter acceptance. The [S0 record](history/completed.md) and
[D2 acceptance record](history/d2-review.md) remain unchanged. Original sources:
[original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md), and
[subsequent stop confirmation](STOP_REQUEST.md).
