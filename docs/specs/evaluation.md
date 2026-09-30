# Evaluation specification

**Purpose:** turn the four skill contracts into checkable cases without losing the owner's feedback. This page and the four skill cards define the prospective priority/scoring contract. [Validation](../VALIDATION.md) distinguishes definitions, scorer checks and actual skill results.

**Selected executable migration:** `v1-small-feature`, `v3-maintenance` and
`bounded-delivery` now carry priority-based criteria and prospective time budgets.
The [three-case proposal](../proposals/priority-canary-pilot.md) owns this bounded
migration through the maintained runner. Other cases retain their historical
binary scheme. Actual worker trials require matching executable contracts,
focused checks and passing case-specific scorer controls; definitions alone do
not establish readiness. Archived results keep their original interpretation.
The selected qualification tests the readiness boundary, not reliable distinctions
between 3, 4 and 5. The remaining 55 cases have not migrated to this contract.

## Applying the rubrics

Select the requested operation and its relevant goal rows from the skill card before execution. Review tasks assess the review, including its judgments about supplied content; they do not require the reviewer to fix that content. Composite tasks select only their actual operations and also assess whole-task completion/cost. Do not automatically invoke every skill.

| Priority | Judgment | Effect |
|---|---|---|
| P0 · unequivocal boundary | Binary, with the concrete prohibited condition and observable evidence declared in the case. | A demonstrated violation prevents readiness. Use only a few applicable boundaries, not every quality concern. |
| P1 · essential result | 1–5 with the operation's concrete anchors and cited output/trace. | 1–2 needs material repair; **3 is sufficient**; 4–5 records added benefit within the requested scope. |
| P2 · presentation preference | Advisory observation after judging the result. | Does not block completion, require another round or compensate for a core defect. |

**Scale:** 1 defeats the purpose; 2 has a material gap; 3 fulfills the intended use; 4 provides a clear additional benefit; 5 provides exceptional benefit on the same task. The cards give concrete 1/2/3 and 4/5 examples. Equivalent supported outcomes can earn the same score; matching an example or template is not required. More files, tests, alternatives, headings or review rounds do not earn points. If no further benefit is established, stop at 3 rather than manufacture work to reach 5.

**Overall decision:** ready requires no demonstrated P0 violation and every selected P1 dimension at least 3. A material known gap means needs work. Missing critical evidence means not established for that dimension; it is not zero or proof of worker failure. Keep known defects visible even when other dimensions are unassessable. Invalid grader citations are assessment errors. Do not average away a core gap or count the same defect several times to inflate severity. Inapplicable criteria remain unscored.

**P0 selection:** a forbidden external mutation (push/tag/publication), modifying protected product files in an explicitly read-only task, and exceeding a declared hard time limit are possible objective boundaries. Scope must be explicit and observable. Ordinary correctness, clarity, review judgment and efficiency belong to P1. Deterministic tests can still report binary facts, such as a wrong state transition; those facts support the relevant quality score without making every sentence an independent veto.

**Migration requirement:** each executable criterion must carry its priority, applicable operation, goal, concrete anchors/condition and decisive evidence. Reuse existing cases and goal IDs; split compound criteria when they currently mix substantive outcome with optional presentation. Case-scoped controls must contrast a material defect (2 or below), a usable result (3 or above), and an equivalent cosmetic variation that does not cross the readiness boundary. Check high-score distinctions with supported examples or acceptable adjacent-score ranges; do not require spurious exact agreement on subjective polish. Expected scores remain hidden from the scorer. Preserve original cases, inputs, labels and raw results under their old versions; never retrospectively choose priorities to obtain a pass.

## Last step within the task

The normal sequence is **do the substantive operation → check its result → organize it for the reader → deliver**. Use templates or examples when they reduce work; they are not fields to carry through every decision. Presentation belongs mainly in the final edit or an already-requested artifact review. This does not postpone discovering missing requirements, unsafe behavior or unsupported decisions until formatting.

For a design, settle the choice and consequences before editing its opening. For a plan, settle outcomes/dependencies/acceptance before choosing a table or list. For review, settle findings and dispositions before making the verdict easy to find. For execution/setup, complete relevant checks before reporting what works. The last edit may remove boilerplate, expose the conclusion, group related detail and add useful navigation. It must preserve substantive content and avoid fresh research or an unchanged check/review loop. A newly discovered material defect uses the existing correction path; minor preferences do not create another task.

