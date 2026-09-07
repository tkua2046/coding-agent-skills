Revised [DESIGN.md](docs/DESIGN.md), [PLAN.md](docs/PLAN.md), and [SPEC.md](docs/SPEC.md).

The proposal validates the whole YAML file before movement and retains one reusable immutable occupancy set. It explains lookup costs, peak parsing memory, compatibility, and failure/retry behavior.

Unresolved choices include the parser versus standard-library-only policy, strict values such as `x: "2"`, duplicate cells versus duplicate keys, occupied starts, and supported YAML features. Concrete examples are documented.

All 3 existing tests passed; YAML and scale checks remain proposed. Prior reports are preserved and reviews remain pending. No implementation, dependency installation, commits, or external actions occurred.