# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return a tuple
of a copied remaining-stock dictionary and ordered `{"order_id": id,
"accepted": bool}` outcomes, one per order.

Each order is checked against the stock remaining after earlier accepted orders.
If any requested quantity exceeds availability, the order returns `accepted=False`
and changes no stock. Otherwise it deducts all requested quantities and returns
`accepted=True`. Processing continues after rejection. Empty orders are accepted;
empty batches return a stock copy and no outcomes. Counts remain integers.

Caller stock and nested order inputs are unchanged. The engine trusts validated
input; the JSON adapter validates the entire batch before reservation, preserving
its existing shape, unique string ID, unique known SKU and positive integer quantity
rules and error behavior. Insufficiency is an ordinary rejection, not a validation
error. State is batch-local, with no persistence or concurrent writers.

This extends [the original contract](ORIGINAL.md), superseding its caller-sufficiency
assumption and unconditional acceptance. Rationale: [D2](DESIGN.md).