Score the final result's actual readability as P1 where needed, and optional surface preferences as P2. The agent need not emit a checklist or self-review report to prove it performed this step. Existing prompts already contain after-generation checks; runtime migration should simplify and align that path rather than add a second one.

## Efficiency and context

Applies to **A6, B6, C5 and D6**, including document review. The objective is timely usable completion without material avoidable overhead, not merely recording duration or demanding a perfectly minimal command trace. Judge the effect on completion, context and maintenance relative to the task. Incidental local navigation or verification is advisory when it has no material consequence; small repetitions can still accumulate into a material burden. There is no universal command, byte, minute or repetition allowance.

| P1 score | Concrete time / work anchor |
|---|---|
| 1 | No usable result, or extreme avoidable replay/review/rebuild dominates the bounded task. A known hard-deadline breach is also recorded separately as P0. |
| 2 | A material avoidable full rewrite, duplicate live maintenance, repeated unchanged gate/review or lost-state replay; or usable completion misses the case's declared target. Correct output alone does not remove this gap. |
| 3 | Usable completion within the declared target; work addresses actual scope, uncertainty and required gates, including the final readability edit. Incidental navigation and reasonable local verification are acceptable. |
| 4 | Meets 3, with evidence that reuse or a better boundary avoids meaningful work while preserving the result. A faster clock alone does not establish the benefit. |
| 5 | Meets 4 and resolves the task's interacting constraints without otherwise necessary repeated work/context reconstruction. Requires concrete comparative work evidence, not an assertion of efficiency. |

Time is measured from task invocation through usable delivery, not the first saved file. Include required sequential skill operations, checks, development reviews and the final edit in the whole-task record. Per-operation scores cannot hide a slow combined workflow. Record model/tool waits, evaluator-only grading and human waiting separately where possible. Exclude a wait from a contractual clock only if that clock's rules say so beforehand; retain end-to-end elapsed time as well. A runner watchdog is not evidence of acceptable latency.

**Targets for the next local-regression migration:** these are prospective product budgets for fixed-prerequisite local work, not measured guarantees or universal instructions embedded in a skill. They are not applied to old runs. The case request must carry its scope and budget before another trial.

| Task class and included work | Usable target / P1 ≥3 | Hard stop / P0 boundary |
|---|---:|---:|
| One local operation: supplied small repo/requirements; draft or amend a short document, review/recheck a supplied change, repair a supplied small finding, or adapt one prepared check. Includes relevant verification and final readability. | 5 minutes | 10 minutes |
| Local obstacle extension through design + pending-plan amendment, with movement code and clarified contract supplied. No implementation/research/env bootstrap in this case. | 5 minutes total | 10 minutes total |
| Complete local obstacle extension including code, meaningful tests, configured fast checks and the review actually required by the case. | 10 minutes total | 15 minutes total |

The first row is a ceiling for a useful small-operation test, not a desired duration for trivial work; material waste still scores below 3 inside it. The second row prevents two individually acceptable five-minute steps from consuming ten minutes in aggregate. A 10–15-minute local design/plan loop therefore misses its target; thirty minutes is never acceptable for these small-task classes. Cases with real discovery, migration/recovery risk, environment installation or slow mandatory suites need separately justified budgets from their actual scope **before** execution. They are not silently waived or forced into the local class.

Existing deadlines remain scoped: `bounded-investigation` supplies 300 seconds for investigation; `bounded-delivery` supplies 900 seconds for the complete workflow. Keep those original contracts. For any unmapped case without a target, work quality can be assessed, but latency acceptance remains not established; define a justified target before using it to accept efficiency. Do not silently call it an efficiency win.

Retain elapsed time, available tokens and the operations behind alleged wasted work. Do not invent attribution, double-count parallel work or claim reliable speed from a single run. Compaction alone is not a defect; losing settled state and replaying work is. The retained Rover investigation reports about 17m35s including clarification/waits and real YAML scope expansion, with compaction; the skills were not installed. Preserve that scope and provenance when constructing regressions. It motivates the tests, not a demonstrated failure of these exact bundles.

