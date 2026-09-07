# Plan

Current: D2 and S1 passed the independent [document review](../reviews/design-current.json)
with no findings; all recorded content hashes matched at implementation intake.
S1 is implemented and prepared for independent code review, followed by human
review. See the [S1 handoff](../reviews/s1-handoff.md) for the candidate, exact checks,
and pending review status. One delivery stage covers the local behavior and its
checks; no additional design approval stages are needed.
The original 15-minute allowance covers the whole task, including necessary
document/code reviews, and is a ceiling rather than a target or a fresh allowance
for each phase. No commit, push, version advancement or release is requested.

## S1: whole-order rejection (implemented; review pending)

Deliver the [D2 contract and decisive acceptance](DESIGN.md#decisive-acceptance)
in `inventory.py` with regression coverage in `tests/test_inventory.py` for both
APIs. The independent document review is complete. The main risk is deducting an
earlier item before discovering a later shortage, or losing prior successful
deductions. Keep the current adapter and
validation policies. Update `docs/SPEC.md` to make D2 the current behavior while
retaining its link to original requirements, and update README usage to remove
the sufficient-stock caller obligation and explain rejection/continuation.

Done means the decisive acceptance passes, caller inputs and integer counts are
preserved, validation behavior remains intact, the complete gate below passes,
and code review has no unresolved blocking findings. Treat implementation,
regression tests and these behavior/usage updates as one reviewable change;
there is no commit in this task. Follow [DEVNOTES.md](../DEVNOTES.md):
implement/test → run full test command and local gate → agent code review of the
identified snapshot → fix and rerun affected checks/gate → hand off for human
review. Record commands/results, reviewed snapshot identity and findings in a new
stage/review record without overwriting prior reports. Agent-only review is
authorized; do not claim human acceptance before it happens.

## Verified baseline

2026-09-07, before implementation, using the supplied `CANARY_PYTHON` runtime:

- `"$CANARY_PYTHON" -m unittest discover -s tests -v`: exit 0, six tests passed.
- `"$CANARY_PYTHON" hooks/pre-commit`: exit 0, six tests passed; this full gate
  also rejects empty test discovery. Use these same commands after implementation.
- Read-only shortage probe: stock `{"a":4,"b":1}`, orders `reject` requesting
  `[["a",3],["b",2]]` then `later` requesting `[["a",4]]`, returned
  `{"a":-3,"b":-1}` and both accepted. D2 instead requires unchanged stock
  after `reject`, then final `{"a":0,"b":1}` and acceptance `[False, True]`.

Existing coverage checks success, empty batches, adapter success and selected
validation failures, but lacks shortage, empty-order and nested-order immutability
assertions. Passing baseline checks are evidence for S0 only, not feature completion.

## Historical plan (preserved)

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See [completed S0 record](history/completed.md); it remains unchanged.
