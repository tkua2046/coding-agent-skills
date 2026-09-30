# Document ownership

These are ownership defaults for documents that are useful or required, not a list of files to create. Preserve established locations that work. DEVELOPMENT.md may already serve the DEVNOTES role. A direct local change can be delivered with a response and existing checks when no durable document is needed.

| Location | Reader | Owns / update trigger |
|---|---|---|
| Root README.md | Users | Purpose, setup/run, examples, visible limits and navigation; update when usage changes |
| Root DEVNOTES.md | Contributors | Environment, checks/hooks/coverage, troubleshooting and contribution/release procedures; update when operations change |
| Root CHANGELOG.md | Users/maintainers | Significant completed impact under Unreleased/version; not a commit or test log |
| Root AGENTS.md | Agents | Scope, conventions, check entrypoints and actual review/acceptance policy; not an architectural manual |
| docs/SPEC.md | Requirement owners | Behavior, original sources, confirmed clarifications and assumptions; update when contract changes |
| docs/DESIGN.md | Developers/reviewers | Choices, reasons, consequences, relevant behavior/examples and decision status |
| docs/IMPLEMENTATION_PLAN.md | Implementers/reviewers | Outcomes, dependencies, boundary reasons and acceptance; not a function/test inventory |
| docs/reviews/ | Authors/reviewers | Findings, reviewed revisions and later verified dispositions |
| Existing plan/handoff status block | Implementer/owner | One live delivery state: completed outcome, next action, open findings, applicable check/review/acceptance links |
| Evidence/artifact location | Investigators/tools | Actual commands, outputs and tested identities; separate retained evidence from disposable caches |

## Useful entrypoints

Make the current choice and consequences easy to find in a design, the next outcome and acceptance in a plan, and the verdict, open findings and next action in a review. Organize supporting sources and detail where useful; no exact opening fields or headings are required. Add navigation when detail grows; link lengthy matrices and transcripts.

Design/spec own decision/contract status and link to delivery state when maintained. A PR can summarize validation/limits for its identified revision without becoming another continuously synchronized record. “Invalid requests preserve saved preferences” belongs in CHANGELOG; test counts/raw logs belong in evidence.

A local extension amends affected decisions, examples and pending outcomes. Private renames or extra tests ordinarily leave design/plan unchanged. Retain completed outcomes; create a separate design for distinct ownership/lifecycle or substantial independent risk.

## Preserve once, then link

When updating owned documents, link the relevant originals retained under the skill’s preservation rule; label proposals and assumptions. Scope evidence to the work being assessed and the repository’s retention policy, without creating a new archive by default.

Review history distinguishes original concern, author fix claim and reviewer verification on the relevant revision. Handoffs link applicable evidence. A resulting commit hash belongs in a delivery response or established record. Explicit repository retention requirements still apply; expected generated artifacts may belong in delivery when they serve its purpose. Keep disposable caches separate.

When moving documents, update links, metadata and operational references. Root placement alone does not fix mixed responsibilities. Never overwrite failed evidence with later success.