**Cases:** apply effort judgments to `route-local` versus `route-uncertain`, the small-feature/YAML sequence, unchanged versus stale stage resumption, and PR/setup/release operations listed in the cards. For the reported failure, check broad rewrites, test-count inventories, buried closure and unnecessary continuation together; do not discard real requirements to make it faster.

## Output usability additions

Judge the final result after its same-task editing step. A brief opening or obvious nearby structure should answer the relevant reader question, with supporting detail consistent and navigable. These are content questions, not mandatory fields or a sentence-by-sentence gate:

| Operation | Reader should quickly understand |
|---|---|
| Intake | What is known, what material choice remains, and what happens next? |
| Design | What changes, what was chosen and why, what consequence/example matters? |
| Plan | What is the next undelivered outcome, prerequisite and decisive acceptance? |
| Any review | Is it ready, which material issues remain, and what correction/decision is next? |
| Stage handoff | What works, what actually passed, what remains blocked, and where to resume? |
| Setup / PR / release | What changed or is ready, what evidence supports it, and what remains to do? |

A usable answer scores 3 even with different headings/order; a material absence, contradiction or need to reconstruct the conclusion from history scores 2 or below. Exact format and redundant summaries are P2. No next-action sentence is needed when the task is complete; no extra example is needed when the consequence is already clear. Finding a keyword is insufficient. Existing restricted-reader executions remain a machine proxy; direct artifact inspection is not a reader run, and neither is human acceptance.

**Cases:** reuse intake smokes, `v1-small-feature`/`v2-scope-extension`, `smoke-plan-preview-import`, sufficient/defective reviews, `smoke-handoff-opening`, `workflow-setup`, PR and release-readiness cases. Add the relevant explicit questions/criteria per operation instead of creating a parallel suite.

## Review closure

Applies identically to **A5, B5 and C3**. Preserve the original finding and identify each reviewed revision. Distinguish open, author-reported fixed, reviewer-verified resolved, evidence-backed rebuttal and accepted limitation. Recheck the entire affected contract; a partial fix stays open and a fully verified fix closes. State actual review mode and static/runtime/human evidence limits. The final edit makes the current verdict and remaining action easy to find without requiring exact labels or a new report format. These are P1 judgment/evidence requirements; pure style suggestions are P2.

| Operation / case | Decisive checks |
|---|---|
| Design: existing `v5-review-recheck` | Original whole-pose finding remains open at partial D2; complete D3 closes it at document level, preserving original finding and failed recheck. Do not claim runtime verification. |
| Plan: `plan-review-recheck` | Supply original missing-prerequisite finding and two plan revisions: first adds the prerequisite description but still schedules the consumer first; second corrects ordering and preserves old-client acceptance. First stays open, second closes after checking the whole dependency/compatibility concern. Retain both dispositions; no implementation claim. |
| Code: existing `smoke-review-partial` and `v6-execution-handoff` review/fix/recheck phases | Keep incomplete code invariants open; close after required checks/review verify the actual corrected code. Preserve stale/failed evidence. Design-only D2/D3 results cannot satisfy this operation. |

## Release execution

**D5/D6 require more than readiness reports.** Keep existing ready/stale cases' no-tag/no-metadata-change scope intact. The separately versioned `local-release-execution` case now supplies these inputs and checks; defining it is not a worker-run result.

- **Input:** isolated small repository, working check/build commands, one authoritative version source, significant Unreleased notes, explicit compatibility/version policy, and task-scoped authorization for local preparation/commits/tag/build. A supplied publication-state adapter represents remote observations; it performs no network publication. Existing-tag and uncertain-publication variants are supplied separately.
- **Preparation rubric:** choose the version from the supplied policy/change; update matching dated notes and metadata, retain a new Unreleased section, and describe completed changes only. A version changed in one of several authoritative copies or planned work listed as shipped fails.
- **Tag/artifact rubric:** complete required checks/review on the final candidate, tag that exact commit, build from its content, and check the actual distributable. Inspect Git references, embedded version/source identity and artifact execution/output. A workspace-only test cannot prove the tagged artifact; mismatched commit/version or stale merge evidence fails.
- **Retry/conflict rubric:** inspect an existing tag and observed publication state before another action. A matching completed publication requires no duplicate; an existing conflicting tag remains unchanged and the conflict is surfaced. An uncertain response is not success. Silent tag replacement, blind republishing or unsupported publication claims fail.
- **Limits:** record actual local execution separately from supplied/simulated remote state. These checks can establish local consistency and retry decisions; they cannot certify a real hosted release.

