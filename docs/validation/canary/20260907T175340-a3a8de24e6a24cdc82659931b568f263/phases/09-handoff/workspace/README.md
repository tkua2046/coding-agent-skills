# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.
If any item exceeds remaining stock, that entire order returns `accepted=False`
and consumes nothing. Later orders continue against stock left by earlier accepted
orders. Successful orders deduct all their items; empty orders are accepted.

For example, with stock `{"a":4,"b":1}`, orders requesting `a:2,b:2`, then `a:4`,
then no items produce acceptance results `[False, True, True]` and remaining stock
`{"a":0,"b":1}`. Each result retains its order ID in input order.

See [DEVNOTES.md](DEVNOTES.md) for checks.
