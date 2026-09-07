# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return
`(remaining, outcomes)`: a copied stock dictionary and one
`{"order_id": id, "accepted": boolean}` result per order, in input order.

Each order checks all requested quantities against current batch-local stock before
deduction. If any item is insufficient, the whole order returns `accepted=False`
and changes no stock. Otherwise all items are deducted and it returns
`accepted=True`. Later orders continue using stock left by successful orders.
Exact availability and empty orders succeed; an empty batch returns copied stock
and no outcomes. Integer counts remain integers and nonnegative for valid inputs.
Caller stock and nested orders are unchanged.

The engine trusts validated input: nonnegative stock, positive integer quantities,
known unique item SKUs and unique order IDs. The JSON adapter validates the entire
payload before invoking the engine; its shapes, errors and validation policies are
unchanged. Insufficiency is a normal order rejection, not a validation error.

This is single-process, in-memory behavior; persistence and concurrency are outside
the contract. [ORIGINAL.md](ORIGINAL.md) preserves the original requirements; its
caller-sufficient-inventory assumption is superseded by [REQUEST.md](REQUEST.md).
