# Outcome-driven workflow revision

Current delivery: the authorized baseline comparison, one skill-repair wave and affected retests have finished within the reviewed 220-call ceiling. The planned identical-candidate timing repeat is deferred; [actual results](../validation/canary/INDEX.md) retain failures and inconclusive scores. Owner review remains pending; no merge, release or global installation is authorized. Baseline: `b9087c56f2b136aff7c4b3495fffeccdfe760a28`. The original proposal and later scope decisions are preserved below.

**Outcome:** a developer can understand the decision and next action quickly, and a coding agent can deliver correct work at a cost proportionate to its uncertainty and consequences. Keep the four skills; change workflow selection before adding more instructions.

## Decisions and consequences

- Select depth from uncertainty, failure consequences/reversibility and affected interfaces/owners. A local understood change can combine design and plan in one short note and one review; an ordinary feature keeps distinct decisions and stages; consequential work expands the relevant risk analysis. One sentence explains the selection. No classification report or scorecard.
- Investigate a consequential unknown with a bounded question/experiment, then reconsider depth. Do not make uncertainty a reason to elaborate an unsupported design.
- Each operation has an observable exit: design decisions sufficient to implement, a usable next stage, material findings resolved, or a specific pending decision. Review suggestions need a concrete consequence to block progress. Rechecks cover the affected invariant; cosmetic polishing does not restart the lifecycle.
- Preserve current user authorization and project gates. Small-task simplification does not waive meaningful tests, hooks, existing code conventions or required human acceptance. Stable setup and release policy are reused rather than recreated for each feature.
- Keep authoritative facts in their owner document; original requests and past results remain available. Templates show a short entrypoint and optional detail, not mandatory paperwork.

Example: an occupied-cell extension needs its blocked-move behavior, lookup decision, a decisive example and an implementation outcome. It can use one local amendment and combined review. A settings migration must additionally explain preservation, validation-before-activation and interrupted retry.

## Goal-to-test contract

| Skill goal | Existing evidence to extend | Missing behavior to add |
|---|---|---|
| Feature design: faithful scope, useful clarification, consequential choices, readable design | Existing intake, small feature, scope extension, migration | Bounded investigation; independent first-screen comprehension; realistic local delivery with chosen depth |
| Implementation plan: actionable stages/dependencies, glanceable next action, low maintenance burden | Small feature, migration, maintenance perturbation | First-screen comprehension; good and defective document review; local delivery without a function/test inventory |
| Stage development: correct tested behavior, useful review that terminates, resumable progress | Counter, incomplete-fix recheck, execution/handoff | Local delivery; review ready work without manufacturing blockers; cost tied to new findings and actual progress |
| Dev workflow: adapt working setup, effective checks, audience-specific docs, truthful delivery | Stale/current release assessment | Adapt an existing small application and prove its local checks catch a real failure; preserve existing tools and useful user documentation |

The five added cases are `bounded-delivery`, `review-ready`, `review-defective`, `workflow-setup`, and `bounded-investigation`. Existing cases retain their history; affected case/rubric revisions advance. This count follows the missing operations, not a target suite size.

## Evaluation and iteration

Freeze task contracts, grading and baseline before candidate edits. Use the existing disposable-workspace runner; add only bounded conditional review phases and a restricted first-screen reader if necessary. The reader sees the actual beginning of generated documents and task questions, not full documents, desired answers or the author's summary. Its answers are a machine comprehension proxy; human glanceability remains for owner review.

Use identical model/effort and runtime settings for baseline/candidate. Run each required case once per frozen candidate; a demonstrated failure permits a documented fix and affected rerun. Repeat the local-delivery comparison to inspect variability. Preserve every attempt, selected bundles, task text, transcripts, outputs, checks, judgments and time. A timeout is incomplete, never approval. Report elapsed time and document/review churn as observations; no universal latency or productivity claim.

