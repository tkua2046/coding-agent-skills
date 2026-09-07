# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return
`(remaining, outcomes)`, with a copied stock dictionary and one
`{"order_id": id, "accepted": bool}` result per order in input order.

Each order is checked against the current remaining stock. If any requested
quantity exceeds availability, reject the whole order with `accepted=False` and
leave all quantities unchanged by that order. Otherwise deduct every requested
item and return `accepted=True`. Continue with later orders; earlier successful
deductions persist. Exact depletion is allowed. An empty order succeeds without
changing stock, and an empty batch returns copied stock and no outcomes.

Caller stock and nested orders remain unchanged; counts remain integers and
nonnegative for valid inputs. The Python API trusts validated input shapes,
positive quantities and known unique SKUs. The JSON adapter validates the whole
batch before reservation, retaining its existing shape, ID, SKU and quantity
errors. Insufficient inventory is a normal rejection, not a validation error.

State is batch-local, without persistence or concurrent writers. This contract
implements [REQUEST.md](REQUEST.md) and the reviewed D2 amendment in
[DESIGN.md](DESIGN.md), superseding only the sufficient-stock obligation in
[ORIGINAL.md](ORIGINAL.md), which remains the historical requirements record.
