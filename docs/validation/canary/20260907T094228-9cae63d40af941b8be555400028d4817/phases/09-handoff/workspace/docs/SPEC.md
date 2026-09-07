# Current contract
See ORIGINAL.md for accepted behavior. Reservation uses batch-local state and returns
remaining stock and ordered outcomes. No persistent database or concurrent writers.

## Requested contract (implemented; independent code review ready; human acceptance pending)

[REQUEST.md](REQUEST.md) supersedes the original sufficient-stock precondition.
For each order, against stock remaining after preceding accepted orders:

- If any requested quantity exceeds its SKU's available quantity, return
  `{"order_id": id, "accepted": False}` and change no stock for that order.
- Otherwise deduct every requested quantity and return the same result shape with
  `accepted=True`. An empty order succeeds without changing stock.
- Continue in input order, producing one result per order. Preserve integer counts,
  stock and order inputs, the copied return stock, and both existing API signatures.
  The adapter keeps all existing JSON validation and errors. The direct engine
  continues to trust valid shapes, positive quantities and known unique SKUs.

### Decisive acceptance

Run the following valid orders through both `reserve` and `execute` (JSON-encoding
the orders for `execute`). Starting stock is `{"a": 4, "b": 1}`:

| Order ID | Items | Expected accepted | Stock afterward |
| --- | --- | --- | --- |
| reject | `[["a",3],["b",2]]` | `False` | `{"a":4,"b":1}` |
| later | `[["a",4],["b",1]]` | `True` | `{"a":0,"b":0}` |
| depleted | `[["a",1]]` | `False` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

The returned stock is `{"a":0,"b":0}` and results carry those four IDs in order
with booleans `False, True, False, True`. Check the rejected first order alone as
well: its returned stock must equal the initial stock. Its insufficient item occurs
after a sufficient one, exposing accidental partial deduction. The full sequence
establishes continuation, exact-stock success, use of updated stock, and empty-order
acceptance. Check deep equality of original stock and orders after execution and
that returned quantities remain integers. A batch with no orders returns equal but
copied stock and no results.

Retain existing validation regression checks. Confirm malformed JSON, invalid
container/order/item shapes, duplicate order IDs, unknown or duplicate SKUs, and
zero, negative, boolean or noninteger quantities still fail at the JSON boundary
with `ValueError` (including its JSON decoding subclass); caller stock is unchanged.
Valid insufficient orders must return rejection rather than a validation error.
