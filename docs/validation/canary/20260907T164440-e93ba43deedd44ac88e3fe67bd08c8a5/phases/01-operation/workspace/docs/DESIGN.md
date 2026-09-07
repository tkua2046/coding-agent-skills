# Export row limit

Extend `export_rows(text)` to `export_rows(text, limit=None)`: parse and validate
the entire CSV, then return at most the first `limit` rows in source order.
Omitting the limit keeps the unlimited result. Applying the limit after validation
preserves D1's failure behavior: `sku,quantity\nA,1\nB,-1\n` must fail even with
`limit=1`. The limit reduces the returned list only; parsing, validation work and
memory still scale with the full input. Stopping at the prefix would hide invalid
later rows and violate the request.

Decision: the limit extension is proposed; D1 remains accepted. Source:
[REQUEST.md](../REQUEST.md), preserved unchanged. Next implementation outcome:
add the optional argument and verify the acceptance examples below. This note
authorizes no implementation and tracks no delivery status.

## Behavior and acceptance

Inspection of [exporter.py](../exporter.py) confirms that the exporter materializes
`csv.DictReader` rows, validates every row, and returns dictionaries in source
order. Keep that parsing and stock validation behavior, including existing error
propagation. Output rendering remains the caller's responsibility. No streaming
or new dependencies are needed.

Validate the limit before processing CSV. The proposed API uses `None` for
unlimited and accepts nonnegative Python integers, excluding booleans. Reject
negative values and all other types with `ValueError`, without coercing strings
or floats. Boolean rejection and the exception type are explicit API choices
where the source request does not specify Python details. A valid zero limit
still requires full CSV validation. For a valid limit, any stock validation
failure raises instead of returning a partial result.

For `sku,quantity\nA,1\nB,2\n`, let A and B denote the parsed dictionaries
`{"sku": "A", "quantity": "1"}` and `{"sku": "B", "quantity": "2"}`:

| Call / input | Expected result |
|---|---|
| Limit omitted or `None` | `[A, B]` |
| `limit=1` | `[A]` |
| `limit=0` | `[]`, after validating both rows |
| `limit=2` or `limit=3` | `[A, B]` |
| Header only, with `limit=1` | `[]` |
| `limit=-1`, `1.5`, `"1"`, or `True` | `ValueError` |
| Second row changed to `B,-1`, with `limit=1` or `0` | Validation failure; no result |
| Second row changed to `B,oops` or `,2`, with `limit=1` | Validation failure; no result |

## Accepted history (original D1, retained verbatim)

# Accepted export design D1
CSV rows are fully parsed and validated before being returned in source order.
The caller owns output rendering. Invalid stock rows fail the request.
This decision is accepted; no delivery status is tracked here.
