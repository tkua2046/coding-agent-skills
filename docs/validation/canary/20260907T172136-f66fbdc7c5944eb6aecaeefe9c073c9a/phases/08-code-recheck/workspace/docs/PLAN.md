# Plan

Status: D2/S1 independent document review ready with no findings; S1 implemented
and awaiting independent code review, then human review. Current state and exact
checks: [S1 record](../reviews/s1-stage.md). Document review:
[preserved report](../reviews/design-current.json).
Requirements: [REQUEST](REQUEST.md), [original](ORIGINAL.md). Rationale:
[DESIGN D2](DESIGN.md). Behavior and decisive checks: [SPEC](SPEC.md).

## S1: reject insufficient orders without partial deductions

After one combined independent design/plan review resolves blocking findings,
update the reservation engine, add focused regression coverage in the existing
unittest suite, and update README usage to describe rejection and continuation.
One coherent implementation/review boundary is sufficient because both APIs share
the engine; no independently deliverable intermediate state is needed. Preserve
the decoder's validation contract. The main risk is deducting an early item before
discovering a later shortage, or checking availability against stale stock.

Accept S1 when both APIs satisfy the [decisive acceptance](SPEC.md#decisive-acceptance),
including rejection without any deduction, continuation, sequential depletion,
exact-stock success, empty orders/batches, integer counts and full input preservation.
Keep validation regression coverage appropriate to the unchanged boundary. Tests
must assert concrete outcomes and final stock, not merely absence of exceptions.

Use the existing [development gate](../DEVNOTES.md), with the prepared runtime:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" .git/hooks/pre-commit
```

Both commands were verified during planning: 6 baseline tests passed, including
the installed gate's nonempty-discovery check. S1 results are in the current record. The
baseline shortage probe failed the target contract as recorded in DESIGN.

Review policy: the independent reviewer follows this planning phase; the implementer
follows document review. After implementation and checks, obtain an agent code review
of the resulting snapshot, fix blocking findings and rerun affected checks/gate before
human handoff. Preserve prior reports and record reviewed snapshot, findings, fixes
and actual check results in a new stage/review record when that work occurs. Do not
claim agent review is human acceptance. Done means implemented behavior, passing gate,
resolved blocking code-review findings and a concrete result ready for human review.
No commit, push, version advancement or release is requested; this stage is a review
boundary only. All phases share the original 15-minute execution allowance; keep
reviews bounded to this change rather than adding stages or consuming the budget.

## Completed history (preserved)

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See [completed S0 record](history/completed.md). Its completion is historical and
does not establish acceptance of S1.