Calibrate the scoring prompt on predeclared acceptable/defective/incomplete outputs, including readability and review restraint. Programmatic contract checks establish runtime behavior; semantic grading checks decision/usefulness criteria. Required correctness and evidence failures cannot be averaged away by speed. First-screen questions must be answered from the exposed text; merely having headings does not pass.

At three checkpoints (test contract, first paired results, final candidate), independently examine the whole workflow: does it reduce developer effort, are tests representative, and did any fix add disproportionate machinery? Retain dissent and dispositions. Do not add a general rule for one example unless the failure mechanism generalizes.

**Separate benefit decision:** passing correctness/semantic criteria establishes candidate acceptability, not improvement. For each goal compare baseline/candidate reader answers, material versus unnecessary review findings, unnecessary document rewrites, and observed elapsed time. Classify benefit as improved, unchanged, tradeoff, or unresolved with concrete evidence. No claim of overall improvement from a passing suite or raw word-count reduction. Owner reading experience remains pending; slower runs and lost capabilities remain visible. Small-task gains cannot excuse a regression in the risk control.

**Iteration bound:** start with one baseline and one candidate wave. Permit at most two targeted skill-repair waves for demonstrated failures before a fresh global review must reconsider the task, measurement and workflow. Do not keep adding prompt rules when the same mechanism persists. Infrastructure corrections are recorded separately and do not count as skill improvement. The initial experiment budget is 150 model invocations; reaching it requires an explicit incomplete-results report and a revised scope decision, never a fabricated pass. An identical-input repeat is predeclared only for the bounded-delivery variability comparison; other reruns need a recorded cause and change.

## Delivery boundaries

1. Review this contract and the concrete cases; fix material evaluation defects.
2. Run the frozen baseline, revise the four skills, run the candidate and iterate from failures.
3. Independently review final changes, run the agreed fast gate and publish a short goal-by-goal result index with raw links. Leave all changes on the feature branch for human review.

Research provenance: [existing source register and licensed originals](../research/workflow/SOURCES.md). Current guidance checked in this conversation: [OpenAI](https://learn.chatgpt.com/guides/best-practices), [Claude Code](https://code.claude.com/docs/en/best-practices), [Google review standard](https://google.github.io/eng-practices/review/reviewer/standard.html). These support proportionate planning and material review; this routing/evaluation design is our proposed synthesis, not a validated vendor workflow.

## Reviewed experiment adjustment

The [global scope checkpoint](../reviews/outcome-scope-checkpoint.md) reviewed incomplete results before the initial 150-call boundary. The primary task adopts its **220 fresh-call hard ceiling**, including prior/aborted calls, for the existing overnight authorization. This is an internal experiment limit, not user approval of a token budget or of the skills. The current scope is the existing 17 cases, identified measurement corrections, **one** minimal current-summary skill repair and affected validation. No new cases, model matrix or general evaluation framework are added. The earlier two-repair-wave allowance is narrowed to one.

Run the demonstrated scope-extension defect first after freezing the repair. If it persists, stop prompt editing and report the limitation. Complete affected validation when the remaining allowance covers it; reserve a whole comparison before the predeclared final delivery repeat. Unsupported scoring recoveries or comparisons that cannot fit are deferred with their original evidence and release limitation stated. The morning deliverable is a reviewed candidate with truthful results, not an inferred release authorization or a promised all-green gate.

Before the final repair wave's development-workflow run, [independent TRU01 review](../reviews/outcome-setup-truthfulness-review.md) confirmed another concrete failure: the setup report called an unexecuted baseline check successful. The same repair candidate therefore includes one clarification in setup's existing completion paragraph, tying claims to actual command output/state. The two design/planning replacements remain unchanged; their already-running targeted case does not select dev-workflow. This is one frozen repair wave covering two evidenced goals, not another cycle or a new review process. Keep the 220-call ceiling. The [V6 commit-count measurement concern](../reviews/outcome-commit-count-review.md) and unsupported scorer recoveries may remain deferred; do not spend the remaining allowance just to relabel them green.
