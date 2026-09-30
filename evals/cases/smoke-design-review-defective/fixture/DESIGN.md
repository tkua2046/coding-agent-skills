# Ordering worksheet — D1
Add optional --needs-order, including quantity == reorder_at. Default export remains unchanged.
In the flag path, parse quantity/reorder_at and discard stocked rows before checking labels,
row shape and duplicate SKUs. Validate retained rows, preserving source order, then use
the existing atomic writer. No matches produce []. For duplicate SKU X in a discarded
stocked row followed by retained X, only retained X participates in duplicate checks.
This reduces validation work to worksheet rows. No streaming or database is proposed.
