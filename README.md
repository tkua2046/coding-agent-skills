# Coding Agent Skills

Four reusable English skills for taking a feature from requirements to reviewed code and delivery. Each skill is independently copyable and includes its own prompts and templates.

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

## Limits and references

Skills guide agent behavior; they are not an automatic approval or release system. Independent review needs a separate context. Installation in your VS Code UI should be checked locally; see [validation](docs/VALIDATION.md) for what was actually tested.

[Developer notes](DEVNOTES.md) · [Changelog](CHANGELOG.md) · [Design](docs/DESIGN.md) · [Justification](docs/JUSTIFICATION.md)
