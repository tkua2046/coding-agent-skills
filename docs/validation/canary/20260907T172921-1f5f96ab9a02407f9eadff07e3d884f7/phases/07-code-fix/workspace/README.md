# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining inventory, the entire order is rejected with
`accepted=False` and consumes no stock. Later orders continue against the inventory
left by successful orders. Exact-fit and empty orders are accepted.

For example:

```python
from inventory import reserve

reserve({"a": 4, "b": 2}, [
    {"id": "first", "items": [["a", 1]]},
    {"id": "reject", "items": [["a", 2], ["b", 3]]},
    {"id": "later", "items": [["a", 3], ["b", 2]]},
])
# ({"a": 0, "b": 0}, [
#     {"order_id": "first", "accepted": True},
#     {"order_id": "reject", "accepted": False},
#     {"order_id": "later", "accepted": True},
# ])
```

See DEVNOTES.md for development checks.

## Unreleased

Orders with insufficient inventory now reject as a whole instead of producing
negative stock counts.
