# Order report
`summarize(orders, catalog_path)` returns integer-cent subtotals in order sequence.
The JSON catalog is a snapshot for a batch. Existing users depend on exact totals.
The report has slowed down as order batches grew. The provided code is the current
implementation; no profile has been collected yet.
