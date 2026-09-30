# Ordering worksheet request

Confirmed local request, 4 September 2026.

Add `--needs-order` to the existing inventory CSV exporter. With the flag, export
only rows whose quantity is less than or equal to reorder_at. Equality counts.
Keep the existing row shape, order, normalization, JSON encoding and success/error
exit codes. Without the flag, the existing complete export stays the default.
The flag is optional; a header-only file or no matching rows succeeds with `[]`.

An export still validates the entire input. A duplicate SKU, missing required
field, malformed number or bad row anywhere is an error, including rows that
would not appear in an ordering worksheet. An error must preserve the previous
destination bytes. For example, an in-stock row with a duplicate SKU cannot be
silently omitted to make a file appear valid.

This is a small local extension for the current in-memory files, normally fewer
than 2,000 rows. Retain the existing all-or-nothing export boundary. No streaming
optimization, database, pricing, stock synchronization or order submission.
The CLI help and README should explain the flag when the feature is implemented.
The author has supplied D1 and P1 for one combined design/plan review. Review is
authorized now; implementation will be assigned as a separate task afterward.
