# Inventory reservation request

Orders may now exceed available stock. If any requested item is insufficient,
return accepted=False for that whole order and leave every stock quantity unchanged
by it. Later orders continue against the remaining stock, including earlier
successful deductions. Successful orders deduct all their items and return
accepted=True. An empty order is accepted without changing stock.

Both inventory.reserve(stock, orders) and batch.execute(stock, text) have callers.
Preserve their signatures, result ordering, caller input immutability, integer
counts and existing JSON validation. The Python engine receives already validated
positive quantities and unique known SKUs. The utility runs inside one process.
