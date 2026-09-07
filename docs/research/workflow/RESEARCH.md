# Research: sustainable development with coding agents

Status: research for a proposal, not an implemented workflow. Checked 6 September 2026 (Los Angeles). Audience: the owner and reviewers of these four skills.

**Finding:** the user's clarify → design/review → staged implementation/review → PR → release workflow is a sound starting point. The missing design work is deciding what each step must establish, when it pays for itself, what persists, and how evidence permits progress. Plan verbosity is one important failure mode within that larger system.

Read next: [proposed changes](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/workflow-proposal.md). Reference: [sources and original texts](SOURCES.md) · [validation proposal](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/workflow-validation.md).

Outline: [Evidence](#what-the-evidence-supports) · [Document roles](#responsibilities-and-maintenance) · [Existing skills](#existing-material-reuse-adapt-or-avoid) · [Pain points](#pain-points-to-design-and-test-against) · [Local findings](#local-evidence-and-open-uncertainty).

## What the evidence supports

This is a targeted comparison of engineering handbooks, firsthand agent workflows, and actual versioned skills/templates. It is not a survey establishing a single industry-standard AI workflow or a productivity benchmark.

| Practice | Evidence and implication | Limit |
|---|---|---|
| Separate document purposes | Google's documentation chapter distinguishes audiences and document types; GitLab describes design as technical direction and decisions that evolve through implementation. This supports readable, maintained contracts and rationale. [W1–W2](SOURCES.md#engineering-guidance) | Neither mandates a separate document for every local feature |
| Scale planning to uncertainty and handoff | OpenAI describes lightweight plans for small changes and persistent execution plans for complex work. Claude Code guidance explicitly acknowledges planning overhead. [W3–W4](SOURCES.md#agent-workflows) | Vendor experience and product guidance, not comparative proof |
| Keep agents grounded in observable progress | Anthropic's long-running-agent experiments use incremental features, tests, Git history and handoff state. [W5](SOURCES.md#agent-workflows) | Multi-session application work; copying its entire harness into a short interview would be an extrapolation |
| Decide whether a spec persists | Böckeler distinguishes spec-first, spec-anchored and spec-as-source, and reports review overload in hands-on tool trials. [W6](SOURCES.md#agent-workflows) | October 2025 observations are historical; our tool comparison uses separately pinned, newer source |
| Detailed maintained specifications are a real alternative | Thoughtworks' SPDD case maintains structured prompts/domain intent with stronger modelling and review discipline. [W7](SOURCES.md#agent-workflows) | Its modelling and synchronization costs need a business reason; it is not evidence for making every implementation plan a second source code tree |
| Review coherent changes and material risks | Google's review guidance favors self-contained changes with related tests and rejects perfection as the approval standard. [W8–W9](SOURCES.md#engineering-guidance) | Local human approval policy still governs advancement |

## Responsibilities and maintenance

The following is our proposed synthesis, not a filename standard claimed by the sources. Reuse established repository names. A small task can have short sections rather than a new file for every concern.

| Artifact | Question it answers | Update trigger / end of life |
|---|---|---|
| Original request + clarification record | What was actually requested and confirmed? | Preserve supplied text; append decisions, assumptions and source locations |
| Current feature specification | What externally observable behavior and constraints must hold? | Contract changes; link original evidence rather than replacing it |
| Design | Why this approach; which boundaries, invariants, alternatives and consequences matter? | A relevant decision/premise changes; locally amend a living design. Supersede a historical decision record explicitly if the repo uses that form |
| Implementation plan | Which coherent outcomes, dependencies and risks determine execution order and readiness? | Pending work or dependencies change; completed work becomes history. Implementation/test details live with code and tests |
| Review record | What is still wrong or undecided, against which content, and how was it checked? | Append each finding's disposition and recheck evidence; keep current verdict and open IDs at the top |
| Code and executable tests | How does it work, and which concrete behaviors were checked? | Implementation evolves; do not replicate every function, assertion or test count in the plan |
| README | What does this project do, and how do I use it? | User-facing setup, examples or limitations change |
| DEVNOTES / existing developer guide | How do contributors develop, check, debug and release it? | Development operations change |
| CHANGELOG | What significant delivered change affects users or maintainers? | A meaningful change completes / a release is prepared; not every commit or test run |
| AGENTS | What project-specific instructions and navigation do agents need? | Stable operating rules change; link detailed references on demand |
| Validation evidence | What ran against what content, with what result? | New checks append evidence; raw logs are not front-page documentation |

**Example:** adding an obstacle changes a movement invariant and an acceptance example. That warrants a local design amendment and an executable regression case. Adding another test of the same invariant does not change the design or pending-stage decomposition. A configuration-file extension introduces a real new input contract and may justify further design; a custom parser policy still needs a reason. An independently evolving subsystem can justify a separate linked design.

## Existing material: reuse, adapt, or avoid

The selected original files and licenses are archived, with immutable URLs and hashes in [the manifest](source-manifest.json). These are source inspections, not executed skill benchmarks. No external bundle was installed.

| Candidate | Useful material | Decision for this repository |
|---|---|---|
| OpenAI historical `create-plan` | Concise scope and ordered checklist; avoid code snippets and excessive micro-steps | Closest lightweight planning reference. It was removed from current `openai/skills`; adapt attributed ideas from the pinned historical version, do not advertise a current install |
| Superpowers `writing-plans` | Split work where review can independently accept/reject outcomes; its reviewer focuses on material implementation problems | Adapt those principles. The inspected planner requires actual code/test snippets in plan steps, conflicting with the user's maintenance goal |
| Superpowers `brainstorming` | Distinguishes spike, bounded and architectural work; bounded designs can be short | Reference its proportionality. Do not import its universal approval gate or its whole skill chain; the user's existing authorization and review policy govern |
| GitHub Spec Kit | Distinct specification, technical plan and story-oriented tasks; explicit independently testable outcomes | Reference the separation and dependency reasoning. Its full artifact set is unnecessary for every follow-up; its task template makes tests optional unless requested, whereas this user's development workflow requires meaningful tests |
| Awesome Copilot `planner.agent.md` | A small planning-only prompt covering goal, requirements, steps and validation | Possible starting prompt; Copilot tool names/frontmatter need adaptation. It is not a Codex skill drop-in |
| Awesome Copilot `create-implementation-plan` | Deterministic machine-facing task structure | Avoid as the default here: its exact implementation detail and mandatory sections recreate the reported burden |
| OpenAI Cookbook ExecPlans | Observable milestones, durable progress/decision state, explicit recovery for complex tasks | Offer selected guidance for long handoffs or substantial risk. Do not make its full self-contained execution-document format mandatory for small changes |

No inspected off-the-shelf item covers the user's complete policy without adaptation. Keeping four small operation-oriented skills is a provisional reuse decision, not a claim that a new framework is needed. Preserve third-party attribution if text is actually incorporated later.

## Pain points to design and test against

| Failure | Likely mechanism / practical control |
|---|---|
| Invented scope or rebuilding existing code | Separate user requirements, confirmed decisions and reversible defaults; inspect the relevant implementation before design; research a material unknown rather than every task |
| Planning never reaches implementation | Optional depth; stages justified by outcomes/dependencies/risk. Resolve material uncertainty with a bounded experiment when authorized; stop cosmetic rewrites |
| A growing second codebase in Markdown | Maintain contracts and decisions; retire completed execution plans. Update documents because their owned fact changed, not because a test name changed |
| Endless review/fix loops | Require a concrete consequence for blockers; distinguish suggestions and unresolved decisions. Recheck the affected contract and expand only when the fix creates new risk |
| Passing tests and review that merely repeat the author's assumptions | Derive expected results from requirements; have an authorized independent reviewer challenge counterexamples. Separate runtime evidence, reviewer judgment and human acceptance |
| Compaction loses progress or resurrects closed work | Small stable entrypoint plus current stage, reviewed content, open findings and next action. Preserve original logs separately; do not replay all history into every role |
| Hooks/coverage provide false confidence | Check actual installation, interpreter, source coverage and failure propagation. Local feedback, CI, branch coverage and behavioral correctness are distinct [W10–W12](SOURCES.md#tooling-and-release) |
| Every commit becomes ceremony | A coherent commit is a checkpoint; a PR is a review unit; release/version/tag is a delivery event. Keep the user's full commit gate, and batch release preparation according to repository policy [W13](SOURCES.md#tooling-and-release) |

For Python, the researched setup supports Ruff fixes before formatting and meaningful tests with a coverage report. A percentage threshold does not replace assertions. Preserve the project's existing gate; a slow suite is a reason to propose an explicit fast-local/full-CI split, not silently weaken the user's policy. Tool versions and installation should be verified in the target repo, not copied from an article's example.

## Local evidence and open uncertainty

The private Rover observation is documented in the [earlier proposal](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/small-change-workflow.md). Its accepted documents were broadly rewritten, and the planning turn included compaction. Later YAML requirements were real user scope. Review issues were eventually closed at document level, with closure buried under historical findings; obstacle implementation had not started. The four skills were not installed there, so this is a motivating failure case, not a test failure attributable to them.

The current skills already contain many sound rules. Inspection found an actual conflict: the implementation planner mandates both a stage table and detailed cards while discouraging duplication. Stage records and review guidance also need clearer lifecycle and current-state behavior. Packaging checks cannot determine whether these instructions produce maintainable work. The next evidence must come from bounded behavioral trials, including existing-repo work, an incomplete review fix, a high-risk control, and maintenance after a minor code/test edit.
