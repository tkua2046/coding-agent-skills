# Whole-order inventory reservation

Reject an order if any item exceeds the stock remaining when that order begins.
Check every item's sufficiency before deducting any items; this keeps rejection
free of partial deductions without rollback machinery. Accepted orders deduct all
items, and later orders use the resulting batch-local stock. This adds a read pass
for successful orders while retaining linear work in the number of requested items.

Decisive example: with stock `{"a":4,"b":1}`, process these orders in sequence:

| Order | Items | Acceptance | Stock afterward |
|---|---|---|---|
| reject | `[["a",2],["b",2]]` | `False` | `{"a":4,"b":1}` |
| later | `[["a",4],["b",1]]` | `True` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

The result must contain all three IDs in this order. Placing the insufficient item
second makes a partial deduction observable; the next order proves continued
processing and acceptance at exact availability.

Decision: proposed extension D2, pending independent document review.
Sources: unchanged [request](REQUEST.md), [original contract](ORIGINAL.md), and
[prior accepted design D1](history/design-d1.md). Delivery and check evidence:
[plan](PLAN.md).

## Compatibility and boundaries

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)`, their
return tuple, stock dictionary and ordered `{"order_id":id,"accepted":bool}`
records. Continue copying stock once and preserve caller stock and nested order
data. Counts remain integers. An empty batch returns the copied stock and no
outcomes; an empty order succeeds without mutation, including with empty stock.

The engine continues trusting validated input. `command_codec.decode` still
validates the complete JSON batch before reservation; malformed input keeps its
existing error behavior. Insufficient inventory becomes a normal `False` outcome,
not a validation error or an exception. No new validation is needed: positive
quantities and unique known SKUs make per-item sufficiency checks sufficient.

Batch-local state and single-process execution make check-before-deduct sufficient
for the requested whole-order behavior. No persistence, concurrency, transaction
framework, dependency or remote service is involved. D2 supersedes only D1's
caller-sufficiency assumption and unconditional success behavior. There are no
unresolved material decisions requiring user input.
