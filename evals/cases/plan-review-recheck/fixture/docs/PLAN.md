# Plan P2
Author claim: R1 fixed by documenting the exporter prerequisite.
Next: enable Client A JSON; accept when A imports SKU strings and integer quantities.

| Order / outcome | Dependency / boundary | Acceptance |
|---|---|---|
| 1. Enable A JSON | Requires exporter JSON support; separately owned A deployment | A imports SKU strings and integer quantities including zero |
| 2. Deploy exporter JSON option | Must be available before A opts in; exporter owner | Explicit JSON preserves SKU strings and integer quantities including zero; malformed quantities fail before any output; default CSV stays byte-identical for B. Include exporter checks and user option docs |

The table is execution order. Both rows are pending. No implementation has begun.
Sources: [request](ORIGINAL.md), [design](DESIGN.md), [original finding](history/R1.md).
