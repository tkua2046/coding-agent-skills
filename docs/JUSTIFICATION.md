# Why this design

The goal is easier development with clear decisions and correct results. The previous delivery failed that goal: 38 skill resources were surrounded by 31,660 validation archive paths. Local checks passed, but no effective whole-deliverable acceptance rejected the result.

## What changes and why

- **Operation selection replaces automatic ceremony.** Merely asking the model to be concise leaves mandatory document/review prerequisites intact. Clear local work can proceed directly; uncertainty and consequential failure modes justify additional investigation, reasoning or review. Explicit project/user requirements remain in force.
- **Original evidence has a delivery boundary.** The user asked for sources and originals, not repeated snapshots in the source PR. Existing Git evidence is retained at a published revision; new results use separate durable storage with immutable links. This preserves inspectability while keeping normal maintenance focused.
- **Existing tests retain their distinct jobs.** Packaging checks cannot measure skill usefulness. Small real LLM tests locate responsibility failures; whole tasks test interactions, correctness and effort. Testing is selected by affected behavior and actual risk, not repeated wholesale after every prompt edit.
- **Acceptance includes aggregate cost and usability.** A reviewer must be able to reject an overcomplicated result despite green tests. A smaller diff alone is not sufficient either: users must still install the skills, understand decisions, finish tasks and retrieve evidence.

## Choices retained

Four independently usable folders keep discovery simple without loading one large manual. Within each skill, shared author/reviewer contracts avoid conflicting format expectations. Templates offer starting points, not mandatory documents. Designs explain decisions, plans explain delivery boundaries, and code/tests retain implementation details.

The Python example adapts Ruff, tests and coverage to the existing project rather than replacing working tools. Coverage is diagnostic, not a proxy for assertion quality. Ordinary commits do not imply PRs, version bumps or release authorization.

## Alternatives and limits

A new workflow orchestrator, custom archival service or rewritten test framework would add maintenance before showing a user benefit. This repair reuses Git for durable historical evidence and the existing execution tools. Full per-phase snapshots remain available in external evaluation storage; shared calibration records no longer need per-run copies. More storage changes need an observed cost, not a speculative architecture.

The retained archive still contributes to Git history. Removing it from the source diff does not erase that fact. Complete behavior evidence must be published separately before a result is called retrievable; an ignored local directory alone is insufficient.

Independent paired tasks provide bounded evidence, not a productivity benchmark. Once a heldout influences a repair, it becomes a regression example. No result is relabeled or criterion weakened to make a candidate pass.

[Requirements](SPEC.md) · [Original user requests](sources/user-workflow.md) · [Research and primary sources](research/workflow/RESEARCH.md) · [Original proposals/reviews](EVIDENCE.md) · [Current decisions](DESIGN.md)
