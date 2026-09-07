# Changelog

Significant completed changes. The current version is an unreleased baseline; no release has been published.

## [Unreleased]

### Added

- Small real LLM operation tests for clarification, artifact responsibilities, review closure, resumption and delivery evidence, using the existing runner and retained originals.
- Shared author/reviewer artifact contracts, adaptable templates and silent after-generation checks, loaded by the relevant operation.
- Goal-to-case coverage for all four skills, with restricted-reader comprehension checks, neutral task-routing probes and real baseline/candidate execution evidence.
- Retained independent global reviews, original failed attempts and versioned measurement corrections. The result index separates skill quality, observed benefit and unresolved release evidence.
- Versioned workflow canary fixtures, evidence-based grading, isolated runner and a release evidence gate, with fast regression controls separate from expensive agent trials.
- Source-preserving research records and reviewed workflow proposals.

### Changed

- Source delivery separates maintained skills/tests from immutable execution archives; prior originals remain retrievable at a published Git revision.
- PR preparation assesses the complete deliverable against its goal and review cost, alongside actual checks.

- Design and specification decisions link to one live delivery record. Plans track observable outcomes and dependencies; verified findings and applicable check results can be reused without duplicate status or self-referential commits.
- Existing-setup inspection and changed-gate verification have distinct scopes. Observe a gate before changing it, retain known failures, and bind before/after claims to their own results. Missing output cannot establish a verified child result.
- Workflow depth follows uncertainty, consequences and affected boundaries. Understood local work can proceed directly when requirements suffice; design notes and reviews serve actual decisions or explicit policy; material unknowns call for bounded investigation.
- Design openings expose current choices and consequences; plan openings identify the next usable delivery consistently with stage order. Prior decisions and completed work remain available.
- Sufficient work can pass review without cosmetic additions; plans and stage records avoid duplicating code/tests or inventing document prerequisites.
- Local feature extensions amend affected design/pending stages; plans focus on delivery decisions without duplicating the implementation/test inventory.
- Review and handoff records expose current open findings and distinguish author fixes from verified closure, retaining prior rounds.
- Normal commits/PRs use fast checks while release readiness requires current heavy behavior evidence.

### Initial library

- Four portable skills covering feature design, implementation planning, staged development and delivery.
- Focused English operation prompts and document templates with separate user, developer and agent audiences.
- An adaptable Python example for Ruff, full-suite tests and branch coverage at commit time.
- Design and justification documents explaining workflow choices and their consequences.
- Repository checks for portable resources, metadata and document links, with a matching CI workflow.
- Independent review findings, original trial inputs/outputs and retained failure/recovery evidence from self-use.
