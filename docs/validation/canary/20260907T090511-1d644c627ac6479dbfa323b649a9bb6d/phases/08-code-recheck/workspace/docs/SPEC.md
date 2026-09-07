# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return
`(remaining, outcomes)`: a distinct stock dictionary and one
`{"order_id": id, "accepted": bool}` result per order in input order.

An order succeeds exactly when every requested quantity is available in the current
batch-local remaining stock. Successful orders deduct all items; if any item is
insufficient, the entire order returns `accepted=False` and deducts nothing. Later
orders continue against the remaining stock. Exact-stock requests succeed, empty
orders succeed without mutation, and empty batches return a stock copy and no results.
Caller stock and nested orders remain unchanged; stock counts remain integers.

The engine trusts validated shapes, nonnegative integer stock, positive integer
quantities, and known unique item SKUs. The JSON adapter validates the whole batch
before execution, retaining existing validation exceptions. Shortage is a normal
false outcome. No new validation policy is introduced.

This supersedes only the caller sufficiency requirement in the historical
[original contract](ORIGINAL.md); see [D2](DESIGN.md) for rationale. Execution is
single-process and in-memory, with no persistence or concurrency guarantees.