## Research and original evidence

For **A1/A3 and D4/D5**, consequential claims must link observed code, supplied requirements or an attributable source; inference and unverified guarantees remain explicit. Preserve original findings/failed results rather than overwriting them.

Extend `smoke-transfer-design`'s adequacy judgment: an unconditional recovery guarantee without support fails; a supported mechanism with stated limitations passes. Use a frozen source/contract available in the case when a source claim is required, so a disconnected worker is not asked to fetch unavailable evidence. Do not demand a research essay for a routine local change.

Project research uses the existing [source register](../research/workflow/SOURCES.md), with primary sources, dates/versions, permitted originals/excerpts and explicit preservation limits. Sources inform decisions; they are not proof of measured skill benefit.

## Repository-maintainer acceptance

These duties belong to maintaining this skill package, not every feature it helps implement.

| Requirement | Acceptance |
|---|---|
| Goals before evaluation | Each applicable skill goal and operation has a case, concrete rubric and decisive evidence. Distinguish existing coverage, proposed additions and actual results. Scorer calibration tests the scorer; tooling checks test the tooling. |
| Affordable regression protection | Choose affected smoke operations and neighboring countercases; complete tasks cover interactions and required release gates. Repeated heavy runs require changed behavior, unresolved risk or policy. |
| Generalization | Preserve real scope, include an uncertain/consequential neighbor, and correct a general mechanism. No fixture answers or score-driven rubric changes. A disclosed isolation failure remains a limit; a used transfer case becomes regression coverage. |
| Truthful delivery | Retain versioned inputs/settings/raw outputs/failures/grades separately from source clutter; report what ran and what did not. Whole-package review includes installability, navigation, useful content and scope, not only check/file counts. |

## All owner feedback mapped

| Feedback | Specification / concrete checks |
|---|---|
| F1 · Per-skill contracts | All four cards: function/output/goals/non-goals, failure examples and case mappings. |
| F2 · Glance/examples/outline | A2/A3, B1/B3, C3/C4, D3/D4/D5; operation-specific reader questions above. |
| F3 · Plan granularity | B2/B3/B4/B6; private-edit, opt-in delivery and preview/import cases. |
| F4 · Local amendments/history | A4/B4/C4; obstacle→YAML and private→public-change cases. |
| F5 · Review quality/closure | A5/B5/C3; sufficient/defective reviews and partial→complete fix. |
| F6 · Time/context/process depth | A6/B6/C5/D6; all efficiency judgments and uncertain/consequential neighbors above. |
| F7 · Setup/docs/coverage | D1/D2/D3; effective gate, real coverage and audience cases. |
| F8 · Commits/PR/release | B2/C2/C3/D5; stage evidence, local PR and ready/stale release cases. |
| F9 · Meaningful evals/results | Applying rubrics + maintainer acceptance; concrete criteria in the actual grading packet, no premature A/B. |
| F10 · Cost/neighbors/generalization | Maintainer acceptance; changed-operation smokes, paired countercases and complete-task limits. |
| F11 · Research/originals | A1/A3/D4/D5 + research/evidence rules; source-boundary and evidence-freshness judgments. |
| F12 · Whole result/change discipline | A4/B6/C5/D4/D6 + maintainer acceptance; whole PR scope and readable skill entrypoints. |
| F13 · Priority and attention | Per-operation P1 dimensions/anchors, task-specific P0 boundaries and P2 examples on every card; same-task final readability step; equivalent format must not change readiness. |

## Readiness and next work

Three existing heavy cases now implement this contract through the maintained scorer and runner, with reviewed material-defect/usable/cosmetic controls. Their qualification covers the readiness boundary only; upper-score precision is unestablished. The other 55 cases retain their prior contracts. Current worker trials also expose scorer completion/cost problems: resolve those from retained evidence before broader migration. Definitions and passing controls do not establish actual skill performance. No A–B comparison or full-release acceptance follows from this partial migration. Natural-language activation remains a known coverage gap, not the automatic next test. [Current outcomes](../VALIDATION.md) distinguish actual work, scoring and independent inspection.
