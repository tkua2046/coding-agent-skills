# Development

Python standard library only. The existing `reserve_batches(stock, batches)` API returns `(remaining_stock, accepted_flags)`; callers supply validated SKU maps with positive integer quantities, and missing stock keys mean unavailable. Retain the return shape and caller-input isolation while fixing rejected-batch behavior.

Run `python -m unittest discover -s tests -v` from the root. Include acceptance checks for the changed behavior in the same increment. Before committing, the gate must pass and an independent code review must resolve material findings. This repository has no additional hook or coverage threshold.
