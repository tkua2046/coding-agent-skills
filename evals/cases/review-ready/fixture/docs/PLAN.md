# Ordering worksheet increment — P1

Next: implement the complete `--needs-order` option from [D1](DESIGN.md) as one
bounded local increment. Whole-file validation precedes selection and writing.
Deliver the flag, error-preservation regressions and usage together. The existing
exporter and its qa suite are the baseline; this increment is proposed, not run.

## Delivery and dependencies

Keep load_inventory as the validation boundary. Add optional selection of the
validated list in the CLI path, reuse write_export, and update help/README. No
other stage is needed before this increment can satisfy [the request](ORIGINAL.md).
A separate implementation task will authorize code edits; this task reviews P1.

## Acceptance before delivery

- Default output remains B2, A1, C3 for the supplied CSV; the flag yields A1, C3,
  retaining shape/order and including equality. All-in-stock and empty input yield `[]`.
- Invalid input anywhere, including an omitted in-stock duplicate or malformed
  later row, fails with code 2 and preserves an existing destination in both modes.
- Run the existing tools/check.py gate with the prepared interpreter after adding
  these regressions to the unittest suite. Preserve quality.ini's discovery.

Use explicit expected records and pre-existing destination bytes in tests. Review
the affected code and results once, address material findings, and report the
remaining limits. A static plan review is not that later execution evidence.
There is no follow-on optimization, release or commit in this review's scope.
