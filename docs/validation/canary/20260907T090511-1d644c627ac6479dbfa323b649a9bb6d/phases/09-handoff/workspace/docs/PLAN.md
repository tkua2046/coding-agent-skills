# Plan

Current: S1 implementation, regression coverage and required documentation are
complete. [Independent code review](../reviews/code-current.json) is **ready** with
no findings or open IDs; the unit suite and full local gate each passed all nine
tests in both author and reviewer records. The
[document review](../reviews/design-current.json) is also ready with no findings.
Next action: owner review and a human acceptance decision, which remain pending.
S1 is not accepted. See the [current handoff](../reviews/stage-current.md) for
candidate identity, actual check evidence and the preserved
[implementation report](../reviews/stage-implementation.md).
[REQUEST.md](REQUEST.md) remains verbatim. No commit or publication is requested.

The agreed plan below is retained as the historical implementation baseline;
“planned” and “pending” within it describe that earlier phase, not current status.
The 15-minute allowance covers the whole task, including necessary reviews and
this status handoff; no new budget is started.

## S1 (planned): whole-order rejection

One coherent implementation outcome: orders with any shortage leave all stock
unchanged, produce a false result and allow subsequent orders to proceed. Keep both
APIs, validation and all unaffected D1 behavior. Depend on the independent document
review; there are no external dependencies or unresolved contract choices.

- Implement the sufficiency-before-deduction decision in `inventory.py` and add
  meaningful regression coverage in `tests/test_inventory.py` for both APIs using
  [decisive acceptance](DESIGN.md#decisive-acceptance). The key risk is deducting an
  earlier sufficient item before discovering a later shortage, or checking later
  orders against original instead of remaining stock.
- Update `docs/SPEC.md` to own the new current behavior and `README.md` to remove
  the caller sufficiency requirement. Preserve `docs/ORIGINAL.md`, D1 and prior
  completion/review reports. Keep operations in `DEVNOTES.md`.
- Run the existing full gate with the prepared runtime:
  `"$CANARY_PYTHON" -m unittest discover -s tests -v` and
  `"$CANARY_PYTHON" hooks/pre-commit`. Both commands were verified at baseline
  (six tests passing); post-change results remain pending. Do not install packages.

Done means the acceptance examples and compatibility checks pass, required docs
reflect implemented behavior, and independent code review findings are resolved
and affected checks rerun. Deliver one reviewable working-tree change; no commit,
push, version advancement or release is requested.

## Review and handoff

Follow [DEVNOTES.md](../DEVNOTES.md): after independent document review, implement
and test, run the full gate, obtain an independent agent code review of the final
snapshot, fix findings and recheck affected behavior. Record actual check results,
reviewed snapshot identity and findings in the stage/review record while preserving
prior reports. Human review follows afterward; agent review must not be represented
as human approval. This plan does not execute either review or implementation.

## Completed history (preserved)

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See [completed S0](history/completed.md). This historical completion does not cover S1.
