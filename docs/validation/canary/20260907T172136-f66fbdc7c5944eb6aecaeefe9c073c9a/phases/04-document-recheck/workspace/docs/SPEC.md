# Current contract
See ORIGINAL.md for accepted behavior. Reservation uses batch-local state and returns
remaining stock and ordered outcomes. No persistent database or concurrent writers.

## Requested amendment (pending implementation)

[REQUEST.md](REQUEST.md) supersedes the caller-guaranteed sufficiency requirement
in [ORIGINAL.md](ORIGINAL.md). For `inventory.reserve(stock, orders)` and
`batch.execute(stock, text)`, process orders in input order against batch-local
remaining stock. If any requested quantity exceeds its available count, return
`{"order_id": id, "accepted": False}` for that order and leave every stock quantity
unchanged by it. Otherwise deduct every item and report `accepted=True`. Continue
after rejection. An empty order succeeds without deductions; an empty batch returns
a stock copy and no outcomes.

Preserve the tuple of remaining-stock dictionary and ordered outcome list, integer
counts, and all caller inputs (including nested items). Keep the existing validated
input assumptions and JSON validation policies and errors: malformed JSON/shapes,
duplicate IDs/SKUs, unknown SKUs, and invalid quantities fail before reservation.
Insufficient inventory is a normal rejection outcome, not a validation exception.

## Decisive acceptance

Run this same valid batch through the Python API and the JSON adapter with stock
`{"a": 4, "b": 1}`:

| Order ID | Items in order | Accepted | Remaining stock after order |
|---|---|---|---|
| first | `[["a",1]]` | `True` | `{"a":3,"b":1}` |
| reject | `[["a",2],["b",2]]` | `False` | `{"a":3,"b":1}` |
| later | `[["a",3],["b",1]]` | `True` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

The returned outcomes must contain those four IDs and booleans in that order;
final stock is exactly `{"a":0,"b":0}`. Stock and nested orders remain equal to
their pre-call values. Also check sequential depletion explicitly: stock `{"a":2}`
with orders requesting 2 then 1 yields `True, False` and `{"a":0}`. This catches
availability checks against original rather than remaining stock. An isolated
rejected mixed order leaves all stock unchanged. Exact equality succeeds, empty
inputs keep their established behavior, and all returned counts have type `int`.

Retain validation regression checks through `batch.execute`: malformed JSON and
invalid shapes, duplicate IDs/SKUs, unknown SKUs, and zero/negative/noninteger
quantities (including booleans) still raise the existing errors. A later invalid
order still prevents execution of the batch at the decoder boundary.
