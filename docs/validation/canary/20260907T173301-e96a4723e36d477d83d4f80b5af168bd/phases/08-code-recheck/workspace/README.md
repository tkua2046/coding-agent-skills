# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining stock, the whole order is rejected with
`accepted=False` and consumes nothing. Later orders continue against stock left
by successful orders, which return `accepted=True` and deduct all their items.
An empty order is accepted. See DEVNOTES.md for checks.

For example, `batch.execute({"a": 2}, '[{"id":"large","items":[["a",3]]},{"id":"fits","items":[["a",2]]}]')`
returns `({"a": 0}, [{"order_id": "large", "accepted": False}, {"order_id": "fits", "accepted": True}])`.

## Unreleased

Orders exceeding inventory now reject as a whole instead of producing negative stock.
