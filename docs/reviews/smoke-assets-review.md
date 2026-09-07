# Smoke assets — independent static review

**Verdict: needs one scoring correction, SAR-01 (P2). The twelve smoke assets otherwise fit the proposed responsibilities; CPR-01 is closed for asset validity.** This is a static review with deterministic fixture sanity checks, **not an actual LLM smoke result** or candidate-skill acceptance.

Reviewed all `evals/cases/smoke-*/` requests, fixtures, rubrics and declared mechanical checks against [smoke contracts](../proposals/smoke-contracts.md) and [continuation repair](../proposals/continuation-repair.md). Inspected the runner's preservation, worker-input and grader-packet paths for their bearing on these assets. Only this report was written; no product changes, model calls, commits or pushes.

**SAR-01 — P2: make smoke opening assessment distinct from required reader execution.** [Shared grader](../../evals/graders/review.md), lines 34–38, requires the restricted reader's actual text/answers for first-screen criteria and says missing reader execution is inconclusive. Both [local design criterion `decision-entry`](../../evals/cases/smoke-design-local/rubric.json) and [transfer criterion `usable-recovery-design`](../../evals/cases/smoke-transfer-design/rubric.json), lines 5–9, judge the opening. However, their smoke cases intentionally have no reader; [runner validation](../../tools/canary.py) rejects a smoke `reading_probe`. The grader packet supplies requests, initial files, phase artifacts and rubric without the case's tier/probe declaration or the smoke proposal's explicit exemption.

A substantive, usable design can therefore receive an inconclusive judgment for evidence this tier deliberately never produces. Whether the grader interprets these as “first-screen” criteria is left implicit. This is an inconsistent scoring contract, not an observed model failure.

Minimal correction: explicitly select direct artifact-based opening assessment for smoke in evaluator-visible instructions/context, and apply the mandatory-reader rule only to cases that require a reader. Retain substantive recovery/invalid-tail assessment and the heavy tier's missing-reader rejection. Do not add a smoke reader or weaken adequacy. Verification should distinguish a usable smoke opening without reader evidence from a heavy case missing its required reader, while still rejecting an opening that omits the consequential behavior. Preserve old identities/results; evaluate the corrected scoring version separately.

**CPR-01 — concrete pair verified.** [Resume request](../../evals/cases/smoke-stage-resume/requests/01.md) and [stale request](../../evals/cases/smoke-stage-stale/requests/01.md) are byte-identical. Their fixtures differ only in `session.py`; original reviews, requirements, tests, gate and initial handoff are identical. Both requests require applicability comparison and the remaining gate without disclosing which verdict to return.

- Positive `session.py` matches R2's `bfe24c031dc02cb821fc710ee9e7fbcf45fa562677728c35a40c8e9ef45d682a`.
- Both test files match R2's `38e1190859b65dc80a0b05642e76af6dba2345bff1eec88211b8b75a9bc2e0e6`.
- Stale `session.py` is `7654b1339a08de19e1c8ccf999d7cc6b8bd44fc3e4ec05937d65df5cd071f7e6`, while its R2 correctly retains the positive hash.
- The same unittest gate passes the positive and fails the stale candidate: invalid `jump` leaves `(4, "closed")` instead of `(4, "open")`. Pending correction/recheck and human acceptance are explicit. Historical R2 is supplied fixture evidence, not a claim of fresh independent review.

**Other contract checks.** All twelve cases declare one executed phase, no reader or conditional loop, and produce an actual note, amendment, review or handoff. The combined D1/P1 review is one coherent review operation. Intake preservation and Unicode conflict form a meaningful pair; design requires the stated invalid-tail consequence rather than a preferred implementation; rollout planning distinguishes real client dependencies from private maintenance; reviews distinguish sufficient work from a partial invariant fix. Setup and PR transfer require actual current execution despite misleading or outdated prior evidence.

No keyword, heading, length, test-count or architectural quota was found. The zero-commit/no-tags checks enforce explicit scope. Preservation lists protect individual supplied files and leave assigned design amendments, new notes/reviews/PR draft and the current handoff writable. In particular, stale-stage code preservation is legitimate because the paired request explicitly authorizes assessment only. The maintenance plan stays immutable because the supplied private change alters none of its decisions. New evidence files are not forbidden by directory-equality checks.

Case-specific rubrics/expected outcomes remain outside worker fixtures; the inspected runner copies only fixtures and selected skills into the worker, then supplies the phase request. Worker-visible requirements, tests and historical reviews are legitimate task evidence. The owner states both transfer cases were authored before candidate completion and not shared with the skill writer; this review records that provenance without claiming an independent chronology/access audit. Keep their details out of repair examples; tuning from a transfer result ends its held-out status.

**Sanity evidence.** Python 3.12.4, bytecode writes disabled. `tools.canary validate` passed all 29 catalog cases without models. Running `-m unittest discover -s tests -v` with the local Python interpreter produced one passing test each for resume/setup and one expected failing test each for stale/PR transfer. The latter returned `"x"` instead of `"  x  "`. Direct fixture calls confirmed `label("ß") == "SS"`, `label(None)` raises `AttributeError`, and the partial-review candidate preserves cursor but changes selection. These establish fixture behavior only; no grader calibration, isolation probe, full workflow or skill improvement is claimed.

