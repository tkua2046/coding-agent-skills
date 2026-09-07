# Current contract
See ORIGINAL.md for accepted behavior. Reservation uses batch-local state and returns
remaining stock and ordered outcomes. No persistent database or concurrent writers.

## Requested extension (planned; not yet implemented)

[REQUEST.md](REQUEST.md) supersedes only the caller-sufficiency precondition in
[ORIGINAL.md](ORIGINAL.md). For each order in input sequence, compare every requested
quantity with current batch-local remaining stock. If any item is insufficient,
append `{"order_id": id, "accepted": False}` and leave all stock unchanged by that
order. Otherwise deduct every item and append the same shape with `accepted: True`.
Continue after rejection using stock left by prior successful orders. Empty orders
are accepted without mutation; quantities equal to available stock are sufficient.

Preserve both public APIs, return shape and result order, input immutability, integer
counts and existing JSON validation/error behavior. Validated input shapes, positive
quantities and known unique SKUs remain preconditions; add no validation policies.
Persistence, concurrency, transaction frameworks and remote infrastructure are out
of scope. See [DESIGN.md](DESIGN.md#decisive-acceptance) for acceptance examples.
