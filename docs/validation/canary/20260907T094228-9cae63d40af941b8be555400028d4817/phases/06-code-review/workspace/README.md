# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining stock, the whole order returns `accepted=False`
and deducts nothing. Later orders continue against the remaining stock. Successful
orders deduct all their items and return `accepted=True`; exact-stock requests and
empty orders succeed. For example, starting with `{"a": 4, "b": 1}`, an order for
three `a` and two `b` is rejected, leaving all four `a` and one `b` available for
the next order. The direct Python API expects already validated orders.
