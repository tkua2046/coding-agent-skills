# Plan

Next outcome: both APIs reject insufficient orders without changing their stock,
then continue processing later orders. Prerequisite: the independent reviewer
assesses [D2](DESIGN.md) and this plan together and material findings are resolved.
The decisive acceptance is the three-order example in D2, exercised through both
APIs with identical expected remaining stock and ordered outcomes.

## Outcome S1

Deliver the reservation change, regression tests and affected current documentation
as one coherent increment. The behavior is local to `inventory.reserve`; retain
the adapter and codec contracts. Update `docs/SPEC.md` to make the requested
rejection behavior current, and README usage to explain insufficient-order outcomes.
Preserve `docs/REQUEST.md`, `docs/ORIGINAL.md` and historical records. Keep
DEVNOTES as the operations owner; its existing gate remains applicable.

Acceptance beyond the decisive D2 example:

- A successful order followed by an insufficient order and then a feasible order
  uses current remaining stock, retains the earlier deduction, skips every deduction
  for the rejected order, and continues in input order.
- Single-item shortage rejects; exact availability succeeds; an empty order
  succeeds, including with empty stock; empty-batch behavior remains unchanged.
- Both APIs preserve caller stock; the Python API also preserves all nested order
  input (compare against a deep snapshot). Remaining quantities retain integer
  types, and acceptance fields are booleans.
- Existing success and JSON validation checks remain green. Preserve the codec's
  shape, ID, SKU and positive-integer rules; a malformed later JSON order still
  fails validation before reservation. Add targeted coverage for these compatibility
  boundaries where the current six tests do not establish them.

No separate delivery stage is useful for this small in-memory change. Implementation,
tests and current documentation belong together; no commit or release is requested.

## Checks and review policy

Follow [DEVNOTES](../DEVNOTES.md) and the [request's scope and budget](REQUEST.md):
use the prepared runtime, no installation or external services, and retain the
nonempty test-discovery gate. Run from the project root:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

Independent document review is complete. Implementation checks and independent
code review precede human acceptance. Agent-only review is authorized; human
acceptance has not occurred. Use the original 15-minute
whole-task allowance across these phases, not a fresh allowance per phase. No
commit, push, version advancement or release.

## Current handoff

S1 is implemented and its checks pass. Independent code review and human review
remain pending; implementation acceptance is not claimed. No known author findings
are open. Next: the separate independent agent reviews the candidate below against
[REQUEST](REQUEST.md), D2 and S1, then records findings and verification. Any required
fixes and rechecks precede human acceptance. No commit, push or release was made.

Document prerequisite: [original independent review](../reviews/design-current.json)
returned `ready` with no findings. Before editing, every SHA-256 in that report
matched, and the prepared runtime was Python 3.12.4. Thus the six-test baseline and
review evidence remain applicable to the pre-edit fixture. The otherwise unavailable
reviewed versions of [design](../reviews/document-candidate/docs/DESIGN.md),
[plan](../reviews/document-candidate/docs/PLAN.md),
[spec](../reviews/document-candidate/docs/SPEC.md) and
[README](../reviews/document-candidate/README.md) are preserved. Original requirements,
historical records and the review report are unchanged.

Implementation: `reserve` checks sufficiency before any deduction for each order.
Regression tests exercise both APIs with independently specified expected outcomes,
including rejection after earlier success, later exact availability, single-item
shortage, empty inputs, deep input preservation and exact result types. JSON boundary
tests assert malformed later orders never invoke reservation. The adapter and codec
are unchanged. SPEC owns current behavior; README explains usage and Unreleased impact.

Candidate: [snapshot identity](../reviews/s1-candidate.json) and
[diff from base](../reviews/s1-candidate.diff). The snapshot records the base commit
and hashes of relevant source, tests, contracts and gate configuration; the diff
includes new historical content. Evidence files are retained separately. Intended
files are staged for inspection, without a commit. Reviewed content is paused for
the incoming reviewer.

Checks on 2026-09-07, project root, prepared Python 3.12.4, no installs or services:

| Command | Result | Original output |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v` | 11 tests, OK | [suite](../reviews/s1-unittest.txt) |
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" hooks/pre-commit` | exit 0; 11 tests, OK; nonempty discovery enforced | [gate](../reviews/s1-gate.txt) |
| `git diff --cached --check` | exit 0 | [diff check](../reviews/s1-diff-check.txt) |

The gate made no source changes. Check success is author evidence, not independent
code approval or human acceptance. Earlier planning baseline and gap probe remain
in the preserved plan and original document review.

## Completed history

Original plan text retained:

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See the unchanged [completed S0 report](history/completed.md) and the
[accepted D1 snapshot](history/design-d1.md). The historical statement above does
not mark S1 complete.
