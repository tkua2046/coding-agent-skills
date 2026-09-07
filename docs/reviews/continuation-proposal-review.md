# Continuation proposal — independent review

**Verdict: ready to implement the direct repairs; the smoke matrix needs one targeted coverage correction, CPR-01, before it is accepted as complete.** Defer canonical rescoring and release-gate identity changes to a separate coherent patch; they are not prerequisites for correcting prompts or obtaining new behavioral evidence. This is design review, not confirmation that the proposed repairs work.

Reviewed on 7 September 2026:

- [Continuation proposal](../proposals/continuation-repair.md), SHA-256 `16dc07f48c1ca1bfb14f8d1323791cd89aac9e04fb0ac0d58d719abeb9560c0a`.
- [Leibniz's workflow analysis](continuation-workflow-analysis.md), SHA-256 `0ef66d208f50240451a6419a3aa16ee4f28c319ba085f45a0975487d81778855`.
- [Smoke contracts](../proposals/smoke-contracts.md), SHA-256 `414114a20e3d36fd5dcae5d2fac183d063bed53463214124136a4009500d72fd`, added to this review after the initial two-document inspection.

Read their proposed replacements against current artifact templates, document ownership, review operations, the scoring prompt and its exact-substring validator. Prior inspection of the cited V6/intake originals informs this review. No fresh model execution, product edits or automatic test results are claimed. Only this review file was written.

## Artifact responsibilities are sound

The four responsibilities identify different decisions, rather than four mandatory documents or agents. A combined design/plan can satisfy both. Flexible examples and silent author checks are appropriate; author self-checks do not establish independent review or human acceptance.

| Responsibility | Accepted interpretation / implementation boundary |
|---|---|
| Design | Explain behavior relevant to the choice, its reason, consequence and example. Original specs/confirmed clarifications remain authoritative; do not create a competing full behavior specification. Decision status belongs here; constantly changing delivery status belongs elsewhere. |
| Plan | Own stage outcomes, dependencies, boundaries and acceptance evidence. A boundary may need its own reason; excluding duplicated design rationale must not remove that delivery decision. A private rename or extra test should not require a parallel prose inventory update. |
| Review | Own revision, verdict, actionable findings and verified dispositions. Share the substantive artifact contract with the author; preserve the separate obligation to inspect actual evidence. A sufficient artifact can receive a short ready verdict. |
| Delivery | Maintain one authoritative current state and link original evidence. A PR may summarize validation and limitations for its identified revision; that is a useful delivery snapshot, not a second continuously synchronized status database. |

Keep contracts within independently usable skill bundles and existing operation/resources where practical. “Load only the relevant contract” concerns instructional resources, not permission to omit original requirements, relevant code or evidence. No contract registry, routing service, extra mandatory report or recursive self-review loop is needed. Fix an issue found by a silent check; expose an unresolved material decision, not the checklist itself.

## Workflow replacements address observed causes

Leibniz's five replacements are proportionate: consolidate live status, identify the relevant candidate, reuse verified dispositions, reuse applicable checks, and lead with the decision/outcome. They respond to actual duplicated status and verification work; the analysis correctly labels causal attribution as a hypothesis and does not blame skills for fixture-required phases.

Preserve these boundaries in implementation and paired smoke tests:

- **Reuse requires applicability.** Unchanged relevant code, requirements and check configuration support reuse only while relevant inputs/runtime conditions and freshness requirements remain applicable. For example, a changed migration input or runtime can invalidate an old check without a code edit. Check this scope; do not replace it with a whole-workspace inventory. Required final gates and explicitly requested independent rechecks still run.
- **Resolved means verified on the relevant content.** An unchanged reviewer-verified finding can be cited. An author's “fixed” label, changed behavior or partial-invariant check cannot be treated that way. Keep the partial-fix negative case.
- **Preserve once, then link.** Capturing an otherwise unavailable uncommitted reviewed version is justified. Repeated manifests of records and a second commit solely to record the first hash are not made useful by the word “evidence.” Preserve original failures while correcting future behavior.
- **Useful openings remain substantive.** Lead with the current decision, consequences and next outcome. Test whether the reader can apply these, including failure/recovery, rather than rewarding headings, keywords or a document squeezed under the reader's character limit. Keep full-design adequacy and an unseen transfer scenario.

These are boundaries of the proposed replacements, not requests for new subsystems or review stages. Ordinary project conventions and explicit task instructions continue to take precedence.

## Smoke matrix: one missing executor countercase

The matrix is otherwise suitable: actual operations produce artifacts, the unchanged runner preserves evidence, a blind grader judges consequences, and heavy cases retain independent reader coverage. The intake conflict and plan-maintenance neighbors vary the decision that should change behavior. The design transfer exercises recovery beyond the CSV example. Smoke readability remains grader assessment, not measured reader comprehension. Keep transfer task details/expected answers out of repair examples; a failed transfer is retained, and once used to tune a prompt it is no longer held out.

**CPR-01 — P2, Stage resumption row.** Its positive exercises the executor, but its named negative is a partial-fix *review* operation. A reviewer can correctly leave a defect open while an executor still blindly reuses an old ready verdict. Those two behaviors can coexist, so passing the review countercase does not establish safe resumption after content changes.

**Minimal correction / retest:** pair the existing resumption input with a copy whose relevant implementation has changed after its ready review, keeping the old review and checked identity intact. Run the same real resumption operation. It must detect that mismatch, check the affected invariant and preserve any required pending recheck/acceptance; it must not claim the old evidence covers the changed candidate. The unchanged positive must still reuse applicable evidence and avoid redundant verification machinery. Reuse fixture/assets; no new runner, multi-phase scenario or broad matrix is needed. Keep human-acceptance handling explicit in the stage fixture; a reviewer verdict alone cannot grant it. Close CPR-01 after reviewing the concrete paired assets, then record the actual runs separately.

Do not resolve this by adding the desired verdict to the worker prompt. Likewise, the CSV design scorer should accept any contract-compliant choice with a correct invalid-tail consequence, rather than force “validate everything”; the intake conflict must exist in requirements, rather than merely asking more questions to satisfy a rubric. These preserve the proposed anti-overfit boundary.

## Minimal grader correction is sufficient to try first

Keep [the validator](../../tools/canary.py) strict. Clarify [the grader instruction](../../evals/graders/review.md): understand nested output as needed, but copy evidence from the cited file's raw text. JSON-encode that literal substring when returning the grade. After decoding the grade once, `quote` must be an exact substring of the source file; do not first unescape nested stdout, normalize newlines or repair a quotation in the validator.

Required controls before relying on the changed scorer:

| Control | Required result |
|---|---|
| Actual archived nested execution output with a genuinely completed successful check | A real blind grader returns a semantically supported grade whose escaped quote passes the existing literal validator. Preserve its original reply and execution. |
| Same realistic nesting with an actual failed/non-executed check and an unsupported author success claim | A real blind grader identifies the contradiction with a valid literal quote. It must not pass merely because “success” appears in the author's text. |
| Quote mutated to decoded newlines, altered result text or a nonliteral excerpt | The existing mechanical validator rejects it. This control verifies exactness; it does not substitute for either real grader run. |

Use archived shapes and preserved failures, not a simplified string-only demonstration. Do not weaken semantic obligations to improve a pass rate. Intake and V6 contract changes need their own goal-based rationale and compatible tests; quote repair provides no justification for changing their acceptance.

## Ready implementation scope and deferred work

Proceed with the replacement instructions/templates, the minimal grader instruction/control repair, and a small smoke selection using the existing isolation/evidence path: one real worker operation and one blind calibrated grader per case. Preserve original requests, outputs, identities and available usage/time. Paired cases should distinguish justified defaults from real ambiguity, sufficient work from material defects, and verified closure from a partial fix. Add focused ownership/check-reuse coverage and transfer; do not construct a broad new matrix before learning from these runs. Then run affected complete canaries with frozen candidates and independently inspect results.

**Canonical rescore is useful but separable.** The proposal's second work row and rescoring section require compatibility/lineage and release-gate semantics beyond the direct repairs. Fresh execution can supply current evidence now; retaining old inconclusive reports does not block that path. Mark rescore deferred for this patch and leave the existing gate unchanged. A later rescore patch must distinguish reused execution from a newly tested worker engine and cannot retroactively relabel originals. This deferral narrows implementation architecture, not the obligation to continue repairing demonstrated behavioral failures.

Next action: include the CPR-01 pair while implementing this scope, verify the positive/negative controls and fresh smoke results, then choose affected full trials from the actual changes. No human approval, runtime correctness, overall speedup or release readiness is established by this review.
