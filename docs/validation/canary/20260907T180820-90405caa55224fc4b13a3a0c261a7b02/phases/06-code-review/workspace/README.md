# Batch inventory reservation
Call `batch.execute({"a": 4}, '[{"id":"o1","items":[["a",2]]}]')` to obtain
remaining inventory and an ordered acceptance result for each order. The Python API
is `inventory.reserve(stock, orders)`. Caller input is preserved. JSON validation
rejects unknown/duplicate SKUs and nonpositive/noninteger quantities before execution.

Each order reserves all its items (`accepted=True`) or, if any item has insufficient
stock, reserves nothing (`accepted=False`). Later orders continue against remaining
stock. Exact-stock requests and empty orders are accepted.

For stock `{"a":3,"b":1}`, orders requesting `a:2,b:2` then `a:3,b:1` produce
acceptance flags `[False, True]` and remaining stock `{"a":0,"b":0}`.
See [the current contract](docs/SPEC.md) for details and [DEVNOTES.md](DEVNOTES.md)
for checks.

## Unreleased
Orders exceeding available stock are now rejected as a whole without consuming
inventory; processing continues with later orders.
