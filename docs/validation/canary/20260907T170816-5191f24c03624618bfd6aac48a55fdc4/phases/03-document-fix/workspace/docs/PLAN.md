# Plan

Next outcome: **S1 — whole-order rejection through both existing APIs** (planned,
not implemented). First obtain the independent combined review of
[DESIGN.md](DESIGN.md) and this plan. Scope and acceptance come from the unchanged
[request](REQUEST.md), [contract addendum](SPEC.md) and design acceptance table.
One stage is appropriate: engine behavior, regression tests and usage documentation
form one small observable change with no migration or external dependencies.

| Stage | Delivery and boundary | Acceptance / done condition |
| --- | --- | --- |
| S1 (pending) | Update `inventory.py` to preflight each order before deductions; extend `tests/test_inventory.py` for whole-order failure, continuation, exact depletion, empty orders and compatibility through both APIs; update `README.md` usage to describe rejection. Keep adapter validation and batch-local ownership. One coherent reviewable change; no commit requested. | Design's mixed-order and rejection-only examples pass, including input preservation and integer counts. Existing validation behavior and successful/empty batches remain intact. Full unittest discovery and local gate pass with nonempty discovery. Independent code review findings are resolved and affected checks rerun; record evidence for subsequent human review. |

Dependency: independent document reviewer resolves any material findings before
implementation. Follow [DEVNOTES.md](../DEVNOTES.md) for the gate and review policy:
implement and test, run `"$CANARY_PYTHON" -m unittest discover -s tests -v` and
`"$CANARY_PYTHON" hooks/pre-commit`, obtain an independent review of the concrete
code/test/doc snapshot, fix findings and rerun affected checks (including the full
gate after code changes). Record reviewed snapshot identity, findings and actual
commands/results in a new stage record without overwriting prior reports. Human
review follows; do not claim it has occurred. No commit, push, version change,
release, installation or external service is authorized or needed.

The 15-minute allowance covers the whole task, including downstream document and
code reviews; it is not a fresh budget per phase. Baseline checks already passed,
but feature checks remain proposed. See [baseline evidence](evidence/planning-baseline.md).
Planning stops here; S1 and both independent reviews are still pending.

## Preserved completed work

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request. The unchanged
[completed S0 record](history/completed.md) remains historical context.
