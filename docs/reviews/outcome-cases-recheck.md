# Outcome cases — round 2 targeted recheck

**OCR-01: verifiedclosed. OCR-02: verifiedclosed. Unresolved within this recheck: none.** Closure concerns the oracle and calibration assets; it does not establish actual model grading, runtime enforcement, or skill improvement.

Independent recheck, 7 September 2026. Only OCR-01/02 were reassessed. The [original review](outcome-cases-review.md) remains unchanged, SHA-256 `fb23dc89b9e3ff166f99c6a1916d2968fd9f51191e73ffdb13587c0c3c22cee2`.

## Reviewed versions and retained evidence

- Revised `evals/cases/bounded-delivery/oracle.py`: SHA-256 `e110ade72b961f8a7ed99cb0dbaeb449000752059e0636a5fa25e959eca55fb5`.
- Revised `evals/graders/calibration.json`: SHA-256 `b7a541ca5ba0f99587ce69c6b0724495805c5ef55fc186f5a80c9ec2be8c9d2e`.
- [Round-1 contract archive](../validation/outcome-contract/case-review-round1.zip): SHA-256 `77aa62ffd3bf5b263e28e7b588519c8f34f0f596725946324a67d7a0312c82f0`, matched its manifest. The original 43 reviewed assets were individually verified inside it and reproduced the round-1 aggregate hash; the archived review matches the preserved report.
- [Raw experiment results](../validation/outcome-assets/ocr-recheck-20260907T082453Z-07c00e1d/results.json): SHA-256 `e87ed72b4203cb710ef38ca7698f40a51604bf4be42438eb336a2a37bf827895`. Records exact commands, working directories, complete oracle stdin, synthetic implementation overrides, outputs, exit codes and elapsed times.
- The same evidence directory retains [console output](../validation/outcome-assets/ocr-recheck-20260907T082453Z-07c00e1d/console.log), the reproducible control driver, captured input ZIP and [hash manifest](../validation/outcome-assets/ocr-recheck-20260907T082453Z-07c00e1d/evidence-manifest.json). Manifest SHA-256: `a16facf4c1d7d23718c878643cec1afe234be79ee8b7249e248a57568d2c4a02`. All 17 captured product inputs matched after execution.

## OCR-01 — verifiedclosed

Lines 18–21 add an accepted order exhausting `a`, a subsequent `a`/`b` order rejected without consuming `b`, and a later successful `b` order. Both `reserve` and `execute` must produce the independently specified remaining stock and `[True, False, True]` outcomes. The earlier multi-item partial-debit trap remains. Line 6 supplies `sys.path.insert(0, os.getcwd())` before importing fixture modules.

Every oracle execution used the captured oracle verbatim as stdin to the prepared Python interpreter with `-I -`, in a disposable fixture copy. No external path injection or environment override was used.

| Control | Observed result |
|---|---|
| Archived oracle + correct implementation under `-I` | Exit 1, `ModuleNotFoundError`; confirms the old import limitation |
| Revised oracle + unchanged original implementation | Exit 1, assertion at line 12 |
| Revised oracle + correct remaining-stock preflight | Exit 0; complete oracle passes |
| Revised oracle + stale-stock core mutant | Exit 1, new direct-API assertion at line 20 |
| Revised oracle + correct core / stale-stock JSON adapter | Exit 1, new JSON-API assertion at line 21 |
| Revised oracle + partial-debit mutant | Exit 1, retained assertion at line 12 |

These results close the missing depletion discriminator and verify the oracle's own isolated-Python import setup. Synthetic `ready` records only satisfy the oracle's record preconditions; they are explicitly labeled controls, not independent reviews or approval.

## OCR-02 — verifiedclosed

Zero-based example 7 now retains the uninformative excerpt and full-design answer while its reader answer exactly matches positive example 6. Its explicit expected result and `expected_criteria.glance` remain `fail`; the local rubric revision advances to 2. Supported-positive example 6 and missing-answer example 8 are unchanged.

The deterministic answer-only shortcut now predicts `[pass, pass, inconclusive]` against required `[pass, fail, inconclusive]`; it can no longer satisfy the three controls. Static inspection confirms why example 7 must fail: the excerpt supplies workflow/function inventory but none of the behavior, decision consequence or next outcome asserted by the reader. This closes the calibration discriminator gap. Real semantic calibration remains pending, not inferred from this control.

OCR-03 is retained as the primary author's acknowledged limitation; owner review remains pending. The case tests behavior within supplied orchestration, not autonomous phase selection. OCR-04 remains a limit on runtime/model claims. No other cases, skill drafts or runtime implementation were reviewed. Only this report and the new evidence directory were written; prior evidence/reviews were preserved. No LLM calls, product edits, commits or pushes.

**Attribution correction:** The original wording was “OCR-03 is retained as the user's accepted limitation”. This incorrectly attributed acceptance to the owner. The primary author acknowledged the limitation for reporting; the owner was asleep and had not reviewed it. Owner review and final human acceptance remain pending. This clerical correction changes no technical finding or evidence; no further technical recheck or tests were performed.