**Reviewed identities.** Workspace HEAD `d76bb80fa15a01e8240a9c328a0bac485b95564b`; all cases and rubrics are version 1. Cases/proposals/grader prompt remained unchanged between 2026-09-07T15:53:45.264047+00:00 and 2026-09-07T16:07:45.159579+00:00. Concurrent runner edits changed its SHA-256 from `ba1d9d77979c90787008fc00d14fb414888d4d2f8e033e64485781c5a94b1400` to `50d6c8f9713f43695c6a37490317786a7ea9cd6f811c2c4cbb27f534e3bb59c7`; the final relevant reader/packet/preservation paths were re-inspected. No frozen skill candidate was evaluated.

| Case | Runner-compatible case fingerprint |
| --- | --- |
| smoke-design-local | `5583aef33f5b491d1c80a10aaf50ce178884f917b842e25ac43697a188186124` |
| smoke-intake-conflict | `9fdbe056c1ced933ebab6a51cad0da2f98b5971be84c5f46da304e3bceb1e215` |
| smoke-intake-preserve | `decd24cfb3a2a5d5477911640aa49ba75304ebc37adef9a968a499e82b473ace` |
| smoke-plan-delivery | `f4b5328f5f8556f1e2b71b06f60ac8b09402103d2d29746fef392b90ce255649` |
| smoke-plan-maintenance | `dd687b7a42a4fd7740350615f9f9693dffa348c2eb59d017c4be944a755eaeeb` |
| smoke-review-partial | `ffdab5a88bfb6579c56083e1fe7a0808db28f8bde5c153be5676adabf6643460` |
| smoke-review-ready | `5222ec2777a388d3fc9eac2c3426f27e67f5c8071617ca3610b7784c4a08d46a` |
| smoke-setup-evidence | `3850132ecdf23d12cb5f48030eaacddc378b8a394d5e57e86a541b4a5afe864e` |
| smoke-stage-resume | `8a239218edf78a48596a18ff27e7ce4445c2b11fee8a801eeb2640be8b8cf858` |
| smoke-stage-stale | `a672556b153967adb984dd34db0711f7736f8237a6d5925b9a6698238775643a` |
| smoke-transfer-design | `d64e5593acc8bec45b1cf5df171b2870e6a05150a1c34406294b73fa6427ea84` |
| smoke-transfer-pr | `d64416aa718af6d01d4f7223ccb6ea65fdddb12b1e49c2db8981b8ca5908e82d` |

Fingerprints use `fingerprint(hashes(files(case_directory)))`: SHA-256 of Python's sorted-key JSON map of relative file paths to byte SHA-256 values, as implemented by the runner.

| Supporting input | SHA-256 |
| --- | --- |
| smoke-contracts.md | `9b72e77438d688e5f07a621f29e4d66f93c3cbc1592e3dcb66dd231f3c6649d6` |
| continuation-repair.md | `4a06529280376ea8df47be652b9f10e11ad5248f809c069e4354ff9dd75d573a` |
| evals/graders/review.md | `2ace548a60a785a04669acc5afaecd8db882d44b75cd3ee483384f682d48633b` |

## SAR-01 recheck — 7 September 2026

**Disposition: closed at the static scoring-contract/control level; ready for actual calibration.** This append-only disposition supersedes the original SAR-01 open verdict for the identities below. It does not claim a model calibration pass, smoke result or candidate-skill acceptance.

Narrowly inspected [shared grader](../../evals/graders/review.md), lines 34–42, the two direct-opening controls and the preserved reader controls in [calibration.json](../../evals/graders/calibration.json), against the minimum correction and [implementation note](continuation-eval-implementation.md). No full case/runner re-review or execution was performed.

The shared instruction now applies mandatory reader evidence only to criteria explicitly requiring an independent/restricted reader. Missing required reader execution remains inconclusive. Artifact-only opening criteria instead assess the document directly and expressly prohibit inventing a reader run or claiming measured comprehension. The criterion supplies the distinction; the correction needs no new reader or case-schema field.

The new `artifact-opening-useful` and `artifact-opening-buried` controls share the same request, rubric and later detail. Only the opening changes: the positive exposes validation-before-activation, preserved active settings, cost and a concrete rejection example; the negative displaces those decisions behind process/history. Expected `artifact-opening` statuses are respectively pass and fail, with no reader artifacts. Identical useful later detail prevents accepting the negative merely because the full artifact contains the answer. These are meaningful authored scoring controls, not executed worker evidence or keyword/length quotas.

Read-only JSON comparison with HEAD `d76bb80fa15a01e8240a9c328a0bac485b95564b` confirmed all original twelve control objects and the shared default rubric unchanged; the current total is nineteen. The preserved independent-reader controls still expect pass for supported reading, fail for an answer unsupported by the exposed entrypoint, and inconclusive when the answer was not captured. This verifies the expected contracts, not whether the running grader meets them.

Source identities verified at `2026-09-07T16:13:02.323322+00:00`:

| Source | SHA-256 / runner identity |
| --- | --- |
| Grader bundle, matching the implementation freeze | `0addfd04790f86a21617ea98f32ca8b2a06c507365ae9237a7b83a331121892c` |
| evals/graders/review.md | `48a9fbb598331d44d2e6751d609d858c7b377647c95b017d7b3c59c58540b6f1` |
| evals/graders/calibration.json | `bf951447181a3953a5dedff755f6c1c904e8c08ccc71deac1a6966dbee7b39de` |
| docs/reviews/continuation-eval-implementation.md | `01f4983cd867b3033d8699089d8157c0e0b168bdfa4476abe26cfa085eb37de0` |

Actual calibration results remain for the primary to collect and assess. Only this review disposition was appended; original findings/identities remain intact. No product edits, model calls, commits or pushes.
