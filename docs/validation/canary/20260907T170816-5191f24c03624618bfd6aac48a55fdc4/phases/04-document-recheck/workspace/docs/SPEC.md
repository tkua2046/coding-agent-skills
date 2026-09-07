# Current contract
See ORIGINAL.md for accepted behavior. Reservation uses batch-local state and returns
remaining stock and ordered outcomes. No persistent database or concurrent writers.

## Requested extension (target contract; implementation pending)

[REQUEST.md](REQUEST.md) supersedes only the original caller-sufficiency assumption.
For each order in sequence, compare all quantities with current remaining stock.
If any item is insufficient, return `{"order_id":id,"accepted":False}` and leave
every stock quantity unchanged by that order. Otherwise deduct all its items and
return `{"order_id":id,"accepted":True}`. Continue processing later orders against
the remaining stock. Empty orders are accepted without changing stock.

Preserve `inventory.reserve(stock, orders)` and `batch.execute(stock, text)`, return
shapes, ordered outcomes, caller-input immutability, integer counts and existing JSON
validation. Inputs to the engine already satisfy the validated shapes, positive
quantities and known unique SKUs; no new validation policy is introduced.
See [design acceptance](DESIGN.md#decisive-acceptance) for concrete expected results.
