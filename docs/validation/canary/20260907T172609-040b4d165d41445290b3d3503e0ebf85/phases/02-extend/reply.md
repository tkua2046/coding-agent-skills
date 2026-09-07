Revised `docs/DESIGN.md`, `docs/SPEC.md`, and `docs/PLAN.md` using both supplied skills. Preserved prior documents and reports in `docs/history/pre-yaml-documents.md`.

The proposal validates the entire YAML before consuming commands and reuses immutable occupancy for expected O(1) movement queries. The plan includes 200,000-cell memory and startup measurements.

Open questions include parser dependency policy, strict values, duplicates, occupied starts, and supported YAML features—with examples in the spec.

All 3 baseline tests passed. Reviews remain pending. No implementation, dependency installation, commits, or external actions occurred.