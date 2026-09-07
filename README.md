# Coding Agent Skills

Four reusable English skills for taking a feature from requirements to reviewed code and delivery. Each skill is independently copyable and includes its own prompts and templates.

Current status: a revised candidate awaiting owner review. [Actual agent-test results](docs/validation/canary/INDEX.md) retain original failures, inconclusive scores and current release acceptance gaps.

## Choose an operation

| Skill | Use it for |
|---|---|
| [feature-design](skills/feature-design/SKILL.md) | Requirements clarification, existing-code intake, design drafting/review |
| [implementation-plan](skills/implementation-plan/SKILL.md) | Stage/commit planning and plan review |
| [stage-development](skills/stage-development/SKILL.md) | Stage implementation, testing, review, fixes and commit readiness |
| [dev-workflow](skills/dev-workflow/SKILL.md) | Environment/hooks, document ownership, PR preparation and authorized releases |

## Use in Codex

Open this repository in Codex. Its `.agents/skills` links expose the four canonical bundles. For another project, copy a desired folder from `skills/` into that project's `.agents/skills/`, preserving its contents; avoid overwriting an existing skill. For personal use across projects, the documented user location is `~/.agents/skills/`.

Use `/skills` or type `$` to select an installed skill. If discovery has not refreshed, restart the session. These locations and symlink discovery are described in [Codex's official skills guide](https://learn.chatgpt.com/docs/build-skills). You can also ask the agent to read a specific SKILL.md by path.

Example requests:

> Use $feature-design to inspect this repository and identify clarification questions for the supplied feature. Preserve the original spec; do not implement yet.

> Use $implementation-plan to turn the reviewed design into stages with observable outcomes and commit gates.

> Use $stage-development to implement stage 1. Use human and independent-agent review before advancing.

> Use $dev-workflow to adapt the existing checks and documentation layout. Keep current tools where they work.

## Choose the amount of process

| Task | Useful default |
|---|---|
| Local, understood and easy to reverse | A short design/implementation note and one combined document review, then implementation, checks and the agreed code review |
| A feature with consequential design choices | Concise design reasoning and outcome-based stages, with the relevant reviews |
| High-consequence change or multiple affected owners/interfaces | Deeper analysis of the actual compatibility, recovery or coordination risks |
| A material unknown | A bounded investigation or experiment, then choose the next step from evidence |

For example: “Use $feature-design and $implementation-plan for this local extension. Choose appropriate depth; a combined note/review is fine. Then use $stage-development to implement with the existing checks and independent code review. Leave human acceptance pending for me.”

Existing repository/user requirements take precedence. Plans own outcomes, dependencies and acceptance; code/tests own implementation detail. Update only affected decisions and pending work. Reviews can accept sufficient work; material findings need a concrete consequence and an affected recheck. Existing gates and real authorization remain in force on the short route.

## Artifact guides

The selected operation loads its relevant guidance; you do not need to paste a large formatting prompt each time. Templates are adaptable examples, not mandatory sections or separate files. After-generation checks are silent unless they uncover a problem.

| Artifact | Starting point | Author/reviewer checks |
|---|---|---|
| Design: choices, reasons and consequences | [Design template](skills/feature-design/assets/design.template.md) | [Design checks](skills/feature-design/references/artifact-checks.md#design) |
| Plan: delivery outcomes, dependencies and acceptance | [Plan template](skills/implementation-plan/assets/implementation-plan.template.md) | [Plan checks](skills/implementation-plan/references/artifact-checks.md#plan) |
| Review: actionable findings and verified dispositions | [Review template](skills/feature-design/assets/review.template.md) | [Review checks](skills/feature-design/references/artifact-checks.md#review) |
| Handoff: current execution state and evidence links | [Stage record](skills/stage-development/assets/stage-record.template.md) | [Execution and resumption](skills/stage-development/prompts/execute-stage.md) |

## Limits and references

Skills guide agent behavior; they are not an automatic approval or release system. Independent review needs a separate context. Installation in your VS Code UI should be checked locally; see [validation](docs/VALIDATION.md) for what was actually tested.

The [goal-based canaries](evals/GOALS.md) check document comprehension, maintainability, useful review, actual implementation and development setup. Normal commits/PRs run fast checks; expensive agent trials run before release or when explicitly requested. See [actual results](docs/validation/canary/INDEX.md) for quality, observed benefit and remaining limits. A passing machine-reader check does not establish human readability.

[Developer notes](DEVNOTES.md) · [Changelog](CHANGELOG.md) · [Design](docs/DESIGN.md) · [Justification](docs/JUSTIFICATION.md)
