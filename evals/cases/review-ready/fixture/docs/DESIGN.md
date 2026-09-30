# Ordering worksheet export — D1

Proposed next increment: add optional `--needs-order` to export rows at or below
their reorder point. Validate the whole CSV before selecting rows; then reuse the
existing atomic JSON writer. This keeps errors in omitted rows visible and keeps
the previous export safe. The ordinary complete export remains the default.

Next action: review this decision together with [P1](PLAN.md); if sufficient, the
separately assigned implementation can deliver the flag, regression tests and
usage update as one local increment. This document records decisions, not results.

## Contract and choice

[The confirmed request](ORIGINAL.md) owns the behavior. load_inventory already
validates all rows, trims labels and rejects duplicates before returning a list.
Keep that boundary. Select on the validated integers using quantity <= reorder_at,
after loading, only when the flag is present. Pass the selected list to
write_export without changing its replace/cleanup behavior or public row shape.

Filtering raw CSV rows would allow an invalid omitted row to escape validation;
that conflicts with the request. The existing in-memory path is adequate for the
stated file sizes. No lazy reader, new dependency or additional component is needed.

## Decisive examples

For examples/stock.csv, default output keeps B2, A1, C3 in that order; the flag
keeps A1 and C3. C3 demonstrates equality. An all-in-stock or header-only file
exports `[]` with success when the flag is set.
If an in-stock row repeats A1 after a valid A1 row, both modes must fail with code
2 and leave an existing destination byte-for-byte unchanged. The same applies to
malformed rows, including ones beyond the last selected item.

## Limits

There is no partial export and no change to destination-directory requirements.
Success still reports the exported row count. CLI help and README gain the option
and the whole-file validation caveat when implemented. Tests and check evidence
belong with the increment; this static design does not establish a passing runtime.
