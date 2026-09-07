# Current contract
`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return a copied
remaining-stock dictionary and one `{"order_id": id, "accepted": boolean}` outcome
per order, in input order. Neither API mutates caller inputs. Counts remain integers.

Each order is checked against stock remaining after earlier successful orders. If
any requested quantity exceeds availability, its outcome is `accepted=False` and
none of its items are deducted. Otherwise all items are deducted and its outcome is
`accepted=True`. Exact availability succeeds. Later orders continue after rejection.
An empty order succeeds without changing stock; an empty batch returns copied stock
and no outcomes.

The JSON adapter validates the entire batch before reservation. Existing shape,
positive integer quantity, unique order ID and unique known SKU checks are unchanged.
Insufficient inventory is a normal rejection, not a validation error. The engine
trusts validated inputs and introduces no new validation policies.

This extends [the original contract](ORIGINAL.md) by replacing caller-guaranteed
sufficiency with whole-order rejection. State remains batch-local and in memory;
there is no persistence or concurrency support. See [design rationale](DESIGN.md).
