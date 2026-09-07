# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining stock, the entire order returns `accepted=False`
without deducting any items. Later orders continue against stock left by successful
orders, which return `accepted=True`. Exact-fit and empty orders are accepted.
See DEVNOTES.md for checks.
