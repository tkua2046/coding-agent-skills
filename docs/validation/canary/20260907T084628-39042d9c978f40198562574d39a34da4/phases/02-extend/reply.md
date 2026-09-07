Revised [design](docs/DESIGN.md), [pending plan](docs/PLAN.md), and [spec](docs/SPEC.md), preserving prior reports.

The design proposes complete validation before movement and a reusable immutable hash set for roughly 200,000 cells. It explains memory tradeoffs and raises contract questions with examples: scalar validation, duplicates, occupied starts, schema strictness, parser/dependency policy, entry point, and resource targets.

All three baseline tests pass; new behavior remains unverified. Reviews remain pending. No implementation, dependency installation, commits, or external actions occurred.