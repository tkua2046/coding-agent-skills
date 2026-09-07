# Plan
S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

## Current extension: pending S1

Status: S1 candidate implemented and locally checked; independent document review,
independent code review and human review remain pending. S1 is not accepted.
Current evidence and next action: [S1 stage record](../reviews/stage-s1.md).
Requirements: [REQUEST.md](REQUEST.md), preserving [ORIGINAL.md](ORIGINAL.md).
Design and decisive acceptance: [DESIGN.md, D2](DESIGN.md#d2-proposed-whole-order-rejection).
Completed S0 remains unchanged; its historical report is
[history/completed.md](history/completed.md).

Next outcome: the independent reviewer resolves the document-review limitation and confirms whole-order atomicity, continuation,
compatibility and feasible checks, or records concrete blockers for correction.
The candidate is prepared under the current implementation request; this does not
waive the unresolved document-review dependency. Use a focused design/plan review and
a focused code/test review for this small in-memory change, within the original
15-minute whole-task allowance. No review approval is claimed.

| Stage | Observable outcome / scope | Dependency and boundary | Decisive acceptance / risk | State |
|---|---|---|---|---|
| S1 | Whole-order rejection and continuation through both APIs; engine change, regression tests and README usage update together | Independent design/plan review remains unresolved; one coherent reviewable patch because checking and deduction must ship together | D2 late-shortage batch and sequential depletion; input immutability, integer counts, empty/exact-fit behavior and unchanged JSON errors; complete local gate | Candidate checked; reviews pending |

S1 should keep `batch.py` and `command_codec.py` behavior intact, place allocation
logic in `inventory.py`, and extend `tests/test_inventory.py`. Update README's
caller-sufficiency statement to describe rejection. The current spec addendum is
already proposed in this planning phase; reconcile documentation if review changes
the contract. No dependencies, new infrastructure or expanded validation policies.

### Execution, checks and handoff

Follow [DEVNOTES.md](../DEVNOTES.md) and the request's agent-only review policy:
implement with regression tests, run the full suite and supplied hook, review the
resulting code/test snapshot, fix findings and rerun affected checks plus the gate.
Human review happens afterward. No commit, push, version advancement or release is
requested; S1 is a single patch boundary, not an instruction to commit.

Existing commands, verified in this phase (six tests passed in each):

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

Use these same commands after adding regression coverage; no installation or external
service is needed. The decisive new examples are proposed checks, not existing passes.
Baseline implementation findings and the negative-stock probe are in
[DESIGN.md](DESIGN.md#verified-baseline-and-limits).

Done means both APIs satisfy D2 acceptance, compatibility checks and the nonempty
full gate pass, focused code review findings are resolved, and README reflects the
behavior. Append implementation evidence and reviewer identity/snapshot/findings
to a stage record without overwriting prior reports. Until then, keep S1 pending.
