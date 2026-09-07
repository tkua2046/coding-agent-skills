# Whole-order inventory reservation

Before deducting an order, check every requested quantity against the current
batch-local stock. If any item is insufficient, append `accepted=False` and deduct
nothing for that order; otherwise deduct every item and append `accepted=True`.
This avoids partial deductions without rollback or extra stock snapshots. For
example, after reserving one unit from `a=4,b=2`, an order for `a=2,b=3` must leave
`a=3,b=2` available for a later order that consumes exactly that inventory.

Decision D2: independently reviewed as ready in
[the preserved document review](../reviews/design-current.json).
See [the current handoff](PLAN.md#current-delivery-and-evidence) for completed
implementation, independent code review, open findings and pending human acceptance.
This is a local extension to D1,
replacing only the caller-sufficient-inventory assumption. Requirements remain in
[REQUEST.md](REQUEST.md) and [ORIGINAL.md](ORIGINAL.md); delivery and evidence live
in [PLAN.md](PLAN.md). No material open decisions remain.

## Behavior and boundaries

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` signatures
and their `(remaining, outcomes)` return shape. Copy stock once, process orders in
input order, and return one `{"order_id": id, "accepted": boolean}` per order.
Insufficiency is a normal rejection, not an exception or an end to the batch.
Earlier successful deductions remain effective; later orders see only those
successful deductions. Exact availability succeeds. An empty order succeeds and
changes nothing; an empty batch returns copied stock and no outcomes.

The engine continues to trust validated input. The JSON adapter still validates the
whole payload before invoking the engine; preserve its existing errors, shapes,
unique IDs/SKUs and positive integer rules. Do not add validation to either API.
Neither stock nor nested order inputs may be mutated, on success or rejection.
Integer stock counts stay integers and, for valid nonnegative input, nonnegative.

The pre-S1 engine deducted unconditionally, while `batch.execute` delegates through
`command_codec.decode`. The change belongs in the engine; the adapter and codec
need no behavioral changes. Unique item SKUs make per-item availability checks
sufficient without aggregation. Checking before deduction takes another traversal
of each successful order, with linear total work and no per-order stock copy.
This guarantee concerns inventory insufficiency in this single-process in-memory
utility; persistence, concurrency and transaction infrastructure remain out of scope.

## Decisive acceptance

Run this same valid batch through both APIs, starting with `{"a":4,"b":2}`:

| Order ID | Items | Accepted | Stock afterward |
|---|---|---|---|
| first | `[["a",1]]` | `True` | `{"a":3,"b":2}` |
| reject | `[["a",2],["b",3]]` | `False` | `{"a":3,"b":2}` |
| later | `[["a",3],["b",2]]` | `True` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

Assert exact ordered IDs and booleans, final stock, integer counts, and unchanged
original stock and nested orders. Also test the first two orders as a prefix to
observe the unchanged stock immediately after rejection. Cover a single-item
shortage (including zero available), an empty batch, and the existing success and
JSON validation contracts. Preserve all existing tests; add representative invalid
shape, duplicate-ID and nonpositive/noninteger quantity checks where coverage is
missing. These examples distinguish correct rejection from unconditional deduction,
partial deduction, stopping the batch, or checking against initial stock.

## Preserved accepted design D1

The following is the original accepted design, retained verbatim as historical
context. Its sufficient-inventory assumption is superseded by the requested D2.

> # Accepted design D1
> The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
> The engine trusts validated orders and copies stock once for batch-local mutation.
> Sufficient inventory is currently the caller's responsibility. The function returns
> one boolean acceptance result per order and does not mutate caller inputs.
