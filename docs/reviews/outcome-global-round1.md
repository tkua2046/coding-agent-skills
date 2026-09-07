# Global assessment: outcome-driven skills, round 1

**Decision: continue the bounded evaluation, but do not claim demonstrated overall improvement or repair skills from the delivery grade yet.** Both versions investigated sensibly, accepted adequate documents, found the same material defects, and delivered correct inventory rejection without correction loops. The apparent delivery fail→pass is not a valid benefit result: both final entrypoints retain obsolete code-review status, and the scorer treats them differently.

**Next:** correct the delivery measurement in OGR-01; keep routing benefit unresolved under OGR-02. Preserve the current attempts. No broad prompt expansion, new framework, or release is warranted by these four pairs.

Independent read-only assessment, 7 September 2026, evidence cutoff 08:48 UTC. This reviewer did not author the candidate or execute its trials. Read the repository instructions, [original requests](../sources/user-workflow.md), [goals](../../evals/GOALS.md), [proposal](../proposals/outcome-workflow.md), four skill entrypoints and relevant operations, baseline-to-candidate changes, and original artifacts from the four pairs below. Only this review file was written. This is neither owner acceptance nor a full-suite/release review.

Baseline: `b9087c56f2b136aff7c4b3495fffeccdfe760a28`. Live skill files matched the [candidate-v1 archive][bundle] at inspection. Model/effort matched: `gpt-6-astra` / `medium`; worker timeout 600 seconds. Other wave cases were not awaited or assessed here.

## Goal-by-goal benefit

“Unchanged” means no material benefit demonstrated in these observations, not proof of equivalence. Quality assessments below are this reviewer's bounded reading of evidence, separately from automated scores.

| Goal | Quality observed | Benefit versus baseline |
|---|---|---|
| FD1: understand uncertainty | Both identify repeated catalog loading, run a bounded comparison, preserve production code, and qualify synthetic timings. | **Unchanged.** Both recommend the same justified next change. |
| FD2: understandable, adequate design | Both restricted readers recover rejection and the precheck decision. Candidate puts current D2 ahead of historical D1. Local state/validation reasoning survives. | **Unchanged overall in this subset.** Better ordering is a useful local observation; reader answers add no demonstrated capability. High-consequence adequacy and human scanning remain unresolved. |
| IP1: executable next outcome | Both delivery plans use one coherent increment, concrete acceptance and existing gates. | **Unchanged.** Candidate planning prose is 414 words versus 399; neither is a function/test inventory. |
| IP2: maintainable plan | These pairs do not exercise a private rename/new-test perturbation followed by a real public-contract change. | **Unresolved.** Do not substitute initial plan length for maintenance behavior; inspect `v3-maintenance` separately. |
| SD1: correct checked delivery | Both independent behavior checks pass, both retain meaningful regression assertions, and both code reviewers run real checks. | **Unchanged.** Fewer named test methods in the candidate are not a benefit metric. |
| SD2: useful review and convergence | Both accept the ready example with the same optional header-only clarification; both defective reviews find validation, delivery dependency and buried decisions. Both deliveries execute one document and one code review, with no fixes. | **Unchanged.** Baseline's extra reviewer-identity detour is real but separately qualified in OGR-03. |
| SD3: resumable current state | Final entrypoints and final review reports disagree in both deliveries; the reader cannot reconcile a report it cannot see. | **Unresolved:** OGR-01. Candidate's pass does not establish this goal. |
| DW1: useful setup | No setup pair inspected in this assessment. | **Unresolved.** |
| DW2: truthful delivery/release | No PR/setup/release pair inspected. The two deliveries honestly leave human acceptance pending. | **Unresolved** for the full goal. |
| ALL: proportionate effort and depth | Both keep local code simple and investigation bounded. No review cycle is saved; selection is substantially supplied by the tasks. | **Unresolved** as a workflow-selection benefit: OGR-02. |

## OGR-01 — Correct the handoff opportunity and scoring standard

**Priority: high. Status: open; blocks interpreting delivery fail→pass as improvement.**

The [baseline grade][b-grade] fails `usable-handoff` because final documents still require independent review after the authoritative report closes it. The [candidate grade][c-grade] passes the same criterion for accurately distinguishing implementation from pending review. Comparing the actual excerpts exposes the inconsistency:

| Evidence | Baseline | Candidate |
|---|---|---|
| Final plan excerpt | “independent document review, independent code review and human review remain pending” | “S1 is implemented and prepared for independent code review, followed by human review.” |
| Restricted reader | Names document/code review as next, with no results exposed. | Names code review as required before human review, with no completed code-review findings exposed. |
| Latest independent code report | Ready; closes DOC-1; next action is owner review. | Ready; no findings; next action is owner review. |

Sources: [baseline excerpts][b-reader-input], [baseline answer][b-reader], [baseline final review][b-code]; [candidate excerpts][c-reader-input], [candidate answer][c-reader], [candidate final review][c-code]. These are original records, not reconstructed summaries.

