# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.

If any item exceeds remaining inventory, the whole order returns `accepted=False`
and deducts nothing. Later orders continue against the remaining stock. Successful
orders deduct every item and return `accepted=True`; empty orders also succeed.
For example, with stock `{"a":4,"b":1}`, an order requesting `a:3,b:2` is rejected;
a following order requesting `a:2` succeeds, leaving `{"a":2,"b":1}`.
See [DEVNOTES.md](DEVNOTES.md) for checks.
