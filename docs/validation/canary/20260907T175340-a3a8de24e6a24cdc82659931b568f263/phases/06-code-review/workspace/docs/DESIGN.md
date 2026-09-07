# Whole-order reservation

Reject an order if any requested quantity exceeds the current remaining stock.
Check all its items before deducting any, then either deduct every item and return
`accepted=True`, or deduct nothing and return `accepted=False`. Continue in input
order. This uses the existing batch-local copy and avoids rollback or a transaction
framework; the cost is a second traversal of successful orders' items.

Decisive example: with stock `{"a":4,"b":1}`, an order for `a:2,b:2`
rejects without changing either quantity. A following order for `a:4` succeeds,
and a following empty order succeeds. Final stock is `{"a":0,"b":1}`;
acceptance results are `[False, True, True]` with the original order IDs.

Decision: extension D2 passed [independent document review](../reviews/design-current.json).
Sources:
[requested extension](REQUEST.md), [original requirements](ORIGINAL.md), and
[current contract](SPEC.md). Delivery and verification status live in [PLAN.md](PLAN.md).
No material open decision requires clarification.

## Behavior and boundaries

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` signatures
and their `(remaining, outcomes)` return shape. Each order has exactly one result
`{"order_id": id, "accepted": bool}` in input order. Compare against stock left by
prior successful orders, including exact depletion to zero. A shortage is an
ordinary rejection result, not an exception; an empty order is accepted, and an
empty batch returns copied stock and no outcomes. All counts remain integers.
Neither stock nor nested order contents may be mutated.

Retain the existing JSON decoding and validation before engine invocation. The
engine continues to trust the stated validated-input preconditions: known, unique
SKUs and positive integer quantities. No new validation policies or changes to
existing malformed-JSON/invalid-input errors are proposed. There is no shared or
persistent state; rejected orders leave the batch snapshot usable by later orders.
No persistence, concurrency, infrastructure, or retry protocol is needed.

Inspection found that `inventory.py` already copies stock once, but unconditionally
deducts items and always returns true. `batch.py` decodes the complete JSON batch
through `command_codec.py` before calling that engine. The change belongs in the
engine, so both APIs receive the same behavior without an adapter redesign.

## Decisive acceptance

Exercise the same valid scenarios through both APIs and compare complete stock and
ordered result values, not just the number of successes:

- The opening example catches partial deduction when the shortage is the second
  item, confirms continuation, and accepts an empty order.
- With `{"a":4}`, sequential requests for `a:3`, `a:2`, and `a:1` yield
  `[True, False, True]` and `{"a":0}`. Availability must reflect earlier successes,
  and a rejected order must consume nothing.
- With `{"a":0}`, a request for `a:1` rejects and leaves zero. All-sufficient
  multi-item orders still deduct every item, including exact-stock requests.
- Empty batches and empty orders preserve stock. For successes and rejections,
  compare stock and nested order inputs against deep copies; verify integer stock
  counts and boolean outcomes. Retain existing JSON validation regressions and
  verify the inspected validation contract remains unchanged.

## Preserved accepted design (D1)

The following original text is retained as historical context. D2 replaces only
its sufficient-inventory responsibility; its validation and state decisions remain.

> # Accepted design D1
> The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
> The engine trusts validated orders and copies stock once for batch-local mutation.
> Sufficient inventory is currently the caller's responsibility. The function returns
> one boolean acceptance result per order and does not mutate caller inputs.
