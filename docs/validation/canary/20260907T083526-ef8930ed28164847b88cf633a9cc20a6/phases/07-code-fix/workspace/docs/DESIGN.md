# Design: whole-order inventory rejection

Amendment D2 passed [independent document review](../reviews/design-current.json)
with no findings. Implementation is ready for code review; current evidence and
pending reviews are in the [S1 handoff](../reviews/s1-handoff.md).
[REQUEST.md](REQUEST.md) is the unchanged feature authority;
[ORIGINAL.md](ORIGINAL.md) preserves the original requirements. Next outcome:
[PLAN.md](PLAN.md#s1-whole-order-rejection-implemented-review-pending) delivers rejection without
partial deductions, followed by human review. A short amendment and one stage are
appropriate because this is a local, in-memory change with unchanged interfaces.

## D2: behavior and rationale

Keep the batch-local stock copy. For each validated order, check all requested
quantities against the current remaining stock before making any deductions. If
any quantity exceeds availability, append `{"order_id": id, "accepted": False}`
and leave the entire remaining dictionary unchanged by that order. Otherwise
deduct every requested quantity and append the same result shape with `True`.
Continue processing later orders in input order. Equality is sufficient; an empty
order succeeds without changing stock. Previously accepted deductions survive a
later rejection. Nonnegative input stock therefore remains nonnegative, and all
counts remain integers.

Prechecking avoids partial mutation and rollback bookkeeping. A per-order stock
copy would also work but would copy unrelated stock for every order; it is
unnecessary given validated unique SKUs. Use ordinary checks and deductions,
without new dependencies or a transaction abstraction. Validation ensures item
lists are reusable and SKUs are unique within each order; the Python API continues
to trust these preconditions rather than introducing new validation policies.

Both `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` retain
their signatures and `(remaining, outcomes)` return shape. Neither caller stock
nor nested order data is mutated. Insufficient stock is a normal `False` outcome,
not an exception. `command_codec.decode` continues validating the entire JSON
batch before reservation, with existing errors for malformed input. Persistence,
concurrency, remote infrastructure and changes to validation remain out of scope.

## Decisive acceptance

Exercise the following batch through both APIs (JSON-encode the orders for
`execute`). Begin with `{"a": 5, "b": 1}`:

| Order ID | Items | Accepted | Remaining after order |
| --- | --- | --- | --- |
| first | `[["a", 1]]` | `True` | `{"a": 4, "b": 1}` |
| reject | `[["a", 3], ["b", 2]]` | `False` | `{"a": 4, "b": 1}` |
| later | `[["a", 4], ["b", 1]]` | `True` | `{"a": 0, "b": 0}` |
| empty | `[]` | `True` | `{"a": 0, "b": 0}` |
| exhausted | `[["a", 1]]` | `False` | `{"a": 0, "b": 0}` |

The final result must contain exactly these IDs and booleans in this order and
the final stock above. This checks rejection when a later item is insufficient,
preservation of earlier success, continued processing, exact depletion, empty
orders and zero availability. Compare stock and nested orders with independent
snapshots afterward and assert integer stock counts. Keep empty-batch behavior
and successful multi-item reservation. Invalid JSON batches, including a valid
prefix followed by an invalid order, must still raise before reservation without
mutating input stock; preserve shape, ID, SKU and quantity validation semantics.

## Inspection and limits

Before implementation on 2026-09-07, inspected `inventory.py`, `batch.py`,
`command_codec.py`, existing tests and the local gate. At that baseline,
`reserve` unconditionally deducted each item;
`execute` decodes the full batch before calling it. Both baseline commands in
[PLAN.md](PLAN.md#verified-baseline) pass, but do not verify D2. No material design
questions remained from that inspection; subsequent document review approved D2
for implementation. Code and human review remain pending. The accepted design
below is historical and its sufficient-stock precondition is the specific
decision D2 supersedes.

## Accepted design D1 (preserved)
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
