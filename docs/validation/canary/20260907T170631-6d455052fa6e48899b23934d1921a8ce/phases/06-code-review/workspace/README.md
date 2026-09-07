# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.

An order with any insufficient item returns `accepted=False` and deducts nothing.
Later orders continue against the remaining stock. Successful orders deduct every
item and return `accepted=True`; empty orders succeed without changing stock.
For example, with `{"a":4,"b":1}`, an order requesting `[["a",2],["b",2]]`
is rejected, leaving enough stock for a later order requesting `[["a",4],["b",1]]`.
See DEVNOTES.md for checks.

## Unreleased

Insufficient orders are now rejected as a whole instead of producing negative stock.
