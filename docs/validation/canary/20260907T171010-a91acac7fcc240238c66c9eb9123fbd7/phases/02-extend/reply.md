Updated `docs/DESIGN.md`, `docs/PLAN.md`, and `docs/SPEC.md`; added fresh baseline evidence while preserving prior reports.

The design proposes complete validation before command consumption and immutable hash-set lookup for 200,000 cells, with parsing memory measured separately. The plan separates occupancy support from YAML integration.

Open questions include strict schema/value rules, duplicates, occupied starts, YAML language features, and the standard-library dependency constraint. Concrete examples are recorded in the design.

All three baseline tests pass. Reviews remain pending. No implementation, dependency installation, commits, or external actions occurred.