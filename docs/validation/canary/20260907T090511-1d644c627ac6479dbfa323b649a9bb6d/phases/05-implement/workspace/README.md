# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining stock, the whole order returns `accepted=False`
without deducting any items. Later orders continue against the remaining stock.
Successful orders deduct all items and return `accepted=True`; empty orders are
accepted without changing stock. See DEVNOTES.md for checks.
