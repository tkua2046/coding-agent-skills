# Design: whole-order inventory reservation

Status: D2 independently reviewed as ready; implementation review pending.
See the [document review](../reviews/design-current.json) and
[S1 execution record](../reviews/stage-s1.md). Requirements:
[request](REQUEST.md), [current contract](SPEC.md), [original](ORIGINAL.md).

Outcome: insufficient orders return `accepted=False` without changing stock;
later orders still run. Check all items against batch-local remaining stock before
deducting any. This adds a read pass per order and avoids rollback state. For
`{a:4,b:1}`, an order requesting `a:3,b:2` fails and a following `a:2` succeeds,
leaving `{a:2,b:1}`. Both APIs and validation stay compatible.

Next: independent code review of [S1](PLAN.md), then human review.
Document readiness does not establish implementation acceptance.

## Accepted design D1 (historical)

The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.

D2 supersedes only D1's caller responsibility for sufficient stock. The remaining
accepted choices carry forward; [completed S0](history/completed.md) is preserved.

## Baseline behavior and decision

Before S1, `inventory.py` copied stock once, then unconditionally subtracted every
requested item and reported success. `batch.py` fully decodes the batch before calling the
engine; `command_codec.py` owns validation. Neither adapter needs a new policy.

**Decision →** preflight each order against current remaining stock, then deduct
only if every item fits. **Reason →** unique SKUs and trusted positive quantities
make this sufficient in the single-process utility. **Consequence →** no partial
deductions on rejection; linear work in total requested items, with two passes
for successful orders and no extra per-order stock copy. **Example →** a shortage
in the final item must preserve even the first item's stock.

Deduct-and-rollback is a credible alternative but adds restoration paths without
benefit here. Copying all stock per order also works but copies unrelated SKUs.
Keep the single batch-local copy; caller stock and nested orders remain untouched.
Earlier successes persist, rejected orders have no stock effect, and later orders
see exactly the remaining stock. No concurrency or crash-atomicity guarantee is
introduced.

## Acceptance

These expected results are derived from the request, not the current engine.
Exercise the decisive sequence through both public APIs:

| Starting stock / ordered requests | Expected remaining / ordered acceptance |
|---|---|
| `{a:4,b:1}`; `reject: a3,b2`; `later: a2` | `{a:2,b:1}`; `reject=False, later=True` (late shortage preserves all stock) |
| `{a:4,b:1}`; `first: a3`; `reject: a2,b1`; `last: a1,b1` | `{a:0,b:0}`; `first=True, reject=False, last=True` (checks current stock, keeps prior success, exact depletion) |
| `{a:0}`; `reject: a1`; `empty: []` | `{a:0}`; `reject=False, empty=True` |
| `{a:2}`; no orders | `{a:2}`; no outcomes, returned stock is a distinct dictionary |

Every outcome retains its original ID and boolean acceptance in order. Assert
unchanged stock and nested orders against pre-call snapshots, integer remaining
counts, and nonnegative stock for valid inputs. A multi-item successful order must
deduct every item. Repeat shortage with the insufficient SKU first as well as last
to catch position-dependent mutation.

Retain JSON rejection for malformed shapes/JSON, unknown or duplicate SKUs,
duplicate IDs, and nonpositive or noninteger quantities (including booleans).
Invalid JSON batches still raise before engine execution, even when a preceding
order is valid. Do not prescribe new errors or validation for direct engine calls.

## Validation and limits

The six baseline tests and complete local gate passed, but contained no shortage
coverage; [baseline evidence and commands](PLAN.md#baseline-evidence) record the
observed failure. Add focused regression coverage for the acceptance above and
run the complete existing gate. No dependencies or external research are needed.
There are no unresolved behavior decisions; independent review may identify
necessary corrections. Review scope is the local D2/S1 amendment, preserving D1
history, within the original 15-minute whole-task allowance.
