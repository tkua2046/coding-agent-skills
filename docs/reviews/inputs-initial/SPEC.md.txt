# Coding workflow skills — requirements

Status: implementation baseline. Source: [user workflow](sources/user-workflow.md).

## At a glance

Deliver four reusable English skills that support the owner's development workflow, plus templates, configuration examples, and a short user entry point. Keep design and justification separate and readable. The repository is the source of truth; it contains no interview question bank.

| ID | Requirement | Observable acceptance |
|---|---|---|
| R1 | Clarify specs before design; support existing code | Intake preserves source text, records assumptions, inspects relevant code and runs a baseline |
| R2 | Design and plan have distinct review steps | Design explains decisions/consequences/examples; plan defines stages, dependencies and acceptance |
| R3 | Every stage has checks, review, fixes and a commit boundary | Review identifies its snapshot; changed code is rechecked; missing human review is not inferred as approval |
| R4 | Separate document audiences and locations | Root README, DEVNOTES, CHANGELOG, AGENTS; specs/design/plans/reviews in docs; logs separate |
| R5 | Reusable development checks | Python sample provides Ruff plus pytest/branch coverage, with a full-suite commit hook and correct failure propagation |
| R6 | Delivery and release are explicit operations | Version/changelog preparation, PR/CI review, merged-version verification, tag and release respect task authorization |
| R7 | Skills remain portable and concise | Each directory works after copying independently; entrypoints route to needed resources; no local absolute paths |
| R8 | Self-use and improvement have evidence | Static checks and behavioral trials are distinguished; discovered defects have changes and follow-up evidence |

## Scope and defaults

Names: feature-design, implementation-plan, stage-development, dev-workflow. Ten internal operation prompts support four user-facing entrypoints. Normal skill discovery remains enabled. Existing repository rules and explicit user instructions override template defaults.

The initial request authorizes implementation, local self-testing and adding this work to the new GitHub repository. It does not request a release or global installation. A real human review is never fabricated; autonomous prototype checks are recorded as such.

Repository documentation is English. Original user requirements retain their original language in the source record. Runtime/software dependencies are used for validation; the skills themselves are Markdown and have no required MCP connection.