Candidate's implementation handoff is valid **as a phase-05 snapshot**. Its final design/plan are not explicitly labeled “as of phase 05”; they say “Current” and “Next”, link that pre-review handoff, and do not point readers to the completed code review. Thus phase anchoring does not justify the opposite final-handoff grades. Both readers accurately report their supplied text; neither reader is the source of the contradiction. Baseline also has a document-review identity problem, but that does not remove the shared stale-code-review problem.

The [case sequence][delivery-case] ends with a reviewer restricted to review/evidence files. [Phase 05][author-request] explicitly prepares the candidate **for** another reviewer. [Phase 06][review-request] cannot update product documents; ready skips both author-fix and recheck phases. Even a correction path ends with the same read-only reviewer. No author receives the completed final review before the reader sees DESIGN/PLAN. The final-state requirement is useful, but the scaffold omits the natural opportunity to satisfy it.

**Smallest correction:** version this case and add one unconditional, bounded author handoff after the last review, before the reader. Allow reconciliation of current status and links using actual review/check evidence, including still-open findings and pending human acceptance. Prohibit feature/code/test changes and alteration of independent verdicts. Link earlier reports rather than rewrite them. A status-only update does not require another code review; charge its time to the existing whole-task allowance. This is an ordinary phase in the existing runner, not a new orchestration mechanism.

Clarify the case's handoff criterion to assess the latest state at that point consistently. Add a small scoring control distinguishing an explicitly historical phase snapshot from an unqualified stale “current” entrypoint contradicted by the latest review. Preserve both present grades and flag the discrepancy in a disposition; do not silently turn either into a pass. Re-run both frozen bundles on the revised case with compatible scoring evidence. The new pair is a measurement repair, not a skill improvement or an identical-input repeat. Keep the separately predeclared repeat attributable to its exact case version.

An alternative would be to narrow this case to **pre-code-review** handoff readability. That avoids a phase but relinquishes the final-resumption claim; it must not be reported as SD3 coverage of completed delivery. Given the user's actual goal, the short final author handoff is preferable.

## OGR-02 — The trials largely supply the workflow choice

**Priority: medium. Status: open limitation; blocks a claim that adaptive routing improved.**

The [investigation request][investigation-request] explicitly says to investigate with a bounded experiment and withhold implementation. [Review requests][ready-request] prescribe one combined review, optional preferences, static inspection, and no additional approval rounds. [Delivery planning][plan-request] requests depth selection but already names design/plan entrypoints and a subsequent reviewer/implementer; its runner fixes the roles and phase order. Both versions therefore receive much of the new policy in the task itself.

These are useful operation tests: the defective example still requires finding a real hidden contract violation, and runtime rejection is independently checked. They establish neither automatic skill discovery nor whether a neutral task would select investigation, a combined note, or deeper risk analysis. The acknowledged delivery scaffold limitation is **not user approval** of that coverage gap.

**Smallest correction:** retain the execution cases and label this limit in the result index. Before claiming routing improvement, reuse the existing local-change and uncertain-report fixtures for a small matched, planning-only probe: provide the problem and actual authorization, but omit instructions naming the desired route, number of documents or reviews. Assess whether the proposed next work resolves the actual uncertainty/consequence; do not grade a category label. Keep the existing migration case as the separate risk-retention control. No new general framework or exhaustive difficulty taxonomy is needed. If this probe is outside the remaining experiment budget, leave routing benefit unresolved rather than add more prompt rules.

## OGR-03 — Reviewer identity caused an avoidable baseline detour

**Priority: medium. Status: observed, unresolved attribution; not a demonstrated candidate defect.**

The baseline [document-review execution][b-doc-execution] explicitly calls the phase fresh, yet its reviewer attempts another reviewer context. That spawn fails. The [resulting report][b-doc] labels itself self-review and ready with a limitation. The implementer then opens DOC-1 because the plan requires independence; the final reviewer inspects the documents again and closes it. Candidate instead recognizes its fresh review context and avoids the detour. The original reports substantiate this difference; it is not merely a grader label.

However, the relevant “If asked for an independent review, use a separate agent context…” sentence is unchanged in both bundles. Added depth guidance may have influenced behavior, but one run does not establish why. Both ready/defective review pairs also use a self-review designation in already separate review phases. Do not count the baseline detour solely as a model-capability failure or proof that the new prompts fixed independence.

**Smallest correction:** make actual role provenance explicit in the reviewer task: this context is already separate from the author and is assigned to perform the review. That is a truthful environment fact, not an instruction to approve or an extra review. Preserve the failed spawn and DOC-1 dispositions. Apply equivalent context to matched evaluations if changing the case. Defer a global skill edit unless the ambiguity recurs with clear role provenance; if it does, qualify the existing sentence rather than add another review layer.

## Is the longer candidate worth keeping?

