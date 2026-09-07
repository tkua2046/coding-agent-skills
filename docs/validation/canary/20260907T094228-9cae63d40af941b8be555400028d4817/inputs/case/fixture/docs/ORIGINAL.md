# Accepted reservation behavior
`inventory.reserve(stock, orders)` returns a copied stock dictionary and one
{"order_id":id,"accepted":True} result per processed order. IDs and item SKUs are
unique within their respective containers; the adapter validates JSON and positive
integer quantities before invoking the engine. The stock is nonnegative on input.
Previously callers guaranteed sufficient inventory; the engine itself can go negative.
Keep integer counts, order sequence, input immutability, and the JSON adapter.
