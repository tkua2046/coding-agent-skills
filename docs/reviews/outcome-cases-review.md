# Outcome cases — independent evaluation review

**Verdict: needs changes. Open material findings: OCR-01, OCR-02.** Fix the inventory oracle's depletion blind spot and add a calibration discriminator for unsupported reader answers before freezing evaluation. OCR-03/04 are crucial limits on conclusions, not additional blockers.

Reviewed 7 September 2026. Scope: the main-authored assets below, including both complete new fixtures/requests, their rubrics, the inventory oracle, the v1/v2/v4 reading deltas, goals and all 12 calibration controls. The other agent's three cases, candidate skill drafts and evolving runtime were not reviewed. Prior proposal closures remain intact.

## Exact reviewed inputs

HEAD: `b9087c56f2b136aff7c4b3495fffeccdfe760a28`; the reviewed edits are uncommitted. Aggregate SHA-256 of the 43-file input map: `ab662adb14cf082acdc8d3df85ca4b02d0c336c527ad69296d66a694b01bd8a9`.

Directory/map hashes below use SHA-256 of UTF-8 `json.dumps(path_to_sha256, sort_keys=True, separators=(',', ':'))`, with repository-relative paths and lowercase file hashes. New-case trees include every source/fixture file, including dotfiles, excluding existing `__pycache__`/`.pyc` artifacts; v1/v2/v4 groups include only `case.json` and `rubric.json`. Individual-file entries are ordinary SHA-256.

| Input | SHA-256 |
|---|---|
| `evals/GOALS.md` | `0b0bc9406a8045c3b07c27bf6ef1f60a9ed0098a02597b856b7ca3b872b24e1c` |
| `evals/cases/bounded-delivery/` (26 files) | `4bd993a88c900add40d95f1bff8d62d5bb60136f5cca0a56e17aff6dac6d2126` |
| `evals/cases/bounded-investigation/` (8 files) | `a0c3d8e66bdaf85a29812fe37e385366e975d0a16721c945b4b48691cc516903` |
| `evals/cases/v1-small-feature/` (2 files) | `18d33833e4f83802cf00238ba38d920edd66caf2e95e3ae7ebd9d97ab9b63ac5` |
| `evals/cases/v2-scope-extension/` (2 files) | `53968dd5462526b2eadd0ed6d12668187cf5a93616ff06d04c971734a9caed89` |
| `evals/cases/v4-migration-risk/` (2 files) | `344466c54b9a0c7f1dec6149f9720d030fdfecede9c83d94de0ef4598c3737eb` |
| `evals/graders/review.md` | `3f8c4ec60e397e6df96cd9c6921886f52a8224fd0422df5f1398a84e1864df25` |
| `evals/graders/calibration.json` | `9404eecd98b7b621bbbec48777b8c6aa6ddbbc74e85399ad8094942acde8a343` |

## OCR-01 — P2 — Oracle accepts reservation against stale initial stock

- **Location:** `bounded-delivery/oracle.py:5–13`; SHA-256 `ca1c443e207c015015170d04636117b79c23a85a4ce55c20f4660b8d3a932f94`. The sole multi-order sequence rejects first, then accepts. The request requires: “Continue with later orders against the current remaining stock.”
- **Trigger:** An implementation preflights each order with `all(stock[sku] >= quantity for sku, quantity in order["items"])`, then debits `remaining`. It checks original availability rather than availability after successful reservations.
- **Observed consequence:** In an isolated copy, this defective implementation passed all six existing fixture tests and the complete current oracle. For stock `{"a":1}` and two successive one-unit orders, it instead returned stock `{"a":-1}` with both orders accepted. Required result: stock `{"a":0}`, first accepted, second rejected. This is an actual missed contract violation, not a speculative coverage preference; semantic inspection might catch it, but the promised independent runtime check does not.
- **Minimal correction:** Add an independently expected sequence where a successful order depletes stock, a subsequent order is rejected against that remainder, and processing continues. Exercise both APIs; retain the existing multi-item partial-debit trap.
- **Verification:** The stale-stock mutant must fail the revised oracle. A correct preflight against `remaining` must pass, including unchanged stock on rejection. The original insufficient-order implementation should continue to fail.
- **Disposition:** Open.

