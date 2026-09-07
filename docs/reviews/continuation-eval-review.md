# Continuation evaluation review

**Verdict: ready for narrow intake/V6 contract corrections and responsibility smoke preparation; revise the mandatory rescore scope before implementation.** No skill improvement or corrected test result is established by this review.

Independent static review of Raman's [contract analysis](continuation-contract-analysis.md) and the [continuation proposal](../proposals/continuation-repair.md), checked against original intake outputs/grades, current case requests/rubrics and evaluator code. I did not review my own workflow analysis. Only this report was written; no model trials or product changes.

## ECR-01 — Defer canonical rescore and release-identity changes

Priority: P2. Location: proposal, second work row and “Rescoring boundary.”

The proposal makes supported rescoring and acceptance of old-engine executions a deliverable before establishing that fresh affected runs are insufficient. Current [identity and release validation](../../tools/canary.py) deliberately bind engine, grader, case, skills and execution evidence together. Separating execution/evaluation identity would require provenance, compatibility, latest-attempt and release-gate changes. This is appreciably larger than fixing nested quotation reliability. Changed worker-visible contracts or skills need fresh runs anyway.

**Correction:** mark canonical rescore and gate changes deferred. First repair grader citation instructions, calibrate on actual nested-output shapes, then run fresh smoke and affected baseline/candidate cases. Preserve prior inconclusive results. Revisit rescore only for a concrete compatible archive whose reuse offers enough value to justify that separate change; do not extend the earlier case-pinned helper by default.

**Verification:** new grading still uses literal source validation; changed-task comparisons use new executions; no historical result is relabeled or admitted through weakened identity checks. Original execution reuse must never be described as a current worker-runner test.

## ECR-02 — V6 acceptance must change consistently across layers

Priority: P2. Location: Raman CV-01, “Smallest correction”; current [V6 rubric](../../evals/cases/v6-execution-handoff/rubric.json), `phase-06-delivery`.

Removing `count == 1` alone leaves “makes one local stage commit” in semantic acceptance. Moving all delivery verification into prose grading also loses a clear machine-observable safeguard. The proposed proportionality rule should reject a demonstrated redundant operation, not infer excess from a second commit or a large retained failure log.

**Correction:** update request, rubric and case together. Preserve mechanically checked properties using recorded phase Git evidence: HEAD unchanged before acceptance, actual descendant delivery commit afterward, and the committed implementation matching the accepted candidate. Keep no-tags, immutable inputs, effective gates and no later-stage work. Let the retained final reply carry the resulting hash. Score recordkeeping separately, requiring a concrete duplicate, its cost and an alternative retaining the same evidence.

**Verification:** reject no commit, pre-acceptance commit and altered/unreviewed payload even with a polished handoff. Accept preservation of an otherwise unversioned prior review and genuinely new failure evidence. A separately authorized follow-up for a new finding is a positive countercontrol; it is not permission to add that work to the original fixture. Keep the six required contexts/rechecks attributed to the fixture.

## Ready scope and controls

**Intake CI-01 is supported.** The [candidate grade](../validation/canary/20260907T094757-ce99b6e7a1b7402e93107e3d2f08145a/grade.json) fails for a missing error-preservation question despite an observed-error/no-coercion preservation default. The [baseline grade](../validation/canary/20260907T090136-e9f9ff66f1594c33b202c5f1e69bbf80/grade.json) accepts that approach. Correct the criterion prospectively; do not patch the skill merely to force another question. Retain the failing Unicode baseline. Positive controls must include both a justified default and a real compatibility conflict requiring clarification; negatives must change behavior or hide uncertainty, not merely omit preferred wording.

**Minimum grader repair:** instruct the scorer to quote literal file text, without decoding nested strings first, and serialize its response so the parsed quote equals that source substring. Keep [exact validation](../../tools/canary.py) unchanged. Add known-output controls with nested quotes, literal backslashes/newlines and actual execution-output structure: real executed success must score validly; an unsupported success summary must not. A mechanically altered/missing quotation must still be rejected. Run these through the existing calibration path; passing them establishes scorer reliability on those shapes, not skill quality. No automatic quote repair, fuzzy matching or retry-until-pass.

**Smoke boundary is useful:** one real worker operation plus the existing blind calibrated scorer, immutable evidence, and a small realistic fixture. Shared artifact responsibilities may be visible to both author and reviewer; case-specific expected answers stay out of the worker context. Load the relevant responsibility/example for generation and the compact self-check afterward on demand, without another agent or generated checklist report. Freeze each smoke's input, allowed edits and outcome criteria before testing; distinguish executed worker smoke from known-output grader controls.

| Responsibility | Necessary positive countercontrol | Negative boundary |
|---|---|---|
| Design | A consequential recovery decision warrants extra detail and an explicit example. | Short opening hides that decision; long history replaces current rationale. |
| Plan | A changed delivery dependency justifies updating the plan. | Private refactor/test addition triggers a prose implementation inventory. |
| Review | Sufficient work and a completely verified fix receive closure. | Cosmetic demands block readiness, or a partial fix is closed. |
| Evidence reuse | Unchanged candidate reuses applicable results; changed behavior gets fresh checks. | Stale output becomes current success, or mandatory hooks are skipped. |

Use a transfer fixture outside the repair examples, freeze it before iterations, and avoid tuning to its wording after each result. Run adjacent responsibilities and affected complete canaries after smoke succeeds. Do not create a separate scoring framework or make every smoke a release requirement automatically. These checks isolate responsibilities; they do not measure whole-workflow productivity.

## Review state

ECR-01 and ECR-02 are open proposal corrections; no permission wait is required for the ready scope above. Recheck their concrete edits and controls before claiming closure. Continue resource-aware repair using fresh evidence; a self-imposed total-call cap is not completion.

Reviewed SHA-256: proposal `16dc07f48c1ca1bfb14f8d1323791cd89aac9e04fb0ac0d58d719abeb9560c0a`; Raman analysis `1076a5cc652557b9c0aab4a47fe8ca33cf4bfee5bb15381c9d817142a09c23df`. Later revisions need a targeted recheck.
