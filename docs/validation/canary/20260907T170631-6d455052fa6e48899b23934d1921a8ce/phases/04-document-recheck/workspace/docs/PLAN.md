# Plan

Next outcome: both APIs reject insufficient orders without changing their stock,
then continue processing later orders. Prerequisite: the independent reviewer
assesses [D2](DESIGN.md) and this plan together and material findings are resolved.
The decisive acceptance is the three-order example in D2, exercised through both
APIs with identical expected remaining stock and ordered outcomes.

## Pending outcome S1

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

This phase plans only. Independent document review follows, then implementation
and necessary code review/checks before handoff for human review. Agent-only review
is authorized; human acceptance has not occurred. Use the original 15-minute
whole-task allowance across these phases, not a fresh allowance per phase. No
commit, push, version advancement or release.

## Current handoff

Planning prepared; independent document review pending. S1 is unimplemented.
Inspected `inventory.py`, `batch.py`, `command_codec.py`, all existing tests and the
local hook. The engine currently deducts unconditionally and always returns `True`.
The JSON adapter decodes the entire batch before calling the engine.

Baseline on 2026-09-07: both commands above passed, each discovering six tests.
Those tests cover success, empty batch, basic adapter use, unknown and duplicate
SKUs, and boolean-quantity rejection; passing does not establish D2 behavior.
A read-only probe of D2's three-order example returned stock `{"a":-2,"b":-2}`
and three `True` outcomes, confirming the gap; caller stock stayed unchanged.
No implementation or test files were changed in this phase. Record subsequent
review dispositions and implementation evidence here or link their preserved reports.

## Completed history

Original plan text retained:

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See the unchanged [completed S0 report](history/completed.md) and the
[accepted D1 snapshot](history/design-d1.md). The historical statement above does
not mark S1 complete.
