# Agreed supplier CSV workflow

The existing direct adjustment API is delivered. CSV preview and confirmed import
are both pending. Preserve the API and its input validation.

The warehouse's read-only pilot can be deployed independently while the service
account has no write permission. Staff use its preview to validate the supplier's
exports. Production import is a later delivery using that preview contract; it
must not bypass preview validation. Write access is unavailable during the pilot.
This operational boundary is agreed, not a question for this planning task.

CSV columns are sku and quantity. A preview validates the entire input, reports
row-specific errors and shows the proposed final quantities. Reject missing
columns, duplicate SKUs, unknown SKUs and non-integer or negative quantities.
A preview with any error is not importable and leaves inventory unchanged.
A valid preview is already useful to staff without an import command.

Later, an explicit confirmation applies the exact validated preview atomically.
Bind confirmation to the previewed file bytes and inventory revision; changed
bytes or stale inventory require a new preview. Rejection leaves stock unchanged.
The write capability is provisioned only for that later deployment. Include
relevant tests and user instructions with each usable delivery.

Example: stock A=4, B=9; CSV A,7 then B,nope yields a row-3 error and stock remains
A=4, B=9. CSV A,7 then B,2 yields a valid preview but still leaves stock unchanged.
After later confirmation of that current preview, stock becomes A=7, B=2.