The meaningful changes are permission to use an already sufficient short note, acceptance of one coherent outcome, and selective rechecks. These remove real prerequisite ambiguity across the skill boundaries. Keeping them as a candidate is reasonable. Most “avoid overengineering” and “be concise” rules already existed in the baseline, which also performs well here. Adding another prohibition for every output difference would reproduce the user's problem.

Across all four bundles' Markdown, including optional templates, whitespace-delimited words increased **5,977 → 6,936 (16%)**; this is not a token/latency estimate. The four trials do not yet demonstrate a commensurate benefit. Current candidate delivery design/plan total **132 lines**, versus baseline **136**; planned versions were 126 versus 133. Candidate's current design precedes history and its handoff is somewhat shorter, but both still maintain separate design/plan/status prose. These are observations, not a reason to impose a line quota or remove decisive risk examples. Raw evidence files are excluded from these human-document comparisons: the baseline's 1,294 aggregate text lines are **not** 1,294 lines of user-facing documentation.

| Pair | Worker seconds: baseline → candidate | What actually changed |
|---|---:|---|
| Bounded investigation | 163.086 → 130.807 | Same recommendation and bounded evidence; somewhat different probe coverage. |
| Ready review | 60.472 → 64.740 | Same ready verdict and optional header-only wording concern. |
| Defective review | 89.385 → 71.132 | Same three material issues, each with scenario and correction. |
| Bounded delivery | 574.981 → 540.073 | Four executed phases and four skips each; correct code both; disputed final handoff measurement. |

Sources: matched [baseline wave][b-wave] and [candidate wave][c-wave], plus original [baseline investigation][b-investigation], [candidate investigation][c-investigation], [baseline ready review][b-ready], [candidate ready review][c-ready], [baseline defective review][b-defective] and [candidate defective review][c-defective]. Times include worker/service/tool waiting and exclude reader/scorer work. Parallel runs, one observation per pair, and the failed baseline spawn prevent a stable speedup conclusion. Candidate implementation itself took 237.530 seconds versus 206.161; aggregate speed hides that tradeoff.

This checkpoint supports retaining a bounded candidate for further evidence, correcting measurement first, and resisting additional general prompt rules. Maintenance, consequential migration, setup/delivery operations and owner reading experience still need their own evidence before the final skill judgment.

[bundle]: ../validation/outcome-contract/candidate-v1/manifest.json
[b-wave]: ../validation/outcome-waves/20260907T083357Z-4e7a7d0afaf24542989af3ae6d400197/request.json
[c-wave]: ../validation/outcome-waves/20260907T083526Z-539409aea63e4f76ab53e714d23e1a9f/request.json
[b-grade]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/grade.json
[c-grade]: ../validation/canary/20260907T083526-ef8930ed28164847b88cf633a9cc20a6/grade.json
[b-reader-input]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/phases/reading-probe/input.json
[c-reader-input]: ../validation/canary/20260907T083526-ef8930ed28164847b88cf633a9cc20a6/phases/reading-probe/input.json
[b-reader]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/phases/reading-probe/reply.md
[c-reader]: ../validation/canary/20260907T083526-ef8930ed28164847b88cf633a9cc20a6/phases/reading-probe/reply.md
[b-code]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/phases/06-code-review/workspace/reviews/code-current.json
[c-code]: ../validation/canary/20260907T083526-ef8930ed28164847b88cf633a9cc20a6/phases/06-code-review/workspace/reviews/code-current.json
[b-doc]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/phases/02-document-review/workspace/reviews/design-current.json
[b-doc-execution]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/phases/02-document-review/execution.json
[delivery-case]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/inputs/case/case.json
[author-request]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/inputs/case/requests/05.md
[review-request]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/inputs/case/requests/06.md
[plan-request]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/inputs/case/requests/01.md
[investigation-request]: ../validation/canary/20260907T083357-130ffc0a8e31423fbe8c8ab9ded1d958/inputs/case/requests/01.md
[ready-request]: ../validation/canary/20260907T083803-07c4c0591a634ee3afcfa02c7dd171e5/inputs/case/requests/01.md
[b-investigation]: ../validation/canary/20260907T083357-130ffc0a8e31423fbe8c8ab9ded1d958/phases/01-investigate/workspace/docs/INVESTIGATION.md
[c-investigation]: ../validation/canary/20260907T083526-78cd855023b842669e1273b62047dfbd/phases/01-investigate/workspace/docs/INVESTIGATION.md
[b-ready]: ../validation/canary/20260907T083803-07c4c0591a634ee3afcfa02c7dd171e5/phases/01-review/workspace/docs/reviews/REPORT.md
[c-ready]: ../validation/canary/20260907T083858-7af0ed6575f94a3ca1834416fa725ff0/phases/01-review/workspace/docs/reviews/REPORT.md
[b-defective]: ../validation/canary/20260907T084000-a0eb40fca76a46c2bf887c6d5c80b331/phases/01-review/workspace/docs/reviews/REPORT.md
[c-defective]: ../validation/canary/20260907T084102-34336eabfb044b8eaac1de37124972c7/phases/01-review/workspace/docs/reviews/REPORT.md
