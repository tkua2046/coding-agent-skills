# Current contract
See ORIGINAL.md for accepted behavior. Reservation uses batch-local state and returns
remaining stock and ordered outcomes. No persistent database or concurrent writers.

## Whole-order reservation

[REQUEST.md](REQUEST.md) supersedes the sufficient-inventory precondition in
[ORIGINAL.md](ORIGINAL.md); both source documents remain unchanged.

For each order in input order, compare every requested quantity with the current
remaining stock. If any quantity exceeds availability, append
`{"order_id": id, "accepted": False}` and leave every stock quantity unchanged by
that order. Otherwise deduct all its items and append the same result with
`accepted=True`. Continue after rejection; prior successful deductions remain.
An empty order succeeds without changing stock; an empty batch returns copied
stock and no outcomes. Exact availability is sufficient.

Both `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` keep
their signatures and `(remaining, outcomes)` return shape. Preserve input stock
and nested order data, integer stock counts, and ordered boolean outcomes. With
valid nonnegative starting stock, remaining quantities cannot become negative.
The engine continues to trust validated input. JSON shape, positive integer,
unique ID, and known unique SKU validation and its errors remain unchanged;
shortage is an ordinary rejection, not a validation error. No new validation
policy, persistence, concurrency, or transaction framework is in scope.

Decisive examples: [design acceptance](DESIGN.md#acceptance).
