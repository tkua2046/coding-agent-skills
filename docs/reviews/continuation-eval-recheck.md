# Evaluation patch — independent recheck

**Verdict: ready to freeze the current engine/grader and restart calibration. ECR-01/02 are addressed within the declared boundary; ECR-03's stale-calibration risk is contained by the coordinated abort.** No functional blocker was found in the reviewed patch. This does not establish LLM grading reliability or skill quality.

Reviewed [implementation note](continuation-eval-implementation.md), actual [engine changes](../../tools/canary.py), [mechanical controls](../../tests/test_continuation_eval.py), grader instructions/calibration material, and intake/V6 request/rubric changes. Only this review was written; no product edits or LLM calls.

## ECR-03 — Running calibration identifies an older engine

Priority: P1 for using results, not a demonstrated engine defect. The implementation note freezes engine `14b11e…`; the [active calibration attempt](../validation/canary/20260907T161236-44a822ce5dee42b0ac1df6082403da99/attempt.json) records that same identity. Reviewed current engine is `2a888d…`. Existing `check_calibration` correctly rejects that mismatch, so the older run cannot qualify current smoke/heavy execution.

**Action:** coordinate the actual freeze, update its recorded identity, and obtain matching calibration before relying on current behavioral results. Preserve the older attempt; do not relabel it or weaken identity validation. This mismatch was reported immediately during review. I did not stop any process or change the engine. Closure needs a calibration record bound to the reviewed frozen engine/grader/environment/settings.

**Coordinated disposition:** the primary confirmed that the earlier calibration was aborted and its original report retained, and now solely coordinates mutations. The latest `2a888d…` engine is exactly the version independently reviewed and mechanically tested below. The stale result is no longer being proposed as current evidence; ECR-03 does not block implementation-review completion. A matching new calibration remains the ordinary next validation step, not another requested engine change or review round.

## Accepted corrections

- **ECR-01:** no canonical rescore, execution/evaluation identity split or relaxed historical acceptance was added. Literal quotation validation remains strict. Nested-output controls preserve complete original command events; the failed-check control distinguishes successful wrapper exit from failed inner checks. Artifact-only opening judgments no longer require a reader, while explicitly restricted-reader criteria still do.
- **ECR-02:** V6's request, rubric and deterministic check consistently replace raw commit count. Captured phase HEADs reject sampled premature delivery; actual parent relationships require descendant delivery. Every introduced commit and final working payload must match the reviewed payload. An evidence follow-up may pass this mechanical boundary while its redundant purpose fails the separate proportionality criterion. Necessary unique evidence and separately authorized new work have positive countercontrols.
- **Intake:** supported preservation defaults satisfy compatibility without another question; silently changing outputs/errors, concealing the Unicode failure or inventing the customization interface still fails. This corrects measurement, not a retrospectively established skill improvement.
- **Smoke:** one actual worker phase, no conditional skip or reader; explicit IDs work across tiers and bulk execution remains heavy by default. Heavy coverage/release requirements remain intact. Valid failed/incomplete smoke attempts do not become release requirements; changed evidence or a heavy report relabeled as smoke is rejected.

## Verification and limits

I ran `.venv/bin/python -m pytest tests/test_continuation_eval.py -q --no-cov`: **28 passed in 8.19 seconds**. This focused rerun was justified by the new smoke/provenance boundary. Controls cover premature/absent/unrelated-history delivery, unreviewed committed/working content, an intermediate bad commit later restored, added tests, legitimate evidence follow-up and proof replay. Model/sandbox calls are replaced or forbidden in these tests. Static comparison confirmed the original twelve calibration controls are unchanged; catalog validation found 17 heavy and 12 smoke cases.

The payload is deliberately limited to declared application/test/behavior/check paths; unrelated new work still needs semantic scope review. HEAD sampling cannot detect a temporary commit/reset entirely within one worker call. Payload hashes establish content equality, not independent approval, fixture-user acceptance or actual hook execution. Later replay evaluates retained runner evidence, not Git objects freshly read from the deleted fixture. These are disclosed limits, not claims of complete event auditing.

Reviewed engine: `2a888d1145e1f4cf57a9f5ae894456f8fa03ae48a644684f2739b51ffe394b59`.
Grader: `0addfd04790f86a21617ea98f32ca8b2a06c507365ae9237a7b83a331121892c`.
Test file SHA-256: `7f5f2f97d0a704ed21fb4b6ea474bfba74145c5f1385ea8b3935e10129225b24`.

No additional engine architecture or unrelated review round is requested. Freeze these reviewed identities and proceed with coordinated actual calibration and frozen-candidate trials. Future mutation requires explicit coordination; this review changes no product files.
