# Export limit amendment — draft

Add optional `limit` to return the first N rows, following [REQUEST.md](../REQUEST.md).
Keep full-input parsing and validation, then select the prefix: an invalid later
row still fails, including with `limit=0`. This preserves accepted D1 below;
the limit reduces returned rows but not full-input parsing or validation cost.
This amendment is proposed, design only; implementation has not changed.
Next step: implement the optional argument and verify the acceptance examples.
For example, `sku,quantity\nA,2\nB,-1\n` with `limit=1` must fail,
not return A. No streaming, dependencies, or rendering changes are in scope.

Contents: [Contract and rationale](#contract-and-rationale) ·
[Acceptance](#acceptance) · [Accepted D1](#accepted-export-design-d1)

## Contract and rationale

Inspection of [exporter.py](../exporter.py) confirms that `export_rows(text)`
materializes `csv.DictReader` rows, then checks each SKU and quantity before
returning the list in source order. Values remain strings. Rendering belongs
to the caller; this change introduces no persistent state.

Proposed interface: `export_rows(text, limit=None)`. Omission or `None` means
unlimited; a nonnegative integer selects at most that many rows. Zero returns
an empty list only after successful validation; a limit exceeding the row
count returns all rows. Existing one-argument calls retain their behavior.
Reject negative and non-integer limits before processing CSV, without coercion.
Proposed API details (assumptions, not specified by the request): use
`ValueError` for invalid limits and reject booleans despite Python's `bool`
subclassing `int`; explicit `None` is the unlimited sentinel.

Keep existing CSV parsing and stock validation behavior, including existing
exception types; do not broaden validation or normalize errors in this change.
Apply the prefix only after the entire input passes those checks. Stopping
after N rows is an alternative that could save work, but violates the explicit
requirement to fail on malformed later rows. Full materialization retains the
existing memory cost even for a small or zero limit.

## Acceptance

For input `sku,quantity\nA,2\nB,0\n`, verify:

| Limit | Expected result |
| --- | --- |
| Omitted or `None` | `[{"sku": "A", "quantity": "2"}, {"sku": "B", "quantity": "0"}]` |
| `1` | `[{"sku": "A", "quantity": "2"}]` |
| `0` | `[]` |
| `3` | Both rows, identical to unlimited output |
| `-1`, `1.5`, `"1"`, or `True` | `ValueError`; no result |

For `sku,quantity\nA,2\nB,-1\n`, both `limit=1` and `limit=0` must raise
`ValueError`, with no partial result. Replacing `-1` with `oops` or removing
B's SKU must likewise fail even beyond the prefix. Header-only input
`sku,quantity\n` returns `[]` for omitted, zero, and positive limits.

At implementation time, exercise these examples and compare unlimited calls
and malformed-row failures with the existing behavior. Evidence here is source
inspection; the proposed interface and examples have not been implemented or
tested. No unresolved requirement blocker was found; the API assumptions above
are explicit draft choices. CSV behavior outside the existing validation is
unchanged and outside this amendment's scope.

## Accepted export design D1
CSV rows are fully parsed and validated before being returned in source order.
The caller owns output rendering. Invalid stock rows fail the request.
This decision is accepted; no delivery status is tracked here.
