# Proposal: maintainable development with coding agents

Status: owner authorized execution with “执行”. The [independent delta review](workflow-regression-review.md) covers archived v3; the [earlier review](workflow-proposal-review.md) covers v2. Implementation and evidence status are tracked in the [current increment](../IMPLEMENTATION_PLAN.md#current-increment) and [canary index](../validation/canary/INDEX.md). Heavy tests remain deferred until release.

**Approved direction:** retain the four existing skills and revise their conflicting defaults so the user's full workflow is useful at different task sizes. Deliver small skill changes, concrete examples and behavioral evidence; do not add a workflow framework. Implementation-plan maintenance is one important part of this proposal, alongside scope control, design quality, review convergence, verification, context and delivery.

Read this page for scope. [Research](../research/workflow/RESEARCH.md) explains the rationale; [sources](../research/workflow/SOURCES.md) retain provenance and original texts; [validation](workflow-validation.md) defines the proposed trials.

Outline: [Workflow](#what-changes-in-the-workflow) · [Documents](#document-contract) · [Deliverables](#concrete-deliverables-after-approval) · [Implementation and evidence](#implementation-boundaries-and-evidence).

## What changes in the workflow

| Step | Proposed behavior | Consequence / example |
|---|---|---|
| Feature intake | Preserve original specs; inspect relevant existing code and baseline checks; separate consequential questions from reversible defaults | Clarify whether blocked movement stops a session; do not ask about routine naming. Research only uncertainties that could change the approach |
| Design and its review | Describe behavior change, key decisions, alternatives, invariants and consequences with decisive examples. Amend affected parts of an accepted design | A local obstacle feature adds a movement rule. A new persistence boundary may justify a separate design. A small design can be a short reviewed note |
| Implementation plan and review | Plan coherent outcomes, dependencies, important risks, acceptance and commit boundaries. Use one compact representation, adding detail only where needed | A stage can say “blocked moves report failure and preserve state; existing commands still work,” without prescribing every function and test |
| Implement and validate | Bring meaningful tests with the code; run focused checks during work and the agreed full hook/commit gate before advancement | A new regression case is maintained in the test suite; it does not require rewriting the plan |
| Human and agent review | Review identifiable content in parallel when authorized. Keep verdict/open IDs first; preserve findings and distinguish author-fixed from reviewer-verified | An incomplete fix remains open. A material fix receives targeted recheck; a cosmetic suggestion cannot create an endless approval loop |
| Resume and maintain | Retain a compact current-stage record with evidence pointers and pending decisions. Update only documents whose owned facts changed | A resumed agent can find the next action without replaying the transcript or reopening completed stages |
| PR and release | Keep coherent commits within the agreed PR scope. Maintain Unreleased notes; prepare a version when release policy requires it; tag the verified release commit | No PR or version bump per implementation commit. A passing hook or agent review does not imply human approval, merge or publication |

Keep the user's requested design, plan and stage reviews. Scale their depth, rather than silently removing them. Existing authorization persists. If a required human decision is pending, preserve it and continue only independent work; do not treat silence as acceptance.

## Document contract

Original requirements remain preserved. Current specs own behavior; design owns rationale and consequential decisions; the implementation plan owns pending execution boundaries and progress. Code/tests own implementation details. Completed plan entries remain historical and are not continually synchronized with later refactors.

README stays the human entrypoint; DEVNOTES (or the established developer guide) owns contributor operations; CHANGELOG owns significant delivered impact; AGENTS owns concise project instructions and navigation. These are already repository policies: improve their application, not add duplicate manuals. [Responsibility and update table](../research/workflow/RESEARCH.md#responsibilities-and-maintenance).

Each substantive artifact starts with its outcome/status, material decision or finding, consequence and next action. Add an outline when needed. Put original sources and long evidence behind links. Do not enforce page, stage or test-count quotas as a substitute for judgment.

## Concrete deliverables after approval

| Deliverable | Existing location and bounded changes |
|---|---|
| Repeatable canary and release regression gate, first | Proposed `evals/` holds versioned cases, isolated-fixture runner and graders; durable results remain under `docs/validation/`. Port the existing trials, preserve the unchanged-skill snapshot, and verify the runner/gate with fast controls. Run expensive baseline/candidate comparisons before release |
| Intake/design skill revision | `skills/feature-design/`: refine intake research triggers, local amendments, decision-focused depth and review closure; adjust affected prompts/assets consistently |
| Planning skill revision | `skills/implementation-plan/`: remove mandatory table-plus-card duplication and repeated workflow narration; establish outcome/dependency planning and completed-plan lifecycle |
| Execution/review revision | `skills/stage-development/`: clarify current-state handoff and finding dispositions in affected prompts/stage record; preserve checks, exact reviewed content and human policy |
| Workflow integration | `skills/dev-workflow/references/documents.md` and setup guidance only where inconsistent with the agreed lifecycle; retain working hook, coverage, PR and release behavior |
| Usable examples and evidence | Small-change and substantial-change examples; isolated trial inputs/results and readable verdicts. Keep evaluation expectations out of worker inputs |
| Navigation and justification | Short usage update in README, affected rationale in JUSTIFICATION, significant change in CHANGELOG; link research rather than copying it into skills |

No new skill, MCP, runtime framework, global installation, Rover edit or model configuration change is proposed. Do not rewrite all four bundles merely for consistency of wording. Existing behavior with no demonstrated conflict remains a regression requirement.

## Why adapt these skills

The [source comparison](../research/workflow/RESEARCH.md#existing-material-reuse-adapt-or-avoid) found useful components, not a verified drop-in replacement for the whole policy. Borrow attributed guidance on concise planning, material review findings, coherent changes and durable handoffs. Do not import templates that require a natural-language mirror of code/tests or an entire mandatory approval chain. OpenAI's historical `create-plan` is no longer in the current repository; do not recommend installing it as a current supported skill.

## Implementation boundaries and evidence

First deliver the reusable canary: fixed raw tasks/fixtures, predeclared grading, the preserved unchanged-skill snapshot, durable run records and a gate exercised by fast controls. Expensive baseline/candidate comparisons may run together before release; completing all heavy trials is not a prerequisite for each small prompt edit. Existing records remain historical; do not relabel them as runs of the new grader. Keep evaluation assets here and create disposable isolated repos per run. This increment has independent value and must be reviewable before changing the behavior it will evaluate.

Then align the affected entrypoints, prompts and templates, include the two examples, and follow the [tiered validation policy](workflow-validation.md#regression-policy-for-future-prompt-changes). Keep a narrow implementation boundary; no mandatory commit per skill. Small changes run fast checks and relevant lightweight regressions. Full heavy behavioral validation gates release, not every commit or PR.

Before delivery, run the existing packaging/skill/checker tests and repository gate. Test the new runner/grader/gate's failure paths and add behavioral regression cases for demonstrated prompt defects. Evaluate outputs against requirement-derived criteria: preserving intent, handling risk, maintainability after small edits, review closure, handoff and honest delivery state. Retain failures and explain remaining limitations.

Freeze baseline inputs and grading before prompt edits. Before release, evaluate the declared baseline and release candidate with matching tasks, grader, model/effort and environment. These bounded comparisons are behavioral checks, not statistical speed claims. Record time, review rounds and document churn as observations. Do not optimize word counts at the expense of a necessary contract or recovery case.

After implementation, obtain an authorized independent review of the changed behavior and evidence. The present proposal review cannot approve future code. Commit/push and CI verification follow the existing delivery scope only when implementation is authorized; installation and release remain separately scoped operations.

## Review history and current boundary

This replaces the narrower [v1 proposal](small-change-workflow.md); its original [review](small-change-workflow-review.md) and immutable input remain preserved. SC01 required a concrete migration hazard; SC02 required a failed recheck before a successful one. The independent v2 review verified both remedies at proposal level; the behavioral trials remain unexecuted.

Current work stops at research, this proposal and its review. Candidate skill edits and behavioral trials have not been executed.

The reviewed v2 is preserved in the [snapshot](evidence/workflow-v2/docs--proposals--workflow-proposal.md.txt). V3 adds standardized regression safeguards with heavy tests deferred to release; its [reviewed inputs](evidence/workflow-v3/manifest.json) and [delta review](workflow-regression-review.md) are retained. Only these status references were updated after review. Evaluation assets, gates and new skill behavior are still unimplemented.
