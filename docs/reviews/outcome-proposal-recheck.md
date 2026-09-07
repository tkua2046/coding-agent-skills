# Outcome proposal — round 2 targeted recheck

**OPR-01: verifiedclosed. OPR-02: verifiedclosed. Unresolved in this recheck: none.** These dispositions establish adequacy of the revised proposal contract; they do not establish implemented enforcement, behavioral improvement, or human acceptance.

Independent sidecar recheck, 7 September 2026. Scope is only the two material round-1 findings, plus one targeted consistency check of available case contracts. OPR-03/04 and remaining case implementation were not re-reviewed.

## Reviewed identity

- Proposal: `docs/proposals/outcome-workflow.md`, SHA-256 `f7b1288d1e845f69de3e86bd002d69b79237c1ca86adaab765ebca265dfd9910`; relevant additions are lines 38 and 40.
- [Round 1](outcome-proposal-review.md) remains unchanged, SHA-256 `4a8fc58947b4af2a51ec1320ceab0a2fb715175dac63496f7a3f5496c63bb929`. Its original findings and verdict remain historical.
- HEAD remains `b9087c56f2b136aff7c4b3495fffeccdfe760a28`; reviewed proposal/case edits include uncommitted content and are bound separately below.
- Case-input fingerprint: `7d9309076d2b99f7d0d540f248d150579aa98d6b4779d80a93e88b75386f8338`. This is SHA-256 of UTF-8 `json.dumps(path_to_sha256, sort_keys=True, separators=(',', ':'))`, with repository-relative paths and lowercase file SHA-256 values.
- Exact 19-file fingerprint scope: `case.json` and `rubric.json` in `evals/cases/{bounded-delivery,bounded-investigation,v1-small-feature,v2-scope-extension,v4-migration-risk}/`, plus `bounded-delivery/requests/01.md` through `08.md` and `bounded-investigation/requests/01.md` under `evals/cases/`. All 21 inputs matched before report creation.
- Final verification detected concurrent changes to `bounded-delivery/case.json` and `rubric.json`. Their inspected SHA-256 values were respectively `366f37c4a6609c29f1f21dc6685aab89f107f928a202e65125bcdcff5b68fd47` and `b455379bcf6314d5aa180c9d0fd43c3fcbe801878c21e8ba1f9d739aa0b18d9b`. The optional case check below applies only to those earlier bytes; newer versions are unreviewed. Proposal and round-1 hashes remain unchanged, so the proposal-level closures are unaffected.

## OPR-01 — verifiedclosed

**Original concern:** A passing suite could coexist with unchanged or worse developer effort without a distinct non-improvement disposition.

**Changed evidence, line 38:** “passing correctness/semantic criteria establishes candidate acceptability, not improvement.” It requires comparison for each goal and says, “Classify benefit as improved, unchanged, tradeoff, or unresolved with concrete evidence.” It also retains owner reading experience as pending and makes slower runs, lost capabilities, and risk-control regressions visible.

**Counterexample recheck:** If both candidates pass but review time, reader usefulness and document maintenance remain equal, the specified benefit decision is unchanged, not improvement. Mixed gains and added cost require an evidenced tradeoff or unresolved judgment; passing criteria alone cannot justify an overall improvement claim. The new paragraph addresses the original decision gap without inventing a universal speed threshold. The exact category names need not match round 1's suggested wording.

## OPR-02 — verifiedclosed

**Original concern:** Per-candidate limits could permit successive repairs indefinitely while postponing the final global review.

**Changed evidence, line 40:** “Permit at most two targeted skill-repair waves for demonstrated failures before a fresh global review must reconsider the task, measurement and workflow.” It adds: “The initial experiment budget is 150 model invocations; reaching it requires an explicit incomplete-results report and a revised scope decision, never a fabricated pass.” Persistent mechanisms must not accumulate more prompt rules; other reruns need a recorded cause and change.

**Counterexample recheck:** After the initial baseline/candidate waves and two targeted repair waves, a third repair cannot proceed automatically: fresh global reassessment is required first. Reaching 150 model invocations independently requires an incomplete-results report and a revised scope decision. This supplies the previously missing cumulative boundary even when each prior run individually respected its timeout. Infrastructure corrections remain recorded separately rather than being credited as skill improvement.

## One targeted case adequacy check

The inspected declarations are consistent with the two revised rules: `bounded-delivery` v1 covers planning through independent code recheck, declares a 900-second workflow allowance, and conditionally skips document/code fixes and rechecks after ready verdicts. Its required `review-convergence` criterion rejects invented blockers and repeated rewrites; `usable-handoff` requires excerpt-supported reader answers. `bounded-investigation` v1 declares 300 seconds and separates observed evidence from claims of delivered performance. The v1/v2/v4 case revisions are version 2; their required reading criteria state, “Correctness inferred from other full files does not repair a failed first-screen probe.” V4 also retains preservation and interrupted-retry meaning in the reader's answer.

These provide relevant evidence inputs and finite declared case phases. They do not replace the separate paired benefit judgment or the experiment-wide repair/invocation limits. No runner enforcement, model outputs, actual timing, or remaining cases were audited. No additional material concern against OPR-01/02 was found in this limited check.

Only this recheck report was written. No product edits, models, canaries, commits, or pushes. Continue the separately authorized case implementation and evaluation; retain these closures with the exact reviewed proposal identity.
