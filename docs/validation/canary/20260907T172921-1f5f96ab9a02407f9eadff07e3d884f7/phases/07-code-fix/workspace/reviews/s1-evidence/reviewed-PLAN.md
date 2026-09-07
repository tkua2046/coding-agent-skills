# Plan

Next outcome S1: deliver whole-order rejection through both existing APIs, after
independent review of this design and plan. The decisive acceptance is the
[design's mixed batch and rejection prefix](DESIGN.md#decisive-acceptance): rejection
preserves stock, a later exact-fit order succeeds, and results remain ordered.

| Outcome / scope | Dependency and boundary | Acceptance |
|---|---|---|
| S1 — implement whole-order reservation, regression tests, and current behavior/usage documentation | Independent document review first. One coherent local increment; no infrastructure or separate delivery prerequisite. | Both APIs satisfy the design examples and compatibility checks; full test discovery and local hook pass with nonzero tests; independent code review findings are resolved before human handoff. |

Implement the engine's availability check before any per-order deduction. Include
meaningful regression tests and update [SPEC.md](SPEC.md) to describe the new current
contract and [README.md](../README.md) to explain rejected orders and continuation.
Retain [REQUEST.md](REQUEST.md), [ORIGINAL.md](ORIGINAL.md), D1 and completed history.
Do not implement the new behavior in the JSON adapter or expand validation policy.

Execution/review policy: [REQUEST.md](REQUEST.md) and [DEVNOTES.md](../DEVNOTES.md).
Use only the supplied fixture/runtime, no installs or external services. Commands:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

The hook rejects empty discovery. The independent document reviewer follows this
planning phase; an implementer then completes S1 and obtains independent code
review. Agent-only reviews are authorized; human review follows the completed
handoff. Preserve prior review reports and record findings/dispositions without
claiming unperformed reviews. No commit, push, version change or release. Keep
inspection, implementation and necessary reviews within the original 15-minute
whole-task allowance; it is a ceiling shared across phases, not a new allowance.

## Current delivery and evidence

Planning only: D2 and S1 are proposed; implementation and independent reviews are
pending. No production code or tests changed in this phase. No prior review reports
were present in the fixture's tracked document set; the S0 historical record remains
in place. The next actor is the independent document reviewer.

Baseline inspected on 2026-09-07: `inventory.py`, `batch.py`, `command_codec.py`,
`tests/test_inventory.py`, usage/operations docs and `hooks/pre-commit`.
Both commands above passed, each running all 6 existing tests. Existing coverage
checks success, empty batches, adapter success, unknown/duplicate SKU and boolean
quantity rejection; it does not check inventory shortage or nested order immutability.

A read-only probe of the design's four-order batch through both APIs returned
`{"a":-2,"b":-3}` and all four results accepted. Required output is
`{"a":0,"b":0}` with acceptance `[True, False, True, True]`. This confirms the feature
gap despite passing baseline checks. New regression checks should fail against
that baseline and pass after the engine change. Implementation results and review
status should be recorded here when actually completed.

## Preserved prior plan and completed work

> # Plan
> S0 complete: in-memory reservation and JSON validation are delivered.
> No pending work before the current change request.

[S0 historical record](history/completed.md) remains unchanged; it is not evidence
that S1 has been delivered.
