# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining inventory, the whole order returns `accepted=False`
and deducts nothing. Later orders continue against the remaining stock. Successful
orders deduct all their items and return `accepted=True`; empty orders are accepted
without changing stock.

For example, with stock `{"a": 3, "b": 1}`, an order requesting two of each SKU
is rejected and leaves both quantities unchanged. A following order requesting
three of `a` and one of `b` is accepted and leaves both quantities at zero.
See DEVNOTES.md for checks.
