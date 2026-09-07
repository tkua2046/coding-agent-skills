# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return
`(remaining, outcomes)`: a copied stock dictionary and one
`{"order_id": id, "accepted": bool}` result per order, in input order.

An order is accepted only when every requested quantity is available in the stock
remaining after earlier accepted orders. Acceptance deducts all requested items;
a shortage rejects the whole order without any deduction or exception. Processing
continues with later orders. Exact depletion to zero is allowed. An empty order is
accepted; an empty batch returns copied stock and no outcomes.

Counts remain integers. Neither stock nor nested order inputs are mutated. The
engine trusts validated input: positive integer quantities, known unique item SKUs,
unique order IDs and nonnegative initial stock. The JSON adapter still validates the
complete batch before invoking the engine, with unchanged decoding and validation
errors. Reservation uses batch-local state, with no persistence or concurrency.

[REQUEST.md](REQUEST.md) supplies the shortage extension to the preserved
[original requirements](ORIGINAL.md); [DESIGN.md](DESIGN.md) explains the decision.
