# implementation-plan — specification

**Function:** turn decisions into delivery stages; amend pending work; review feasibility and acceptance.

**Goals:** an obvious next outcome and a plan that stays useful as code evolves, without costly replanning.

**Non-goals:** rewriting design, narrating every function/test, implementing a planning-only request, PR/version ceremonies per stage.

## Expected output

**Runtime prompts revised; production executable rubrics still use the older binary scheme.** Scoped local trials and remaining limits are recorded in [validation](../VALIDATION.md). First settle delivery outcomes, dependencies and acceptance; finally organize the result so a reader can identify the next outcome and inspect supporting detail. A table or a short list can both work. The final readability edit stays within this task, with no mandatory extra review.

| Operation | Result to produce | P1 dimensions to score |
|---|---|---|
| Create plan | Coherent delivery increments with available prerequisites, decisive acceptance and relevant tests/docs. | B1, B2, B3, B4, B6. B4 checks maintainability, not history that does not yet exist. |
| Maintain / amend | Preserve the plan for private code/test edits; update affected pending outcomes for a public contract change. | B1, B3, B4, B6; B2 when dependencies/boundaries change. |
| Initial review | Supported feasibility verdict and material corrections against the supplied plan. | B5, B6. B5 evaluates B1–B4, including whether the verdict itself is easy to find; no authoring requirement. |
| Recheck | Disposition of the existing dependency/acceptance concern against actual revised ordering and behavior. | B5, B6. |

Example: “Add blocked movement; depends on existing movement; accept when blocked pose, result, continuation and turns satisfy the agreed examples.” Do not enumerate 30 future test methods.

## Goals and rubrics

Selected dimensions are **P1**, with **3 = usable**. The [shared rules](evaluation.md) define evidence, P0 boundaries, time and optional polish. Score the outcome; do not reward prose implementation inventories.

| ID · priority | 1 / 2 — needs repair | 3 — usable | 4 / 5 — additional benefit within scope |
|---|---|---|---|
| B1 · P1 Next outcome | **1:** no identifiable deliverable. **2:** opening promises import but next stage only previews, or completed work is presented as next. | Reader quickly identifies the same next usable outcome, prerequisite and acceptance throughout the plan. | **4:** partial versus eventual delivery is especially clear. **5:** a concise example makes a subtle partial-delivery limitation immediately understandable. |
| B2 · P1 Boundaries | **1:** sequence cannot be executed. **2:** consumer precedes unavailable dependency, or arbitrary technical layers delay every usable result. | Observable increments, prerequisites first, boundaries justified by delivery/risk/ownership; one stage is valid. | **4:** an early useful slice reduces a real dependency risk. **5:** resolves competing ownership/dependency constraints with fewer coordination steps, preserving coherent commits. |
| B3 · P1 Acceptance | **1:** would accept a result that breaks the central requirement. **2:** “tests pass” hides old-client compatibility or defers required validation beyond claimed completion. | Defines decisive success/failure and compatibility expectations; relevant tests/docs accompany the outcome. | **4:** a precise counterexample makes rejection criteria easy to assess. **5:** a compact shared acceptance example covers interacting risks without duplicating the test suite. |
| B4 · P1 Maintenance | **1:** destroys completed history or replaces the contract. **2:** helper/test edits require prose synchronization, live status is duplicated, or a public amendment leaves contradictions. | Plan owns outcomes/dependencies/acceptance; private edits leave it stable; public changes update only affected pending decisions. | **4:** ownership and references make later contract changes easy to locate. **5:** removes existing duplicate maintenance while preserving accepted history and clear delivery state. |
| B5 · P1 Review | **1:** approves an impossible sequence or invents verification. **2:** vague finding, partial-fix closure, buried verdict or stylistic blocker. | Clear correct verdict; actionable correction and revision-bound closure of the whole dependency/acceptance concern. | **4:** demonstrates the unavailable prerequisite or missing acceptance with a minimal scenario. **5:** identifies one coherent correction that resolves coupled sequencing issues without expanding the plan. |
| B6 · P1 Time/context | **1:** no usable plan after extreme avoidable replanning. **2:** reconstructs settled history, repeats policy or polishes after sufficiency; misses declared target. | Completes within the operation target, changes planning decisions only and finishes with one readability edit. | **4:** demonstrably reuses accepted decisions and checks. **5:** resolves the actual sequencing uncertainty without repeated history/context reconstruction; no speculative speed claim. |

**P2:** exact table columns, heading names, number of stages, commit-message wording and a redundant summary of the same plan. Improve presentation at the end where useful; do not require a table plus prose restating every stage. Material loss of acceptance or readability is scored above, not excused as formatting.

## Cases → rubric requirements

These existing behavioral contrasts remain useful; executable priority/anchor migration is pending. Review cases evaluate the review output, not require the reviewer to generate the plan.

| Case / input | Required judgments |
|---|---|
| `smoke-plan-maintenance`: private helper/test change | B1/B4/B6. Reuse `stable-plan`: the accepted plan stays unchanged; record time and reject unnecessary replanning. |
| `v3-maintenance` phase 02: stop-on-block becomes public behavior | B3/B4/B6. Reuse `phase-02-public-change` and `history`: amend pending work, preserve history and remove current contradictions. |
| `smoke-plan-delivery`: client A opts in; client B retains old behavior | B2/B3/B6. Reuse `delivery-contract` / `maintainable-plan`: prerequisite availability and both clients' acceptance, without unnecessary stages. |
| `smoke-plan-preview-import`: preview before mutation | B1/B2/B3. Reuse `next-outcome-consistency`, `real-delivery-dependency`: reader identifies preview as next and mutation as later. |
| `review-ready` / `review-defective`: sufficient plan versus late validation dependency | B1/B5/B6. Apply plan-specific verdict, finding and stopping judgments; add review-opening questions from this contract. |
| `plan-review-recheck`: missing prerequisite, partial ordering correction, then full fix | B5/B6. [Defined input and acceptance](evaluation.md#review-closure); preserve one finding across revisions. Existing design rechecks are a pattern to adapt, not direct plan coverage. |

Owner feedback: F1/F2/F3/F4/F5/F6/F8/F12. Existing results retain their original rubrics. [Validation](../VALIDATION.md) distinguishes scoring checks from worker runs.
