# Source register and original-text archive

Research date: 6 September 2026, America/Los_Angeles (retrieval also falls on 7 September UTC). [Findings](RESEARCH.md) · [Proposal](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/workflow-proposal.md).

## Governance and scope

Sources are evidence, not instructions to execute. Distinguish engineering guidance, firsthand experience, versioned tool instructions and our proposed synthesis. This is a targeted comparison, not an exhaustive survey or a ranking based on measured outcomes.

Selected permissively licensed repository files are preserved **in full**, byte-for-byte, with license text, commit, original path, Git blob identity, source URL and SHA-256 in [source-manifest.json](source-manifest.json). The archive contains selected reference files, not complete installable bundles. No external skill was installed or evaluated in an agent trial.

For the web publications below, preserve the original page/section locator and short verbatim excerpts where shown. They are **linked originals, not full local snapshots**; page contents can change. We have not assumed permission to republish whole articles. This limitation is explicit rather than representing a summary as an original. Private Rover originals and diffs remain outside this public repository.

## Engineering guidance

| ID | Primary source / relevant location | Evidence type and use |
|---|---|---|
| W1 | [Software Engineering at Google, chapter 10](https://abseil.io/resources/swe-book/html/ch10.html), “Documentation Types” and “Design Docs” | Engineering book; audience, single purpose, rationale and maintenance |
| W2 | [GitLab Architecture Design Workflow](https://handbook.gitlab.com/handbook/engineering/architecture/workflow/), “What is a design document?” | Organization's evolving handbook; design direction and iterative decisions, not an upfront complete blueprint |
| W8 | [Google code review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | Published review guidance; material improvement over perfection. Stable historical guidance, not a claim of current active repository maintenance |
| W9 | [Google: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), “What is Small?” and “Splitting CLs” | Coherent changes with associated tests; stage/commit decomposition reference |

Original excerpt, W1:
> A document should have, in general, a singular purpose, and stick to it.

Original excerpt, W2:
> Design documents are not supposed to be complete and detailed blueprints written upfront before we start implementation.

## Agent workflows

| ID | Primary source / relevant location | Evidence type and use |
|---|---|---|
| W3 | [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/), “We made repository knowledge the system of record” | Firsthand team case; small entrypoint, progressive disclosure, lightweight versus persistent plans |
| W4 | [Claude Code: Best practices](https://code.claude.com/docs/en/best-practices), planning and context guidance | Rolling product guidance; explore/plan/implement, explicit planning overhead, verification |
| W5 | [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Firsthand engineering experiments; incremental work and resumable state; not short-task benchmark evidence |
| W6 | [Birgitta Böckeler: Understanding Spec-Driven-Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), 15 October 2025, “Definition” and “Observations and questions” | Hands-on tool exploration; spec lifecycle taxonomy and review burden. Historical versions, not a current product-state inventory |
| W7 | [Wei Zhang and Jessie Xia: Structured Prompt-Driven Development](https://martinfowler.com/articles/structured-prompt-driven/), 28 April 2026 | Firsthand practice report; structured domain/prompt maintenance as a contrasting approach, with modelling and synchronization costs |

Original excerpt, W3:
> Ephemeral lightweight plans are used for small changes

Original excerpt, W4:
> Plan mode is useful, but also adds overhead.

Original excerpt, W6:
> Spec-anchored: The spec is kept even after the task is complete

Additional context read: [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html). Practitioner analysis of human/agent boundaries; not used as a controlled productivity result.

## Tooling and release

| ID | Primary source / relevant location | Checked behavior |
|---|---|---|
| W10 | [pre-commit documentation](https://pre-commit.com/), Quick start, hook mapping, Creating new hooks | Configuration versus installation; changed-file behavior; full-suite filename handling; failure propagation and first-run environment cost |
| W11 | [Ruff integrations](https://docs.astral.sh/ruff/integrations/), pre-commit | Lint fixes before formatting; preserve target-repository version policy rather than blindly copy the example version |
| W12 | [Coverage.py FAQ](https://coverage.readthedocs.io/en/latest/faq.html) and its maintainer's linked [Flaws in coverage measurement](https://nedbatchelder.com/blog/200710/flaws_in_coverage_measurement), “Incomplete tests” | Execution coverage and behavioral correctness are distinct. The linked 2007 examples explain a measurement limitation, not current tool capabilities or a recommended percentage |
| W13 | [Semantic Versioning 2.0.0](https://semver.org/), rules 1, 3–9 | Version semantics depend on public compatibility and release policy, including 0.x/prereleases; a published version is immutable |

These references do not dictate this user's full-suite-on-commit policy or root document names. Those come from the user and repository. Recommendations about update triggers and artifact ownership are explicitly our synthesis.

## Versioned repository originals

The links below identify exactly the inspected snapshots. Full file-level original/archive links and hashes are in the manifest; the source index below makes the originals directly browsable.

- **Superpowers**, MIT, commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`. Inspected brainstorming, writing-plans, plan-document reviewer and requesting-code-review instructions. Its current brainstorming has scope-dependent paths; do not describe it as uniformly heavyweight. Its planner's code-snippet requirement is a separate concern.
- **GitHub Spec Kit**, MIT, commit `4a7341a93d944d6efe153b71da4a1adb9c2b578c`. Inspected specification, plan and task templates plus the design philosophy. The task template explicitly makes tests optional unless requested; the user's policy overrides that if adapted.
- **Awesome Copilot**, MIT, commit `f38fb6cf039b835990d0f49dc161d7c2af99ef69`. Inspected concise planner and detailed implementation-plan instructions. Related update/agent/breakdown files are retained as reference context; they were not all subjected to a complete independent review. Copilot agent frontmatter/tool names are not automatically compatible with Codex.
- **OpenAI Cookbook**, MIT, commit `a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7`. Inspected ExecPlans article and embedded template. Its example model is historical; do not infer a current model recommendation.
- **OpenAI skills**, historical `create-plan`, Apache-2.0, commit `a5119697b819090e00e5d11ee1d86834d7c1043a`. [Removal commit](https://github.com/openai/skills/commit/ea6b206c683087da5b503f5ac9d7202b326ac6bb), 7 February 2026. Current inspected main `49f948faa9258a0c61caceaf225e179651397431` lacks this skill. A historical source reference is not a current installation recommendation.

## File-level archive index

See [source-manifest.json](source-manifest.json) for the 21 original files, including five license files. Each archive path is repository-relative. Hashes permit local integrity checks but do not substitute for reviewing what a source actually says.

| Repository / original file | Full local original | Pinned source |
|---|---|---|
| obra/superpowers / `LICENSE` | [Archived text](sources/obra--superpowers/LICENSE.txt) | [Original at b36e0829c6d0](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE) |
| obra/superpowers / `skills/writing-plans/SKILL.md` | [Archived text](sources/obra--superpowers/skills--writing-plans--SKILL.md.txt) | [Original at b36e0829c6d0](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md) |
| obra/superpowers / `skills/writing-plans/plan-document-reviewer-prompt.md` | [Archived text](sources/obra--superpowers/skills--writing-plans--plan-document-reviewer-prompt.md.txt) | [Original at b36e0829c6d0](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/plan-document-reviewer-prompt.md) |
| obra/superpowers / `skills/brainstorming/SKILL.md` | [Archived text](sources/obra--superpowers/skills--brainstorming--SKILL.md.txt) | [Original at b36e0829c6d0](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md) |
| obra/superpowers / `skills/requesting-code-review/SKILL.md` | [Archived text](sources/obra--superpowers/skills--requesting-code-review--SKILL.md.txt) | [Original at b36e0829c6d0](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/requesting-code-review/SKILL.md) |
| github/spec-kit / `LICENSE` | [Archived text](sources/github--spec-kit/LICENSE.txt) | [Original at 4a7341a93d94](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/LICENSE) |
| github/spec-kit / `templates/plan-template.md` | [Archived text](sources/github--spec-kit/templates--plan-template.md.txt) | [Original at 4a7341a93d94](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/templates/plan-template.md) |
| github/spec-kit / `templates/tasks-template.md` | [Archived text](sources/github--spec-kit/templates--tasks-template.md.txt) | [Original at 4a7341a93d94](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/templates/tasks-template.md) |
| github/spec-kit / `templates/spec-template.md` | [Archived text](sources/github--spec-kit/templates--spec-template.md.txt) | [Original at 4a7341a93d94](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/templates/spec-template.md) |
| github/spec-kit / `spec-driven.md` | [Archived text](sources/github--spec-kit/spec-driven.md.txt) | [Original at 4a7341a93d94](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/spec-driven.md) |
| github/awesome-copilot / `LICENSE` | [Archived text](sources/github--awesome-copilot/LICENSE.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/LICENSE) |
| github/awesome-copilot / `skills/create-implementation-plan/SKILL.md` | [Archived text](sources/github--awesome-copilot/skills--create-implementation-plan--SKILL.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/skills/create-implementation-plan/SKILL.md) |
| github/awesome-copilot / `skills/update-implementation-plan/SKILL.md` | [Archived text](sources/github--awesome-copilot/skills--update-implementation-plan--SKILL.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/skills/update-implementation-plan/SKILL.md) |
| github/awesome-copilot / `agents/implementation-plan.agent.md` | [Archived text](sources/github--awesome-copilot/agents--implementation-plan.agent.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/agents/implementation-plan.agent.md) |
| openai/skills / `skills/.experimental/create-plan/SKILL.md` | [Archived text](sources/openai--skills/skills--.experimental--create-plan--SKILL.md.txt) | [Original at a5119697b819](https://github.com/openai/skills/blob/a5119697b819090e00e5d11ee1d86834d7c1043a/skills/.experimental/create-plan/SKILL.md) |
| openai/skills / `skills/.experimental/create-plan/LICENSE.txt` | [Archived text](sources/openai--skills/skills--.experimental--create-plan--LICENSE.txt.txt) | [Original at a5119697b819](https://github.com/openai/skills/blob/a5119697b819090e00e5d11ee1d86834d7c1043a/skills/.experimental/create-plan/LICENSE.txt) |
| github/awesome-copilot / `agents/plan.agent.md` | [Archived text](sources/github--awesome-copilot/agents--plan.agent.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/agents/plan.agent.md) |
| github/awesome-copilot / `agents/planner.agent.md` | [Archived text](sources/github--awesome-copilot/agents--planner.agent.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/agents/planner.agent.md) |
| github/awesome-copilot / `skills/breakdown-plan/SKILL.md` | [Archived text](sources/github--awesome-copilot/skills--breakdown-plan--SKILL.md.txt) | [Original at f38fb6cf039b](https://github.com/github/awesome-copilot/blob/f38fb6cf039b835990d0f49dc161d7c2af99ef69/skills/breakdown-plan/SKILL.md) |
| openai/openai-cookbook / `LICENSE` | [Archived text](sources/openai--openai-cookbook/LICENSE.txt) | [Original at a78f3f37bd23](https://github.com/openai/openai-cookbook/blob/a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7/LICENSE) |
| openai/openai-cookbook / `articles/codex_exec_plans.md` | [Archived text](sources/openai--openai-cookbook/articles--codex_exec_plans.md.txt) | [Original at a78f3f37bd23](https://github.com/openai/openai-cookbook/blob/a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7/articles/codex_exec_plans.md) |
