# Whole-order rejection delivery

Next outcome: S1 delivers whole-order rejection through both existing APIs after
the independent reviewer assesses this design and plan. Decisive acceptance is the
[mixed-order sequence and cumulative depletion case](DESIGN.md#decisive-acceptance):
rejected orders consume nothing, later orders continue, and successful orders deduct
fully. There are no unresolved material design choices.

| Pending outcome | Dependency and boundary | Acceptance |
| --- | --- | --- |
| S1: implement availability-before-deduction in the engine, with regression tests and updated current behavior/usage documentation | Independent document review first; one local increment because both APIs share the engine and no separate delivery dependency exists | Both APIs satisfy the design examples; inputs and validation remain intact; full tests and existing hook pass; independent code review findings are resolved |

Update `docs/SPEC.md` to describe the extension and README's caller-sufficiency
wording when S1 is implemented. Preserve `docs/REQUEST.md`, `docs/ORIGINAL.md`, D1,
completed S0 and any review reports. DEVNOTES remains the owner of operational
checks; no operational change is anticipated.

## Execution and review policy

Follow [the request](REQUEST.md) and [DEVNOTES](../DEVNOTES.md). This phase changes
planning documents only. An independent reviewer follows, then an implementer;
the implementer runs the existing gate and obtains the necessary independent code
review before handing off for human review. Agent-only review is authorized; do not
claim human acceptance. Keep review findings and dispositions in their review
records and link them here. No commit, push, version change or release is requested.
The 15-minute allowance covers the whole task, including reviews and implementation;
it is not a separate budget for each phase or a target to consume.

Use the prepared runtime, without installation or external services:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

## Current handoff and baseline

- Planning prepared; independent document review pending. S1 is unimplemented;
  code review and human review are pending. No implementation or test files changed.
- Inspected `inventory.py`, `batch.py`, `command_codec.py`, tests, and the hook.
  The engine deducts unconditionally and always reports success. The adapter
  validates all JSON orders before calling it. Existing tests cover success,
  empty batches, adapter success, unknown/duplicate SKUs and boolean quantities,
  but do not cover insufficient inventory or deep order-input preservation.
- Baseline on 2026-09-07: both commands above passed, each collecting 6 tests.
  These results establish the existing baseline, not acceptance of S1.
- A read-only probe of the design's mixed-order sequence returned stock
  `{"a":-2,"b":-2}` with all four outcomes `True`, confirming the requested gap.
  The required result is `{"a":0,"b":0}` with `True, False, True, True`.

Sources: [design](DESIGN.md), [request](REQUEST.md), [original](ORIGINAL.md).
Completed work: [S0 historical record](history/completed.md).

## Preserved prior plan

The following source text is retained verbatim as historical context:

# Plan
S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.
