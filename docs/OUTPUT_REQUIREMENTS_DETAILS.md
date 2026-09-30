# Prior specification draft and audit — retained history

**Superseded as an active specification.** The [four current skill specifications](OUTPUT_REQUIREMENTS_PROPOSAL.md) and their evaluation rules now own the proposal. This file preserves the earlier audit, findings and draft wording; its unresolved statuses and next-step suggestions describe that earlier revision. Do not use them as current instructions.

[Feature design](#a-feature-design) · [Implementation plan](#b-implementation-plan) · [Stage development](#c-stage-development) · [Development workflow](#d-dev-workflow)

For each card: functionality → expected output → goals → non-goals → failure modes → tests and rubrics. Goal IDs connect each test to the result it is meant to establish. Check each applicable goal separately; a combined score must not hide a failure. Examples illustrate behavior, not mandatory wording or technology.

## Audit against all owner feedback

**Verdict: needs changes.** The existing skills contain useful concrete rules; the feedback-to-specification-to-rubric mapping is incomplete. Do not rewrite already adequate rules or treat existing test results as acceptance of the new draft. Scope: tracked skills/evaluation definitions at `e5e7242f4f2c6ec3d219c20e2eb58a6c6ba85902`, plus the current uncommitted proposal. This is a source/evidence audit by the author, not an independent behavioral evaluation.

**Read first:** retain the plan-maintenance, local-amendment, review-closure, setup and delivery contracts. Resolve the four findings below before selecting further experiments. The owner's rejection of earlier document entrypoints remains a usability failure for those drafts; a machine-reader pass elsewhere does not override it.

### Open findings

- **Q1 — Incomplete requirement mapping (F1/F9).** The draft defines A1–D5, but existing case rubrics do not reference them or map all applicable owner requirements to separately assessable criteria. The [scorer](../evals/graders/review.md) reads the supplied case rubric and request; it does not automatically add obligations from this document. Connect the applicable operation, goal, concrete criterion and evidence, reusing existing cases. Do not solve this by multiplying headings or tests.
- **Q2 — Efficiency specification remains incomplete (F6).** Route choice, stopping guidance and some time checks exist. Acceptance of the reported small-change time/context cost is still undefined. Specify what useful completion and unnecessary repeat work mean for each operation, how time/context cost is observed, and justified case-specific acceptance. Inspect the reported run before attributing its cause. No new numeric target is justified by this audit.
- **Q3 — Usability coverage is partial (F2/F5/F12).** Templates define openings, examples and navigation, and some rubrics assess them. Existing combined design/plan and restricted-reader cases do not establish every operation's output usability, or the human usability of the delivered skill package. Identify which concrete reader questions/failure examples remain uncovered; retain author/reviewer agreement and avoid universal word/line quotas.
- **Q4 — The documented next evaluation has an unsupported priority (F9/F11).** The [research follow-up](research/workflow/RESEARCH.md#7-september-2026-skill-evaluation-follow-up) still says the next evaluation should assess natural-language selection, without stating the unresolved acceptance prerequisite. That is an acknowledged coverage gap, not a demonstrated priority. It can steer subsequent work into another premature test wave. Reconcile the maintained next-action guidance with the complete specification audit.

### Item-by-item coverage

“Present” means an explicit rule or a directly relevant declared criterion exists. “Partial” identifies a missing part or mapping. Neither means all required behaviors passed. Run evidence keeps its original case, skill version and limits in [VALIDATION](VALIDATION.md) and [EVIDENCE](EVIDENCE.md).

| Feedback | Existing specification | Existing rubric / evidence | Audit disposition |
|---|---|---|---|
| F1 — Per-skill function/output/goals/non-goals | **Partial:** entrypoints, operation prompts, templates and this draft supply the pieces. | **Partial:** [GOALS](../evals/GOALS.md) maps broad goals to cases; case grading does not consume A1–D5 automatically. | Q1: finish the concrete mapping, including all ten operations. |
| F2 — Glance, outline, consequences/examples | **Present:** [design contract](../skills/feature-design/assets/design.template.md), [plan contract](../skills/implementation-plan/assets/implementation-plan.template.md), [document entrypoints](../skills/dev-workflow/references/documents.md). | **Partial:** `v1-small-feature / first-screen-comprehension`; [review-defective](../evals/cases/review-defective/rubric.json) explicitly checks buried decisions/navigation. The investigation reader passed after a real failure. | Q3: retain these criteria; establish uncovered output/reader responsibilities and human usability. Do not claim this requirement was absent. |
| F3 — Plan is not prose implementation | **Present:** [plan checks](../skills/implementation-plan/references/artifact-checks.md) explicitly reject helper/test synchronization and duplicate policy. | **Present:** [stable-plan](../evals/cases/smoke-plan-maintenance/rubric.json), plus public-change maintenance criteria. The retained repair pair passed the private-edit case. | Retain. Map B1–B5 to the existing criteria; the private-edit pass does not establish every planning goal. |
| F4 — Amend locally; preserve accepted work | **Present:** [draft-design](../skills/feature-design/prompts/draft-design.md) and [plan-implementation](../skills/implementation-plan/prompts/plan-implementation.md) distinguish local amendments and separate designs. | **Present:** [v3-maintenance](../evals/cases/v3-maintenance/rubric.json) distinguishes private changes, public changes and historical work. | Retain. Current complete coverage of the obstacle workflow is not established by the private-edit result alone. |
| F5 — Actionable, consistent, convergent reviews | **Present:** [shared review contract](../skills/stage-development/assets/review.template.md) and corresponding author/reviewer references define findings, revision, fix claims, verification and stopping. | **Present:** [v5-review-recheck](../evals/cases/v5-review-recheck/rubric.json), sufficient/defective review cases; the selected partial-fix smoke passed. | Retain closure rules. Q2/Q3 remain for cost and usability across review operations; do not equate one invariant recheck with overall convergence. |
| F6 — Time, context/token cost and process depth | **Partial:** all skill entrypoints route by uncertainty/consequences; execute-stage rejects redundant gates. Explicit context-cost acceptance is missing. | **Partial:** [bounded-delivery](../evals/cases/bounded-delivery/rubric.json) grades depth/convergence; [budget_check](../tools/canary.py) really enforces declared elapsed budgets. It is not merely a recorded timeout. | Q2. The existing 900-second full-task case includes implementation; it does not resolve the reported document-work delay. No dependable speedup is established. |
| F7 — Hooks, Ruff, coverage, document ownership | **Present:** [setup operation](../skills/dev-workflow/prompts/setup-dev-workflow.md), Python assets and document ownership explicitly cover these. | **Present:** [workflow-setup](../evals/cases/workflow-setup/rubric.json) separately checks gate effectiveness, application coverage and document audiences. | Retain. Tooling/package checks and a fresh export do not substitute for worker behavior or the user's own environment acceptance. |
| F8 — Stage/commit/PR/release boundaries | **Present:** [execute-stage](../skills/stage-development/prompts/execute-stage.md), [prepare-pr](../skills/dev-workflow/prompts/prepare-pr.md) and [release](../skills/dev-workflow/prompts/release.md) preserve checks/review/authorization and avoid PR/version-per-commit. | **Present for bounded operations:** stale/current evidence, local-only PR scope and release-readiness cases. | Retain. Readiness fixtures do not certify a real merge/release or authorize publishing. Do not repeat prior unauthorized-main behavior. |
| F9 — Goal-derived evaluations and truthful results | **Partial:** GOALS, runner instructions and validation distinguish behavior, tooling and scorer calibration; the final goal-level acceptance map remains incomplete. | **Partial:** the scorer has explicit pass/fail/inconclusive rules, but bundled case criteria do not establish every newly stated goal. Recent repair reviews were not a calibrated full-release run. | Q1/Q4. Preserve original results; no retroactive regrading or A/B before its acceptance basis. |
| F10 — Affordable tests, neighbors and generalization | **Present:** [test cadence](../DEVNOTES.md#choose-tests-by-the-changed-behavior) and GOALS distinguish focused smoke, complete tasks and required release testing. | **Partial:** real neighboring and transfer cases exist. Earlier transfer isolation had a disclosed leak; full current release acceptance is pending. | Complete goal-to-case/neighbor selection after Q1. Keep general failure mechanisms distinct from fixture answers; no automatic all-heavy rerun. |
| F11 — Research, references and originals | **Present:** [source register](research/workflow/SOURCES.md), full selected licensed originals, [research](research/workflow/RESEARCH.md) and immutable execution evidence. Web articles are linked originals/excerpts, not full local snapshots. | **Partial:** original-contract/evidence-preservation criteria exist; systematic acceptance of research-based design claims is not mapped across the new goals. | Q1/Q4. Retain provenance and explicit preservation limits; do not claim no research was done or that every source is locally archived. |
| F12 — Whole-deliverable usability and controlled change | **Present:** [PR preparation](../skills/dev-workflow/prompts/prepare-pr.md), review contracts and repository instructions assess aggregate purpose/reviewability. | **Present:** [smoke-pr-scope](../evals/cases/smoke-pr-scope/rubric.json) checks required generated data versus unrelated output; the selected pair passed. | Retain. Prior document-usability rejection and current Q1–Q4 prevent whole-delivery acceptance; reduced file count is not sufficient. |

### Which skill needs which specification work

| Skill / operations | Retain | Specification gap to resolve |
|---|---|---|
| feature-design — intake, draft, review | Requirements/assumptions, decision/example contract, local amendment, matching review obligations. | Map each operation's goals to criteria; complete efficiency/context expectations and uncovered navigation/research-evidence judgments (Q1–Q3). |
| implementation-plan — draft, review | Outcome/dependency/acceptance structure, private-edit stability, public-change amendments. | Map both operations separately; complete time/repetition acceptance and reader/reviewer coverage without an implementation inventory (Q1–Q3). |
| stage-development — execute, review | Meaningful checks, current evidence, whole-finding closure, one usable handoff. | Make C5's effort goal assessable alongside correctness, identify uncovered review/handoff criteria and applicable neighboring cases (Q1–Q3). |
| dev-workflow — setup, PR, release | Existing tooling, doc audiences, actual-diff review, lifecycle and authorization rules. | Map each operation's output/readiness and unnecessary-work criteria; retain phase-specific evidence limits (Q1–Q3). |

F9–F11 also govern **maintenance of this skill repository**. They do not require every downstream feature to create a research archive, calibration suite or new workflow framework. Q4 concerns project guidance, not another skill or operation.

**This audit changed only documentation.** No skill/rubric/runner edit, new model trial, remote action or independent approval occurred. No old grade was changed. The next authorized work should reconcile the specification and maintained next-action guidance against this complete audit, then select tests from actual gaps.

## A. feature-design

**Function:** clarify a feature using its original requirements and existing code; produce or amend the necessary design decisions; review a design when requested.

**Expected output, depending on the requested operation:**

- **Clarification:** known behavior, consequential unresolved questions, explicit assumptions and next action. If a spec/addendum is needed, record the observable requested behavior and acceptance examples with clarification sources.
- **Design:** an opening decision summary, followed by only the supporting detail needed. A useful shape is: “Change X using Y because Z; consequence C; example input/state → result; unresolved decision or next action.” Longer designs have a navigable outline. Sources, assumptions and decision status remain identifiable.
- **Design review:** readiness, open findings and next action first; then revision/scope and actionable findings. This uses the same design requirements as the author.

**Goals / rubric dimensions:**

- **A1 — Correct contract:** preserve original requirements and confirmed answers; distinguish observed facts, assumptions and proposals. Ask questions only where the answer changes a consequential decision.
- **A2 — Glanceable decision:** the opening lets a reader recover what changes, the chosen approach, why, the material consequence and any blocking decision. The body makes supporting decisions/examples easy to locate.
- **A3 — Sufficient reasoning:** explain relevant compatibility, ownership, validation and failure behavior through concrete examples. A consequential choice has a reason and cost; persistent effects include interruption/retry behavior.
- **A4 — Proportionate amendment:** update affected decisions/examples for a local extension; preserve unrelated accepted work. Private implementation edits do not trigger a design rewrite. More analysis must resolve actual uncertainty or consequences.
- **A5 — Useful design review:** detect violations of A1–A4, explain their consequences and minimal corrections, and accept sufficient work without imposing another documentation style.

**Non-goals:** describe every function/test; own implementation sequencing; implement code during a design-only task; require a separate document or an alternatives catalogue for every request.

**Avoid:** policy/history before the decision; “handle errors gracefully” without defined outcomes; presenting guesses as requirements; rewriting the movement design for one obstacle check; lengthy review driven by wording preferences.

**Tests and concrete rubrics:**

| Test input | What to check in the result | Existing related case |
|---|---|---|
| Existing feature with settled defaults; a neighboring variant has two incompatible requirements | **A1:** keep settled defaults without reconfirmation. In the conflict variant, identify the incompatible promises and consequence; do not silently choose which promise to abandon. Intake-only output does not modify implementation. | `smoke-intake-preserve`, `smoke-intake-conflict` |
| Add obstacles to an existing movement design, with blocked-pose and continuation semantics supplied | **A2:** the opening states the changed behavior and decisive example. **A3:** explain the chosen lookup representation's relevant tradeoff; the blocked example accounts for the required state/result. **A4:** amend affected decisions while retaining unrelated movement history. Do not require one data structure regardless of constraints. | `v1-small-feature`; `smoke-design-local` supplies a smaller amendment scenario |
| Change a locally stored configuration that must remain usable after failure | **A2:** recovery choice and consequence appear before history. **A3:** explain what remains usable on invalid input/interruption and the condition for safe retry. **A4:** no speculative distributed framework. | `smoke-transfer-design` |
| Review one sufficient design and one that buries a choice which bypasses required whole-input validation | **A5:** accept the sufficient version with inspection evidence; identify the actual omitted-input counterexample in the defective version. **A2:** identify where the buried decision impedes use and propose a local correction, not a wholesale rewrite. | `review-ready`, `review-defective` (currently combined design/plan cases) |

## B. implementation-plan

**Function:** translate sufficient requirements/design decisions into delivery stages and commit boundaries; amend pending work when behavior changes; review sequencing and acceptance.

**Expected output:**

- An opening identifying the next undelivered usable outcome, its dependency/open decision and decisive acceptance.
- A short ordered list or table: **outcome/scope → dependencies and reason for boundary → acceptance evidence**. Relevant tests and documentation belong within the outcome.
- Links to authoritative design and check policy, rather than copied rationale or workflow instructions.
- For a review request: verdict, actual dependency/acceptance/maintenance problems and the needed corrections.

**Goals / rubric dimensions:**

- **B1 — Executable next step:** a reader knows what can be delivered next and what must be settled first; the opening agrees with stage order.
- **B2 — Coherent boundaries:** each stage has an observable outcome and justified boundary. Dependencies precede their consumers. A single stage is valid.
- **B3 — Assessable completion:** acceptance describes required behavior, compatibility and relevant failures, not merely “tests pass.” A partial delivery has stated usable scope and limits.
- **B4 — Maintainable plan:** implementation details stay in code/tests. Private helper/test changes leave the plan unchanged; public behavior changes update only affected pending outcomes and contracts, preserving history.
- **B5 — Useful plan review:** assess B1–B4 without requesting an implementation transcript, arbitrary extra stages or repeated policy paragraphs.

**Non-goals:** enumerate methods, files or tests exhaustively; duplicate the design; maintain several copies of current progress; create a PR/version for each stage; implement a planning-only request.

**Avoid:** “write classes → write methods → add tests” as the delivery structure; entire-plan rewrites; named-test counts; repeated cumulative-suite/hook instructions; an opening that promises the eventual feature rather than the actual next stage.

**Tests and concrete rubrics:**

| Test input | What to check in the result | Existing related case |
|---|---|---|
| Rename a private helper and add a regression test for an existing contract | **B4:** accepted plan stays unchanged; the explanation locates the change in code/tests. Adding the helper or test name to the plan fails. | `smoke-plan-maintenance`, `v3-maintenance` phase 01 |
| Change the public contract from continuing after a blocked command to stopping | **B4:** amend the affected behavior and pending stage, keep original/completed history accessible, and remove contradictory current instructions. Do not perform excluded implementation. | `v3-maintenance` phase 02 |
| Deliver an opt-in exporter change to client A while client B needs the old default | **B2:** required exporter behavior is available before client A depends on it. **B3:** acceptance covers opt-in behavior and preserved default; necessary checks are not deferred until after “complete.” **B5:** no gratuitous infrastructure stages. | `smoke-plan-delivery` |
| Plan a read-only preview followed by a later confirmed import | **B1:** opening identifies preview as next, not completed import. **B2:** import depends on the validated preview. **B3:** stage acceptance distinguishes preview from state mutation. | `smoke-plan-preview-import` |
| Review a sufficient plan and a variant that ships before required validation | **B5:** accept the sufficient plan; flag the invalid ordering with the affected behavior and correction. Do not demand a test/function inventory or split a coherent stage for formatting reasons. | `review-ready`, `review-defective` |

## C. stage-development

**Function:** implement a bounded outcome, verify it with applicable checks and required review, fix substantive findings, and leave a usable handoff. Also support a review-only operation.

**Expected output:**

- The working code diff and relevant tests/docs for the requested outcome.
- Observed check results, remaining material issues and next action in one existing status record or a sufficient completion response.
- A review report, when requested/required: **verdict + open findings + next action; scope/revision; finding location → trigger → consequence → correction → verification**.
- Recheck dispositions distinguish open concerns, author-reported fixes, reviewer-verified closure and accepted limitations.

**Goals / rubric dimensions:**

- **C1 — Correct outcome:** fulfill the actual behavioral contract, including relevant compatibility/state/failure invariants. Tests use meaningful expectations rather than copying implementation logic.
- **C2 — Effective verification:** execute applicable gates, inspect hook edits and failures, and tie claims to the content actually checked. A configured hook, empty test collection or stale green log does not prove success.
- **C3 — Review and closure:** catch material defects, verify the whole concern at the actual revision, retain finding identity, and stop blocking once it is fixed. Distinguish self-review, independent review and human acceptance.
- **C4 — Usable continuation:** a fresh context can identify completed work, blockers, evidence and next action from one current record; affected stale evidence is rechecked.
- **C5 — Proportionate completion:** an understood local change can proceed directly when authorized. Extra investigations/review rounds must address a concrete uncertainty, defect or applicable requirement. Report unfinished attempts and actual effort honestly.

**Non-goals:** automatically start new design/planning phases; refactor unrelated code; replace required independent/human review with self-review; publish a release; manufacture a handoff file when the response already suffices.

**Avoid:** tests without decisive assertions; author claims treated as verified fixes; heading-only verification of a whole-pose defect; cosmetic review loops; repeating completed work; claiming completion after timeout.

**Tests and concrete rubrics:**

| Test input | What to check in the result | Existing related case |
|---|---|---|
| Implement a counter change with real tests/hooks and required reviews | **C1:** the observable counter behavior satisfies independently derived examples. **C2:** actual gate failures block progression; checks run on the candidate. **C3:** absent required review remains pending. **C4:** handoff makes that pending work actionable. | `counter-stage` |
| Recheck a partial fix, then a fully corrected revision | **C3:** keep the finding open when one affected state component still changes; close it only after the whole invariant is verified. Retain original finding and revision-specific dispositions. A fully corrected version must not inherit the historical blocker. | `smoke-review-partial`, `v5-review-recheck` |
| Resume a previously verified stage; neighboring variant has changed code | **C4:** reuse still-applicable review in the unchanged variant and complete the outstanding required check. **C2/C3:** identify changed evidence in the stale variant and recheck the affected behavior rather than accepting the old verdict. | `smoke-stage-resume`, `smoke-stage-stale` |
| Complete an understood local feature with a supplied task budget | **C1:** actual implementation passes independent behavior checks. **C5:** inspect the trace for unnecessary new phases, repeated closed findings and unfinished work; report worker cost separately from evaluator cost. A correct but timed-out run is not completed acceptance. **C4:** next state is usable. | `bounded-delivery`; `transfer-transcript-search` adds an open-ended feature |
| Complete a file import where corruption or interruption can leave partial state | **C1:** independently check promised error behavior, preserved usable state and retry. **C2:** original tests passing cannot override a demonstrated contract failure. **C3:** a scoped fix receives whole-concern verification without encoding that fixture's answer in the skill. | `transfer-packet-import` |

## D. dev-workflow

**Function:** adapt repository setup and document ownership; prepare a coherent PR; prepare or perform a versioned release within authorization. Select the requested operation, not all three automatically.

**Expected output:**

- **Setup:** usable environment/check commands and working requested configuration; an accurate report of what is configured, installed and actually verified. Include Ruff/tests/coverage in an appropriate requested Python setup while respecting an adequate existing stack.
- **Documents:** README for users (purpose, runnable usage, examples, limits, navigation); DEVNOTES for contributors (setup, hooks/checks/coverage, debugging and contribution/release operations); CHANGELOG for significant completed impact; AGENTS for actionable agent conventions and policy links. Adapt useful existing conventions.
- **PR:** concise title/body describing the final problem, resulting behavior, useful example, material consequences, actual validation and remaining limits, matching the full intended diff.
- **Release:** consistent version/notes/tag/artifact and exact observed publication state, or the specific unmet readiness condition.

**Goals / rubric dimensions:**

- **D1 — Working setup:** documented commands work for the actual repository. Hook changes propagate intended lint/test failures. Existing useful tooling is retained.
- **D2 — Meaningful coverage:** report coverage of the application under change, including missing lines/branches where supported. Respect justified repo thresholds; do not treat coverage percentage as correctness.
- **D3 — Reader-specific documentation:** users can run the product from README; contributors can find the authoritative check/development instructions; change history and agent rules have clear owners without duplication.
- **D4 — Reviewable delivery:** the PR describes actual final behavior and every included file serves the task. Retain required generated artifacts; keep disposable output and bulky raw-run archives out of the maintained source diff.
- **D5 — Accurate lifecycle:** stage commits do not automatically become PRs or version bumps. Release evidence matches the final candidate and required deferred checks. Authorization, local checks, remote CI, merge, tag and publication remain distinct facts.

**Non-goals:** redesign feature behavior; impose the same toolchain/file scaffolding on every repo; invent coverage floors; require a PR per commit; grant permission to push/merge/release from a procedural document.

**Avoid:** README as a development diary; CHANGELOG as a test log; multiple owners of check commands; reporting tool-runner coverage as application/skill quality; huge source PRs full of raw evidence; release claims based on stale checks.

**Tests and concrete rubrics:**

| Test input | What to check in the result | Existing related case |
|---|---|---|
| Adapt an existing Python hook and add/report available application coverage | **D1:** preserve the working setup, actually run the intended gate, and verify the changed gate rejects failures. **D2:** report current application coverage and missing code; no invented threshold or substituted tool coverage. | `workflow-setup` |
| Prior “green” output only lists test files; neighboring cases have failed or missing child results | **D1:** run the useful current gate. **D5:** distinguish what each prior/current record establishes; do not turn a file listing or missing result into executed success or an invented failure. | `smoke-setup-evidence`, `smoke-setup-child-evidence`, `smoke-setup-baseline` |
| Reorganize a README containing useful usage mixed with developer history | **D3:** preserve runnable usage and public behavior in README, put maintained development instructions in DEVNOTES, retain history access, and keep each command authoritative in one place. Moving content must not delete useful information or create empty ceremony. | `workflow-setup` |
| Prepare a PR containing a required generated CSV example and unrelated preview output | **D4:** retain the required sample, exclude the unrelated output from the proposed scope, and describe actual behavior/checks. Do not use a blanket generated-file ban or copy logs into the PR. **D5:** remain local when only drafting is authorized. | `smoke-pr-scope`, `smoke-transfer-pr` |
| Assess a release with current evidence and a neighboring stale-evidence variant | **D5:** recognize the genuinely ready candidate, reject readiness when required evidence no longer applies, and identify the next required action. No fabricated tag/publication or extra authorization round when authorization already exists. | `release-ready`, `release-stale` |

## Time and unnecessary work — proposed acceptance

**This is skill quality in ordinary development, not an interview schedule.** The owner reported a small obstacle extension taking roughly 15 minutes. Recording elapsed time or saying “be proportionate” does not establish that this problem is solved. Efficiency applies to all four skills, including authoring, review and rechecks.

### Goal and unresolved acceptance threshold

The user should receive the required usable result within a task-appropriate time budget, without paying repeatedly for settled decisions. Quality requirements still apply: a fast incomplete design or premature review closure fails.

The previous five-minute suggestion was assistant-invented and is withdrawn. The owner reported unacceptable time spent on a small obstacle extension; that establishes an efficiency problem, not a replacement numeric threshold. Identify the actual work, unnecessary repetition and time distribution, then define scenario-appropriate acceptance as part of the complete skill specification. Do not silently equate document work with implementation/code testing, or let this single concern replace the other feedback.

### Rubric, applied separately from output quality

| Criterion | Pass | Fail / inconclusive |
|---|---|---|
| T1 — Time to usable result | A complete required output and final response arrive within a justified, predeclared operation/case budget. Record start/end and time spent in authoring, required review and repair. | Exceeding that budget fails its time criterion. Lost timing/completion evidence is inconclusive. A case without a defined acceptable budget cannot establish time acceptance; a saved file alone is not completed delivery. |
| T2 — Unnecessary repetition | Subsequent investigation, rewrite, recheck or full-suite run addresses a named unresolved decision, changed behavior, material finding or mandatory requirement. | Rewriting accepted movement history, rechecking an unchanged closed finding, or repeating the same gate merely to accumulate reassuring evidence. Cite the redundant actions and what had already been established. |
| T3 — Stop when sufficient | Design ends once consequential decisions/examples are adequate; planning ends once next outcome/dependencies/acceptance are usable; review ends when no material concern remains; execution/setup ends after required work/checks. | Another round changes only stylistic preferences, expands scope without a need, or recreates working setup after the requested result is available. Real unresolved defects still require correction. |
| T4 — Quality preserved | The applicable skill goals pass alongside T1–T3. | Time is saved by dropping failure behavior, hiding unresolved findings, skipping required checks or claiming unperformed review. Speed cannot compensate for these failures. |

Measure user-facing elapsed time from invocation to usable completion, including model/tool waits and required development review. Report evaluation-only reader/grader time separately. Preserve available token counts, individual operation durations and all attempts; overlapping work must not be summed and called wall-clock time. Distinguish slow service response from unnecessary workflow using the trace, without excluding either from the user's observed wait. A time-budget failure alone does not diagnose its cause. Missing records do not become evidence of success. One passing attempt cannot establish reliable speed.

### Cases derived from these goals

| Case | Concrete expectation / rubric | Existing material and gap |
|---|---|---|
| Fully specified obstacle extension: requested design + plan + document review | Measure time to usable completion; define the acceptable budget before running (T1). Check local amendments and no repeated settled decisions (T2), finish after adequate review (T3), and retain blocked-state/continuation semantics plus clear entrypoints (T4). | Reuse the small-change context from `v1-small-feature`; its current plan-only request does not itself execute the complete proposed review workflow. This timed case is not finalized, implemented or run. |
| Same-size local change in another domain | Use a comparably bounded, fully clarified optional setting or filter change with the same timed operations. T1–T4 must hold without Rover-specific instructions in the skill. | Select/freeze the actual transfer input before a skill correction; this row is a case proposal, not an executed benchmark. |
| Private helper/test change; already sufficient review | Planning returns without rewriting the plan; review produces a supported ready verdict without a cosmetic fix loop (T2/T3). Record time rather than counting a no-op rewrite as useful progress. | Existing `smoke-plan-maintenance` and `smoke-review-ready` provide contexts. Existing results are not retrospectively graded against new budgets. |
| Small diff with a consequential unresolved recovery/compatibility issue | Identify the uncertainty and necessary next investigation; do not force the local-change route or remove essential reasoning to meet its time target (T4). Set this operation's scope/budget before running it. | Existing `route-uncertain` and `smoke-transfer-design` protect against over-simplification; they are not subject to the fully specified local-change target. |

### Current evidence and remaining work

The current `bounded-delivery` case has a 900-second whole-task budget and qualitative depth/convergence criteria. It includes implementation and code review, so it does not establish acceptable time for the reported obstacle document work. The [validation report](VALIDATION.md) records 77–300-second individual operation workers and an incomplete final invocation; it explicitly does not establish dependable speedup. The original reported obstacle run has not been inspected in this revision, so its exact time distribution and cause remain unknown.

First reconcile all feedback in the problem inventory with the per-skill goals and expected outputs. Efficiency and these proposed stop conditions are part of that review. Only then finalize suitable cases/rubrics, obtain actual traces and correct observed general failure mechanisms. Keep original failures and protect neighboring behavior; do not change a target after failure merely to obtain a pass.

## What this proposal changes, and what it does not establish

The cards define the proposed product behavior and show how to test it. Existing case names above identify reusable material; **they do not claim that every proposed goal is already covered or has passed**. Existing combined criteria need reconciliation with these goal-specific judgments before using them as acceptance for this proposal.

The [validation report](VALIDATION.md) records earlier actual runs, including failures and uncertainty. Those results keep their original criteria and skill versions. This rewrite changes no skill, test fixture, scoring prompt or historical result, and runs no new LLM experiment.

Review these four cards for missing/wrong goals first. Then align the affected existing cases/rubrics, add only genuinely missing cases, and run selected focused tests. Complete cases exercise interactions and required release acceptance. Preserve inputs, source versions, raw results and failures; do not choose an A/B wave before its product requirements and acceptance are defined.
