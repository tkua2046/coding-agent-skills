# Current contract

`inventory.reserve(stock, orders)` and `batch.execute(stock, text)` return
`(remaining, outcomes)`. Remaining stock is a new dictionary; caller stock and
orders, including nested item lists, are unchanged. Outcomes contain one
`{"order_id": id, "accepted": boolean}` dictionary per order in input order.

Compare every requested quantity with current remaining stock before deducting
anything in an order. If any item is insufficient, return `accepted=False` and
leave all stock unchanged by that order. Otherwise deduct every item and return
`accepted=True`. Continue with later orders against stock left by earlier successful
orders. Exact availability is sufficient. Counts remain nonnegative integers for
validated inputs. Empty orders are accepted; empty batches return a copied stock
dictionary and no outcomes.

The JSON adapter validates the entire batch before invoking the engine, preserving
existing validation errors. Shapes, unique string order IDs, known unique item
SKUs, and positive integer quantities (excluding booleans) are required. The engine
trusts those validated inputs. Insufficient stock is an ordinary rejected outcome,
not a validation exception. No new validation policy is introduced.

State is batch-local and in memory; persistence and concurrency are outside this
contract. [Original requirements](ORIGINAL.md) remain preserved; the
[requested extension](REQUEST.md) supersedes unconditional acceptance and the
sufficient-stock caller precondition. See [design rationale](DESIGN.md).
