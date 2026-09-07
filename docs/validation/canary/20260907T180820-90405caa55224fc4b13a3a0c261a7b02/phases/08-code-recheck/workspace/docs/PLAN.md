# Reservation extension delivery

S1 is implemented: insufficient orders leave all stock unchanged, later orders
continue, and both APIs retain their contracts. Regression tests and usage/current
contract documentation are updated. The installed gate and explicit unittest
command both pass with 9 tests. Independent code review and human review remain
pending; this is not accepted delivery. No document findings are open, and no code
review findings have yet been supplied. Next: the independent agent reviews the
identified candidate and records findings, then any necessary fixes/rechecks precede
human review. No commit, push, version advancement, or release was performed.

## Candidate and checks

- Candidate: base commit `82d1bf03d1cf15929aed6f48e34c62b0be3d677e`, plus
  [captured diff](../reviews/s1/candidate.patch); exact relevant file hashes and
  runtime are in [candidate.json](../reviews/s1/candidate.json). Evidence files
  accompany the diff; the manifest does not hash itself or other evidence.
- The [independent document review](../reviews/design-current.json) is ready with
  no findings. All 15 reviewed file hashes matched at this fresh phase entry.
  [Exact reviewed design/plan text](../reviews/s1/reviewed-documents.json) preserves
  their earlier state. D2 behavior is unchanged; DESIGN now acknowledges the review,
  and this plan now records implementation progress. Prior reports remain intact.
- On 2026-09-07, `"$CANARY_PYTHON" hooks/pre-commit` passed the unchanged baseline
  with 6 tests: [output](../reviews/s1/baseline.txt).
- After implementation, `"$CANARY_PYTHON" hooks/pre-commit` passed with 9 tests,
  exit 0: [output](../reviews/s1/gate.txt). The gate rejects empty collection and
  made no automatic changes.
- `"$CANARY_PYTHON" -m unittest discover -s tests -v` also passed with 9 tests,
  exit 0: [output](../reviews/s1/unittest.txt).
- `git diff --check` passed, exit 0. Git emitted sandbox warnings about its
  external Xcode cache; the diff check itself completed successfully. Initial
  staged whitespace checking flagged a diff context line and test-runner trailing
  space in new evidence. The snapshot now uses zero context, and trailing output
  whitespace was trimmed; `git diff --cached --check` then passed.
- Regression sensitivity: an in-memory replacement of both API engine references
  with the original unconditional-deduction function ran
  `InventoryTests.test_whole_order_rejection_and_sequential_stock`. It produced
  four expected assertion failures (both APIs, both item orders), no errors:
  [output](../reviews/s1/regression-original.txt). Files were not changed by this
  probe. Final checks above exercised the actual implementation.
- New coverage verifies exact remaining inventory and ordered boolean outcomes,
  all-or-nothing rejection, current-stock sequencing, nested input preservation,
  independent returned stock, integer counts, empty orders/batches, and existing
  JSON validation before any engine invocation. Adapter code and policy are unchanged.

## Scope and review policy

Sources: [request](REQUEST.md), [original requirements](ORIGINAL.md),
[reviewed design](DESIGN.md), and [operations](../DEVNOTES.md). S1 is the single
local engine/test/documentation increment. No persistence, concurrency, transaction
framework, adapter redesign, dependencies, or external services are included.
The user supplies the next independent code reviewer; no independent code review
was performed by this implementing agent. Human review stays pending afterward.
The request forbids committing and allows agent-only review during work.

## Preserved planning evidence (before document review)

- Planning prepared; independent document review, S1 implementation, new tests,
  code review, and human review remain pending. No implementation changes made.
- Inspected `inventory.py`, `batch.py`, `command_codec.py`,
  `tests/test_inventory.py`, and `hooks/pre-commit`. The engine copies stock once
  but deducts unconditionally. The adapter decodes the whole batch before calling
  it. Existing tests cover success, empty batch, adapter success, unknown SKU,
  duplicate SKU, and boolean quantity rejection, but no insufficient-stock case.
- Baseline on 2026-09-07: both commands above passed, each discovering 6 tests.
  The gate explicitly rejects empty discovery. These passes do not establish D2.
- A read-only engine probe of the design's four-order example returned
  `{"a":-3,"b":-2}` with all four flags `True`, confirming the requested gap.
  D2 instead requires `{"a":0,"b":0}` and `[False,True,False,True]`.
- The implementer should record final check results and delivery status here;
  preserve any reviewer reports and their findings/dispositions rather than
  replacing them with author self-check claims.

## Preserved progress

See [completed S0](history/completed.md). The original plan below is retained
verbatim as historical context, not the current pending-work status.

# Plan
S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.
