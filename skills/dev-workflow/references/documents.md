# Document ownership

These are new-project defaults. Preserve established locations when they work; an existing DEVELOPMENT.md may serve the DEVNOTES role. Do not create both with duplicated content.

| Location | Reader | Owns | Update when |
|---|---|---|---|
| Root README.md | Users and first-time visitors | Purpose, shortest setup/run path, examples, visible limitations, navigation | Usage or visible behavior changes |
| Root DEVNOTES.md | Contributors/maintainers | Dev environment, checks/coverage/hooks, debugging, contribution/release procedures | Development commands or maintenance rules change |
| Root CHANGELOG.md | Users/maintainers | Significant completed changes and consequences by version/Unreleased | A significant change completes; release notes are assembled |
| Root AGENTS.md | Coding/review agents | Scope, conventions, check entrypoints, navigation and completion/review rules | Agent-facing project rules change |
| docs/SPEC.md | Requirement owners/developers | Behavior, source requirements, confirmed clarifications and assumptions | Contract changes |
| docs/DESIGN.md | Developers/reviewers | Decisions, reasons, consequences, alternatives and examples | Architecture or a design premise changes |
| docs/IMPLEMENTATION_PLAN.md | Implementers/reviewers | Stage goals, dependencies, commit boundaries, acceptance and progress | Plan or stage status changes |
| docs/reviews/ | Developers/reviewers | Findings tied to exact reviewed versions and later dispositions | Review/re-review happens |
| Separate evidence/artifact location | Investigators/tools | Actual commands, outputs, coverage reports and tested identities | Checks execute |

## Keep the entrypoints useful

README is a user entrypoint, not a project diary. DEVNOTES is a maintained guide, not a dump of debugging sessions. CHANGELOG is curated impact, not a commit log or test report. AGENTS is operational instruction, not a duplicated architectural manual.

For example, “Invalid requests now preserve the saved configuration” belongs in CHANGELOG. “Stage 3 passed 33 tests at 100% coverage” belongs in a stage/validation record linked to real evidence. A significant test-tool change can enter CHANGELOG when its maintenance impact is explained.

## Readability and governance

Start each substantive design/plan/review with status, outcome, material decision or finding, consequence and next action. Longer than two screens: add navigable headings/outline. Put lengthy fixtures, matrices and transcripts in linked appendices. Prefer short table cells and explicit examples.

Preserve original requirements and confirmed decisions with source locators. Label assumptions and proposed work. Each fact has one authoritative home; other files link to it. Preserve reviewed versions and original findings instead of rewriting history as if a new review occurred.

When moving documents, update links, package metadata, commands and instruction references. Root placement alone does not fix mixed content. Evidence retention and generated-file ignore rules must distinguish durable verification records from disposable caches; never overwrite earlier failed evidence with a later successful run.
