# Skill specifications — review entry

**Current result:** all four skill cards define operation-specific outputs, core priorities and concrete 1–5 scoring anchors. All four runtime bundles are revised. Three existing heavy cases now implement readiness-based priority scoring; 55 cases retain their prior contracts. Actual scoring still has completion/cost limitations. [Results and limits](VALIDATION.md).

## Proposed priority and scoring contract

**Do the substantive task → check the result → make it readable → deliver.** Final readability/formatting stays inside the same task. It is not a separate review cycle. Existing prompts already contain after-generation checks; the runtime revisions simplify and align that path.

| Priority | Meaning | Acceptance |
|---|---|---|
| P0 | A few explicit, observable boundaries, such as forbidden publication or a declared hard deadline | Binary veto only when unambiguous |
| P1 | Essential behavior, decisions, usability and efficient completion | 1–5, with **3 = usable**; no need to chase 5 |
| P2 | Preferred headings, layout or redundant summaries | Optional final polish; cannot block completion |

Each skill card below maps its operations to relevant dimensions and gives concrete anchors and cosmetic counterexamples. A readable alternative format receives the same core score; a buried decision or wrong coverage measurement remains substantive. Missing evidence is not zero; core defects cannot be averaged away. [Shared rules and whole-task time budgets](specs/evaluation.md) define the remaining boundaries, including the slow obstacle-change regression.

**Review/status:** independent review of the operation-level definitions found one material issue: inspection must score accurate diagnosis, not require repair of the supplied system. It was corrected and reviewer-verified closed. Three existing heavy cases now implement priority scoring; the other 55 retain their prior contracts. The runtime revisions, scorer qualification limits and actual trials are recorded separately in validation. Historical results keep their original meaning. [Original priority feedback](sources/user-workflow.md#u11--task-attention-priority-and-graded-quality) · [Final-step clarification](sources/user-workflow.md#u12--readability-as-the-final-step-of-the-same-task).

| Read one skill | Its deliverable |
|---|---|
| [feature-design](specs/feature-design.md) | Clarification, design decisions and design review |
| [implementation-plan](specs/implementation-plan.md) | Delivery outcomes, dependencies, acceptance and plan review |
| [stage-development](specs/stage-development.md) | Working changes, checks, review closure and handoff |
| [dev-workflow](specs/dev-workflow.md) | Setup/docs, PR and authorized release |

[Shared evaluation rules and complete feedback mapping](specs/evaluation.md) · [Original feedback](sources/user-workflow.md) · [Prior audit and superseded draft](OUTPUT_REQUIREMENTS_DETAILS.md).

## Feedback retained

| ID | Problem or missing deliverable you raised | What the specification must retain |
|---|---|---|
| F1 | Skill definitions and concrete output requirements were never clearly presented. | Per skill: function, expected output, goals, non-goals, failure modes, then corresponding cases/rubrics. Reusable templates/self-checks reduce context burden; author and reviewer share the contract. |
| F2 | Design/plan/review documents cannot be glanced through; long text has no useful outline. | A short usable opening and navigable supporting detail. Design choices need reasons, consequences and concrete examples; length reduction must preserve necessary information. |
| F3 | Implementation plans paraphrase every function/test and repeat workflow boilerplate. | Plan delivery outcomes, dependencies, commit boundaries and acceptance. Adding a private helper/test must not require maintaining a parallel prose implementation. |
| F4 | Adding one obstacle causes entire design/plan rewrites. | Decide when to amend versus create a document; update affected decisions/pending work, preserve unrelated accepted work and original history. |
| F5 | Review findings lack clear status; writing/review expectations conflict; repeated rounds do not converge. | Actionable findings and visible open → author-fixed → reviewer-verified states; verify full fixes, retain history, accept sufficient work and stop cosmetic loops. |
| F6 | Small changes take 10–15 minutes and trigger context compaction; ordinary use becomes slower and more complex. | Time, token/context cost and unnecessary repetition are product-quality concerns. Choose process depth by actual uncertainty/consequences; do not turn a workflow problem into an interview schedule or chase engineering metrics. |
| F7 | Basic dev setup and document ownership were missing or mixed together. | Working hooks, Ruff and application coverage; README for users, DEVNOTES for contributors, CHANGELOG for significant changes, AGENTS for agent instructions. Respect useful existing-repo conventions. |
| F8 | Stage/commit/PR/version/release behavior is unclear. | Relevant checks before commits, requested agent/human review and fixes, then next stage; coherent PR delivery and authorized version/tag/release. No automatic PR per commit or unexpected push to main. |
| F9 | Packaging tests and grader examples were presented confusingly; skill quality and coverage were not demonstrated. | Define goals before cases/rubrics; distinguish behavioral tests, tooling checks and scorer calibration. Show what ran, its actual grading, what remains untested and each requirement's coverage. Do not start A/B before this basis exists. |
| F10 | Heavy tests are too costly for every edit; isolated prompt fixes can break neighbors or overfit. | Focused LLM smoke tests for responsibilities, realistic complete tasks for interactions/release, recorded regression evidence and neighboring cases. Avoid both toys and oversized canaries, rubric hacking and fixture-specific fixes. |
| F11 | Research and original evidence were omitted or replaced by summaries. | Research real development/design/LLM workflows and reusable skills; retain references and attributable originals, including the supplied OpenAI eval article. Preserve raw run inputs/outputs, failures and review dispositions. |
| F12 | The proposed deliverable itself became unreviewable: a sprawling document and a 32,250-file PR. | Review the whole result against the original goal, not just local checks. Keep the source deliverable useful and concise, link evidence, review proposals before substantive changes, and test the changes. |
| F13 | Peripheral hard requirements compete with the actual task; binary rubrics flatten differences in importance. | Task-first skill prompts and aligned rubric priorities; anchored quality scores, few unequivocal vetoes, sufficient completion and nonblocking polish. |

**Historical specification review:** independent review found two gaps, in cross-operation review closure and release execution. Both were corrected and reviewer-verified closed; no material specification finding remains. The original review and recheck are retained locally in artifacts/specification-review/review.md. This is specification acceptance for case adaptation, not proof that the skills run well.

**Earlier step:** the definitions above were reviewed for binary case adaptation. Subsequent trials and the owner's priority feedback motivate the prospective replacement at the top of this document. That earlier review does not establish readiness of a priority-aware grader or reliable skill behavior.
