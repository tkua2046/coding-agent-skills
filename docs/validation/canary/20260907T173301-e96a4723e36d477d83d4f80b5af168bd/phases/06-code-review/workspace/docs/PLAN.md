# Whole-order rejection delivery

S1 implements whole-order rejection through both existing APIs. Decisive acceptance is the
[mixed-order sequence and cumulative depletion case](DESIGN.md#decisive-acceptance):
rejected orders consume nothing, later orders continue, and successful orders deduct
fully. There are no unresolved material design choices.

| Stage contract | Dependency and boundary | Acceptance |
| --- | --- | --- |
| S1: implement availability-before-deduction in the engine, with regression tests and updated current behavior/usage documentation | Independent document review first; one local increment because both APIs share the engine and no separate delivery dependency exists | Both APIs satisfy the design examples; inputs and validation remain intact; full tests and existing hook pass; independent code review findings are resolved |

`docs/SPEC.md` now describes the extension and README explains rejection to callers.
`docs/REQUEST.md`, `docs/ORIGINAL.md`, D1, completed S0 and prior review reports are
preserved. DEVNOTES remains the owner of operational checks; operations are unchanged.

## Execution and review policy

Follow [the request](REQUEST.md) and [DEVNOTES](../DEVNOTES.md). The independent
document review passed and implementation is prepared for the separate code
reviewer. Independent code review is required before acceptance for human review.
Agent-only review is authorized; do not
claim human acceptance. Keep review findings and dispositions in their review
records and link them here. No commit, push, version change or release is requested.
The 15-minute allowance covers the whole task, including reviews and implementation;
it is not a separate budget for each phase or a target to consume.

Use the prepared runtime, without installation or external services:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

## Current handoff

- S1 implementation and regression coverage are complete; the installed gate passed.
  Independent code review and human review remain pending. Next: the separate
  reviewer assesses the captured candidate and records findings; resolve and
  recheck any material findings before human acceptance. No commit was made.
- [Independent document review](../reviews/design-current.json): ready, no findings.
  Before implementation, every recorded SHA-256 matched the fixture. The otherwise
  unavailable reviewed design/plan are preserved in
  [the original document snapshot](../reviews/evidence/d2-reviewed-documents.json).
  There is no unresolved document-review blocker.
- The engine now checks all requested items before deducting. Tests exercise both
  APIs for rejection without partial deduction, continued processing, cumulative
  depletion, exact availability, zero stock, empty orders/batches, deep input
  preservation and integer/boolean types. Existing validation tests are retained;
  an additional test checks that a malformed later order prevents engine invocation.
  README owns usage and Unreleased impact; SPEC describes current behavior.
- Candidate: base `00a3e7d561907ec46b41344298221692a1d1d4a8` plus
  [captured changed-file diff and new-file content](../reviews/evidence/s1-candidate.json).
  This snapshot also includes requirements, unchanged API/validation code and hook
  configuration needed to interpret checks. Prior review output is preserved.
- Checks on 2026-09-07 used `/Users/tk/Documents/coding-agent-skills/.venv/bin/python`,
  Python 3.12.4, via `CANARY_PYTHON`, without installation or external services:
  - `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`
    before the engine fix: exit 1, 12 tests, 8 failing subtests across both APIs.
    [Original failure output](../reviews/evidence/s1-before.txt) demonstrates that
    the new behavioral tests detect the previous unconditional deductions.
  - `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" hooks/pre-commit`
    after the fix: exit 0, all 12 tests passed.
    [Original gate output](../reviews/evidence/s1-gate.txt). The hook runs the full
    suite and rejects empty collection; no duplicate standalone run was needed.
- Prior six-test baseline and original probe results remain in the preserved
  document snapshot and review. They establish historical behavior only.
- Intended changes and evidence are staged for review; the staged diff was inspected.
  `git diff --check` passed before staging. `git diff --cached --check` exits 2
  solely for four trailing spaces in preserved raw unittest failure output
  (`s1-before.txt`); that output is retained verbatim. The source/document-only
  staged whitespace check passed. Git emitted sandbox cache/config warnings but
  returned diffs and status successfully. The hook made no automatic changes.

Sources: [design](DESIGN.md), [request](REQUEST.md), [original](ORIGINAL.md).
Completed work: [S0 historical record](history/completed.md).

## Preserved prior plan

The following source text is retained verbatim as historical context:

# Plan
S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.
