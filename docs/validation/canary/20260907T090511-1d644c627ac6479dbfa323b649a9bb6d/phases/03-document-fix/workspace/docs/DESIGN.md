# Design: whole-order inventory rejection

D2 is proposed for independent review; implementation is pending. Fulfill
[REQUEST.md](REQUEST.md) by checking every item against current batch-local stock
before deducting anything for that order. An insufficient order returns
`accepted=False`, changes no stock, and does not stop later orders. The next outcome
is [S1 in PLAN.md](PLAN.md#s1-planned-whole-order-rejection).

This local, in-memory change needs a short design amendment and one delivery stage;
one independent review can assess both documents. Original requirements and the
accepted D1 below remain historical authorities; D2 supersedes only the caller's
responsibility to guarantee sufficient inventory.

## D2: proposed behavior and rationale

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)`, including
their `(remaining, outcomes)` return shape. Copy stock once per batch as today.
For each order in input order, accept exactly when every requested quantity is at
most the corresponding current remaining quantity. On acceptance, deduct all items;
on rejection, deduct none. Append exactly one `{"order_id": id, "accepted": bool}`
result and continue. An empty order is accepted without mutation; an empty batch
still returns a stock copy and no outcomes. Exact-stock requests succeed.

Use a read-only sufficiency pass followed by deduction only on success. Validated
unique SKUs make per-item checks sufficient; aggregation is unnecessary. This avoids
rollback state and partial deductions when a later item is insufficient. Two passes
remain linear in requested items and need no new dependency or transaction layer.
Atomicity here is only per order in the existing single-process execution model.

`reserve` continues to trust the existing validated input contract: nonnegative
integer stock, known unique item SKUs, positive integer quantities and valid shapes.
Do not add validation policies. `command_codec.decode` continues validating the
whole JSON batch before execution, with existing exceptions for invalid JSON/input;
insufficient inventory is a normal false result, not a validation error. Preserve
caller stock and nested order data, integer counts, and result order. No persistence,
concurrency, infrastructure, version, or release changes are in scope.

## Decisive acceptance

Run this same batch through both APIs, encoding orders as JSON for `execute`.
Start with `{"a": 4, "b": 1}`:

| Order ID | Items | Accepted | Remaining after order |
| --- | --- | --- | --- |
| reject | `[["a",3],["b",2]]` | `False` | `{"a":4,"b":1}` |
| fill | `[["a",4],["b",1]]` | `True` | `{"a":0,"b":0}` |
| depleted | `[["a",1]]` | `False` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

The first order must preserve even the sufficient `a` quantity, allowing `fill` to
consume the original stock exactly. The final return is
`({"a":0,"b":0}, [{"order_id":"reject","accepted":False},
{"order_id":"fill","accepted":True}, {"order_id":"depleted","accepted":False},
{"order_id":"empty","accepted":True}])`.
Check the rejected prefix separately to establish its unchanged stock directly.
Assert original stock and deeply nested orders are unchanged, remaining stock is a
distinct dictionary, and counts retain integer type. Existing successful/empty-batch
and JSON validation behavior must still pass; invalid payloads must still raise
rather than become false outcomes. These expectations follow from the requested
contract, not current engine output.

## Verified baseline and limits

Inspection on 2026-09-07: `inventory.py` copies stock but unconditionally deducts
items and always returns true. `batch.py` delegates after `command_codec.py` validates
the whole batch. Existing tests cover success, empty batches, adapter execution and
selected validation errors; they do not cover shortage rejection or nested input
immutability.

Using the supplied `CANARY_PYTHON`, both
`"$CANARY_PYTHON" -m unittest discover -s tests -v` and
`"$CANARY_PYTHON" hooks/pre-commit` passed all six baseline tests. A read-only probe
of the acceptance batch through both APIs returned `{"a":-4,"b":-2}` with all four
results true, confirming the gap. Inputs remained unchanged in that probe.
These are baseline results, not evidence of D2 completion. No material design
questions remain; independent review and implementation checks are still pending.

## Accepted design D1 (preserved)
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
