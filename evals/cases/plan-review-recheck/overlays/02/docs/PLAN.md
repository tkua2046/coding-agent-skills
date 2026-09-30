# Plan P3
Author claim: R1 fixed by ordering the available exporter before A rollout and retaining legacy-client acceptance.
Next: deploy exporter support for opt-in JSON alongside default CSV. No new prerequisite is needed; accept explicit JSON preserving SKU strings and integer quantities including zero, malformed input failing before output, and byte-identical default CSV for B.

| Order / outcome | Dependency / boundary | Acceptance |
|---|---|---|
| 1. Deploy exporter JSON option | Existing CSV exporter; independently deployable prerequisite for A | JSON preserves SKU strings and integer quantities including zero; malformed quantities fail before any output; B with no format option receives byte-identical CSV. Include exporter checks and option/compatibility docs |
| 2. Enable A JSON | Stage 1 deployed and verified available before A changes; separate client ownership | A opts in and imports SKU strings and integer quantities including zero; verify B still receives byte-identical default CSV during A rollout. Include integration checks and A rollout docs |

Both rows are pending. CSV removal and B migration are out of scope. No implementation has begun.
Sources: [request](ORIGINAL.md), [design](DESIGN.md), [original finding](history/R1.md).
