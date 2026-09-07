# Whole-order inventory rejection

Proposed D2: check every item against the current batch-local remaining stock
before deducting any item in that order. If any quantity is insufficient, append
`accepted=False` and leave that order's starting stock intact; continue processing
later orders. Otherwise deduct all items and append `accepted=True`. This avoids
partial deductions without rollback machinery, at the cost of a second item pass
for successful orders. For example, an order requesting a sufficient `a` followed
by an insufficient `b` must consume neither; a later order can use both.

Requirements: [requested extension](REQUEST.md), [original contract](ORIGINAL.md),
and [current specification](SPEC.md). D2 supersedes only D1's caller-sufficiency
assumption. Next outcome and review/delivery status: [plan](PLAN.md).

## Behavior and boundaries

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` signatures
and return shapes. The engine continues to copy stock once and to trust validated
orders; it must not mutate stock or nested order inputs. Each order gets one
boolean outcome, in input order, using stock remaining after earlier successes.
Exact availability succeeds, integer quantities remain integers, an empty order
succeeds without deductions, and an empty batch returns copied stock and no results.

`command_codec.decode` continues validating the entire JSON batch before invoking
the engine. Insufficient stock is an ordinary rejection outcome, not a validation
error. Preserve existing malformed-input errors and policies; no additional engine
validation. Known unique SKUs make per-item availability checks sufficient without
aggregation. Two passes are compatible with the existing validated item lists.

This is order-level atomicity in a single-process in-memory call. Earlier successes
remain applied to the local copy when a later order is rejected. No persistence,
concurrency, transaction framework, remote infrastructure or new dependency is needed.

## Decisive acceptance

Run this sequence through both APIs with initial stock `{"a":4,"b":1}`:

| Order | Items | Accepted | Remaining stock |
| --- | --- | --- | --- |
| first | `[["a",1]]` | `True` | `{"a":3,"b":1}` |
| reject | `[["a",2],["b",2]]` | `False` | `{"a":3,"b":1}` |
| later | `[["a",3],["b",1]]` | `True` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

Assert exact ordered outcomes and final stock, plus deep preservation of caller
inputs and integer stock values. Also check cumulative depletion: with `{"a":3}`,
orders requesting 2 then 2 then 1 yield `True, False, True` and final `{"a":0}`.
This distinguishes checks against current stock from checks against original stock.
Cover rejection at zero stock, empty batches, and existing JSON validation regressions.

## Preserved accepted design D1

The following source text is retained verbatim as historical context:

# Accepted design D1
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
