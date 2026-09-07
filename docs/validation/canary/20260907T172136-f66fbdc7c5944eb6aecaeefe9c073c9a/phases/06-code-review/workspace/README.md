# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
Each order is checked against the remaining stock. If any item is insufficient,
the whole order returns `accepted=False` without deducting any stock. Later orders
continue against the remaining inventory. Successful orders deduct all their items
and return `accepted=True`; an empty order is accepted without changing stock.

For example:

```python
batch.execute({"a": 2}, '[{"id":"large","items":[["a",3]]},{"id":"next","items":[["a",2]]}]')
# ({"a": 0}, [{"order_id": "large", "accepted": False},
#             {"order_id": "next", "accepted": True}])
```

Insufficient inventory is a normal result, not a JSON validation error.
See DEVNOTES.md for development checks.
