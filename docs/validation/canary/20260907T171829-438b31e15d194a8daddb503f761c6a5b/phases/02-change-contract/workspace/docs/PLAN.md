# Plan
Next: implement the confirmed stop-on-block contract in the navigator. The behavior
decision is settled by [STOP_REQUEST](STOP_REQUEST.md); execution follows this
planning-only phase. Decisive acceptance: (0,0,0), `FRF`, occupied {(0,1)} returns
(0,0,0), [False].

| Pending outcome / scope | Dependency and boundary | Acceptance evidence to produce |
|---|---|---|
| Deliver stop-on-block behavior with updated navigation tests and affected usage documentation. | Confirmed [D3 design](DESIGN.md); a usable core result before adapter integration. | [Contract examples](SPEC.md) cover first and later blocks, preserved successful prefix, omitted suffix (including unknown commands), turns, negative coordinates, and subsequent runs. Retain attempted-unknown and empty-batch behavior. Run the navigator suite. |
| Expose batch outcomes in the text adapter with integration coverage and usage documentation. | Depends on the core stop behavior above; separate adapter-facing result. No adapter exists in the inspected fixture, so its entry point/interface must be established when that pending work starts. | `FRF` with (0,1) occupied displays only failure, with final pose (0,0,0); no output for the unattempted R/F. `RFFL` with (2,0) occupied displays two successes then failure and final pose (1,0,1). Include an unblocked batch integration case. |

Checks and review policy: follow [AGENTS.md](../AGENTS.md) and
[DEVNOTES.md](../DEVNOTES.md). Before review, run
`python3 -m unittest discover -s tests -v` and the proposed adapter integration
coverage when that outcome is implemented. These are planned checks, not results.
This phase permits document revisions only, with no commits or external actions;
it adds no approval or review gate.

## Current delivery status

D3 planning revision is complete; core implementation and adapter work remain
pending. Inspection shows the navigator still continues after a block and an
existing test asserts D2 continuation. Existing staged code/test edits are retained.
No implementation or tests were run in this planning phase. Prior acceptance
records do not establish validation of D3.

## Completed-stage history

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).

Historical evidence: [completed S0](history/completed.md),
[accepted D2 record](history/d2-review.md), and
[prior plan/design/contract](history/d2-artifacts.md). The earlier adapter acceptance
of failure followed by two successes is superseded by the pending outcome above;
completed D2 remains recorded as delivered under its then-current contract.