## OCR-02 — P2 — Readability calibration can pass without checking excerpt support

- **Location:** `evals/graders/calibration.json:104–171`, zero-based examples 6–8; compare `evals/graders/review.md:34–38`: “An answer only counts when the excerpt supports it”.
- **Trigger:** The reader confidently supplies the correct behavior/decision/next action from prior knowledge, while the exposed entrypoint contains only policy and a function inventory. The calibration's sole negative reader instead explicitly says, “It does not tell me what behavior is changing”.
- **Consequence / evidence:** A deterministic answer-only shortcut—missing answer → inconclusive, admitted inability → fail, otherwise pass—matches all three current `glance` controls without inspecting an excerpt. Swapping the positive reader answer into the negative control leaves that shortcut green although the required excerpt-support criterion must fail. Correct answers also appear in the calibration request/full-design context, so factual answer matching cannot establish that the entrypoint is usable. This is a demonstrated missing discriminator, not a claim that an actual LLM grader misgraded a run.
- **Minimal correction:** Add or substitute a negative control with a confident, factually correct answer unsupported by the retained excerpt; keep its full-document answer available to challenge source separation. Require `glance: fail`. Preserve the supported-positive and missing-answer controls.
- **Verification:** The answer-only shortcut must no longer satisfy the controls. During the separately authorized real calibration, the grader must cite the exposed text's omission and reject unsupported recovery; source-supported answers still pass and missing execution remains inconclusive.
- **Disposition:** Open.

## Crucial limitations

- **OCR-03 — Scripted execution is narrower than autonomous workflow selection.** `bounded-delivery/case.json:11–47` fixes planning, a combined document review, implementation and code review; fixes/rechecks are conditional. Requests 01/02 supply the entrypoints and combined-review operation. The pair can compare artifact usefulness, wasted fixes and elapsed work within that scaffold. It cannot establish that a skill independently chose or eliminated those phases. The 900-second ceiling also cannot by itself demonstrate relief from ten-minute reviews; retain the separate benefit judgment in `GOALS.md:29`. This limits claims, not case validity.
- **OCR-04 — Declared safeguards are not executed evidence.** Fixture requests and case metadata agree on 900/300-second allowances; goals/grader agree on restricted, excerpt-supported reading and separate evaluation overhead. No model calibration, reader isolation, phase-skip enforcement, budget enforcement or paired-runtime fairness was exercised here. The 32 declared baseline skill hashes match the pinned commit, but actual runs must still use matching case/grader/model/settings identities. Synthetic readability and investigation remain limited proxies for owner usability and production performance.

## Checks and boundaries

Static inspection covered the listed assets and reading deltas. The [main author's sanity record](../validation/outcome-assets/20260907T080838Z-dfcc057e2a2e44f2956301f5d63e2dfe.json) matches its declared current inputs and reports six inventory/two investigation baseline tests passing; those are fixture checks, not skill evidence.

Reviewer experiments used disposable copies only: original fixture oracle failed at its first rejection assertion; stale-stock mutant passed six fixture tests and the existing oracle but failed the added depletion counterexample; a correct remaining-stock control passed the oracle and counterexample. Synthetic `ready` JSON files satisfied the oracle's record preconditions solely for this control experiment; they are not reviews or approval. Calibration shortcut checks were deterministic, with no model invocation.

Only this report was written in the repository. No product edits, LLM calls, expensive canaries, commits or pushes. Recheck OCR-01/02 against revised evaluation hashes; do not infer whole-suite or implementation acceptance from this report.
