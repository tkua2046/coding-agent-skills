# Handoff measurement recheck — OGR-01 / OGR-03

**Verdict: ready-for-retest. No material finding in this measurement correction.** The revised case supplies the missing author handoff, retains the total allowance, and distinguishes stale current status from preserved history. Reviewer requests now state their actual independent role. This is approval of the bounded test contract for another run, not evidence that either skill bundle has improved.

| Finding | Disposition | What remains |
|---|---|---|
| OGR-01: missing final handoff and inconsistent scoring | **Ready-for-retest.** Author opportunity and the scoring distinction are sufficient. | Execute the supplemental scoring controls and matched baseline/candidate v2 runs; inspect original outputs. Preserve both v1 grades. |
| OGR-03: recursive reviewer identity | **Ready-for-retest.** All four reviewer requests identify the fresh context as the assigned independent reviewer. | Observe whether the detour recurs. No causal attribution to a skill change is established. |

The separately requested migration check records **HMR-01** below. Its v3 correction is now **verified-ready-for-retest**; the original finding and both v2 failures remain preserved. It does not change the handoff correction's ready-for-retest verdict.

Independent targeted review, 7 September 2026; read-only checks completed at **08:57:02 UTC**. Scope: [original findings](outcome-global-round1.md), the archived v1 case and reports, [current case](../../evals/cases/bounded-delivery/case.json), [rubric](../../evals/cases/bounded-delivery/rubric.json), requests, [handoff controls](../validation/outcome-contract/handoff-controls.json), and their existing execution/scoring path. Applied the repository instructions and stage-development review operation. Only this review file was written; no model calls, skill/product edits, engine edits, commits or release actions were performed.

## Why the correction is sufficient to retest

**Original discrepancy verified.** The [baseline report][br] retains a failed handoff grade while the [candidate report][cr] retains a passing one. Both restricted-reader inputs expose code review as pending after their latest independent code reports say ready. The candidate's plan calls this “Current”; it does not qualify the state as a historical phase-05 snapshot. Original evidence hashes verify in both archives. Their complete v1 case inputs are identical. Neither old verdict is rewritten by this recheck.

**Natural author opportunity.** [Request 09](../../evals/cases/bounded-delivery/requests/09.md) asks the author to read actual latest review/check evidence and reconcile the existing entrypoints and handoff. It allows a pending blocker to remain pending; it does not instruct the author to manufacture readiness. Earlier reports remain history behind links. Code, tests, behavior contract and independent findings/verdicts cannot be changed. A status correction alone does not trigger another code review. This addresses the actual missing opportunity without relaxing the product contract.

**Normal phase, unchanged budget.** The v1 eight phases and skip conditions are unchanged. Phase 09 is appended without a skip condition or overlay. The existing `run_case` loop therefore invokes it after the last review/recheck on an otherwise completed run, even when ready reports skip correction phases. An interrupted earlier run remains incomplete. The reader runs after phase 09 and sees the same document beginnings and questions as before. `observations` includes the new worker phase in the existing **900-second** whole-task check; it gives no extra allowance. This is the existing retrospective budget check, not a new hard interruption mechanism. Engine and global grader identities match both v1 runs exactly.

**Consistent final-state judgment.** The revised `usable-handoff` criterion requires the latest exposed entrypoints to agree with authoritative review/check evidence. A faithful reader repeating stale current text fails that obligation; explicitly historical text behind an accurate current summary is allowed. The scope criterion also checks that the final author left the reviewed code/tests and independent verdicts intact. Full phase snapshots remain available to the scorer to assess that boundary; this review does not claim a new mechanical mutation guard.

**Focused controls and hidden expectations.** The two controls share the request, latest ready review, explicitly historical phase-05 record, artifact filenames and scripted execution record. Only current status, its identical exposed excerpt and the corresponding reader answer differ. Both excerpts fit the reader's 30-line/2,000-character limit. Thus the distinction is current-state accuracy, not missing feature detail, a different review result or different historical evidence. Their local criterion equals the case's `usable-handoff` criterion byte-for-byte after JSON parsing.

I checked the controls through the existing `calibration_contract` and an **in-memory projection** of the current calibration/`grade_packet` construction. The scorer-facing content is only `request.md`, `rubric.json`, the generated response schema and `artifacts/*`. The example IDs, `expected` and `expected_criteria` are absent. Those expectations are parent-side comparison data; the complete `handoff-controls.json` stays outside the scorer packet. Scripted reader records remain explicitly labeled as controls, not actual readability trials.

The subsequently supplied one-off `artifacts/run_handoff_controls.py` is **ready to execute these controls**. Static inspection and AST parsing, without importing or executing it, confirm that it copies only request/artifacts and supplies the local rubric to the frozen `grade_packet`. Expected outcomes are compared only after scoring, outside the packet. Before scoring, the existing OS probe must demonstrate denial of reads of the actual control source and network access; failure aborts. The unique `supplemental-grader-controls` record retains inputs, exact helper bytes, isolation results and execution evidence. `grade_packet` retains strict quote validation; `require_completed` stops interrupted/incomplete calls. This record cannot qualify as global calibration or a worker result. No new API or engine change is introduced. Actual supplemental execution/isolation and score agreement remain unobserved in this review; no control score is claimed.

**Truthful reviewer identity.** Requests 02/04/06/08 each add the same two-line provenance statement; the remaining request bodies match v1. This matches `runtime.execute`, which starts a fresh ephemeral context per phase. It neither supplies a verdict nor removes review duties. The baseline archive confirms the failed nested spawn in execution stderr and the later DOC-1 disposition; these remain intact. The revised prompt removes the environment ambiguity without a global skill edit or another reviewer layer.

## HMR-01 — Migration question and mandatory answer do not align

**Priority: medium. Status: open measurement issue; do not interpret this failure as a demonstrated glanceability regression.** Additional inspection at 09:00 UTC covered the [migration baseline report][mr], archived request/rubric, exact excerpts, reader answer and full plan. Archive hashes verify. The candidate counterpart had no final report when inspected; no pairwise result is claimed.

Question 3 asks for the **next uncompleted implementation outcome, its dependency, and one decisive acceptance example**. The reader correctly identifies S1 reader/conversion without activation, its S0 review dependency, and duplicate-ID rejection. This is supported by the exposed plan and design baseline. The reader also identifies v1 preservation and copy/validate/atomic activation. Yet `first-screen-comprehension.pass_when` specifically demands **interrupted retry acceptance**, which belongs to the later S2 activation/recovery stage. The other five semantic criteria pass, including full-plan recovery dependencies.

The recorded fail follows that literal rubric; it is not an unexplained scorer deviation. The measurement asks for an example of the next outcome while requiring a particular later outcome's example. A correct answer to the posed question can therefore fail. The excerpt really does truncate S2 before its acceptance cell, so first-screen recovery-acceptance visibility is absent. That observation does not establish inability to find the asked next outcome, and the full plan explicitly covers interrupted retry. Full-document coverage does not repair a reader failure; here the claimed failure tests an additional, unasked obligation.

**Minimal correction before using this criterion for comparison:** align question and rubric. If the intended goal is next-stage comprehension, accept a supported decisive example for that stage and retain the existing full-document recovery criteria. If the intended goal additionally requires immediately visible recovery acceptance, ask that explicitly as a separate obligation and evaluate matched bundles under the revised contract. Preserve the present grade; do not retrospectively relabel it a pass or change skills to force S2 ahead of a valid S1. No case/skill modification or retest was performed here.

### HMR-01 recheck — version 3, 09:03 UTC

**Disposition: verified-ready-for-retest; no remaining finding in this minimal correction.** The author adopted the second option. Independent comparison against both archived v2 cases verifies that only `case.json` and `rubric.json` changed: both versions advance to 3, a fourth reader question is appended, and the first-screen criterion's `pass_when` changes. The original three questions, exposed documents/limits, worker request, fixture, phases, checks, other criteria, global grader, engine and selected candidate skill bytes are unchanged.

The new question explicitly asks: “What safety acceptance should be checked if migration is interrupted before activation and then retried?” The rubric now separately accepts a supported example for the next dependency-ordered outcome and requires an explanation of interrupted-retry safety. It expressly allows recovery acceptance to belong to a later stage. Thus S1 can remain reader/conversion work while S2 owns activation/recovery; the reader is now actually asked about both. Answers must still be supported by the exposed beginnings, so this correction does not turn absent recovery information into a pass.

The now-complete [candidate v2 report][mcr] also fails only `first-screen-comprehension`. Its excerpt exposes fresh-process interrupted-retry acceptance, while its answer supplies the requested S1 equivalence example. This corroborates the original question/rubric mismatch; it does not establish a v3 pass. Both original report evidence manifests verify, and both failures remain unchanged.

Next: matched baseline/candidate **worker, reader and grader** reruns under the exact v3 contract. These are measurement repairs, not skill repairs or identical-input repeats of v2. The read-only delta/identity assertions passed; this reviewer ran no models and changed only this review record. No handoff-control result, owner acceptance or overall skill improvement is claimed.

| Additional reviewed item | SHA-256 |
|---|---|
| Migration case tree v3 | `ed4cab7ba71cabddae4f5f0d7e48df28477b10cda9f55709dc09ceb5513db9b1` |
| Migration `case.json` v3 | `efe0e6ea93f612bbc1af6a6e08dbf5da5f8ffdf64e3a80abf55ad17c2fe2a0e9` |
| Migration `rubric.json` v3 | `221af8b50763324a491e934e660b872543369942f38cea34ada065e33011208d` |
| Unchanged migration worker request | `6ae01303883526e72911bf12fefd3cd8807d3e4975fc463fdbd134ac60a73519` |
| Candidate migration v2 report | `96fa744ed59de34e67774617f9d1265768872fb5f4e8e7dd494679592a31ef8d` |
| Candidate migration v2 grade | `2e01b9e5177a74ce528738d22937c039c6c580af6a9785c27667ebff2b2b2e5f` |
| Candidate migration v2 reader input | `ce830a90863e6083ba630a7f21a7d254e1e3a13e889aa66b8433d6ef91df5717` |
| Candidate migration v2 reader reply | `30e3ab597159e39f2641d14902912ba567471dac44f6f1a0a4c97f7092f28b0d` |

## Checks and exact reviewed versions

Read-only Python assertions passed: case/resource validation; v1 archive integrity; baseline/candidate case equality; unchanged fixture, oracle, prior phase definitions and budget; exact reviewer-request prefix changes; control contract/projection checks; and frozen engine/grader identity equality. No behavioral trial or scoring-model execution was run. Skill usefulness, OGR-02 workflow selection, owner acceptance and overall improvement are outside this verdict.

Tree/packet fingerprints below use the repository convention: SHA-256 of `json.dumps({relative_path: SHA256(file_bytes)}, sort_keys=True).encode()`. The case tree uses `tools.canary.files`, which excludes generated caches. Packet fingerprints describe the in-memory scorer content, not executed packets.

| Reviewed item | SHA-256 |
|---|---|
| Archived v1 case tree, both runs | `179ce250a642ce6cf96bf3b447c75271c98df02b56ded6060d6554da560da9e9` |
| Current v2 case tree | `7a6cebac220467e4fa7c3185b2a27a203a8814ee5ee8b497631a8058eaa7eb05` |
| Current `case.json` | `6b3aa465d6ec9ba40c2a10447853d98ed31784b540301a71115b32a203cf683d` |
| Current `rubric.json` | `e4934669221ecf211868ba93fb9d4985deea6ffa746ff5b59c542d025d28d366` |
| Request 02 | `fd638e1698480eb1a850be41fc60ca2c12b98ae26ce1f5dfc991946f740cd5e5` |
| Request 04 | `40632db7f74b0310921d7d91a61cbe7c71399555ff950e808d2ea8751885331f` |
| Request 06 | `6561c343240caec012f24721f643ba825529931a7c5a0e26495ae5257dddb7ac` |
| Request 08 | `5ab149b9e28ee4c8c04581750c333169901cc9c62a9fabc43ca373f2a5d69a66` |
| Request 09 | `57f1b67315a84b3fe04f5a3d9194f7f681d78e8c154df83b13523fb80ada0a95` |
| `handoff-controls.json` | `16c33d55b7ef58f9ebbeede7289fa452f47efe98a7383d98fba4e87c02ed8a10` |
| One-off `run_handoff_controls.py` | `6b7846bc64e330ecadc54cb19d1b4410f497db5bb441b359a6861f3d67a484fc` |
| Projected stale-current packet | `154d721ac2a7479a5a4a123003ab32e728edee31dc3c83cf3245b22b2092a59d` |
| Projected historical-with-current-handoff packet | `090a843a32427097f2e3df371df5c5b092f7170ae0f9dd39061e06b278fbffce` |
| Original global review | `faf3438f13a2e46e64dbbd4cd3028db353ef9e4270cb50e460247b08ab1df006` |
| Baseline v1 report | `abf9f02a3e3c7338f03bb1523334f445fb60fa5f9691e55b5d5315b39d377b78` |
| Baseline v1 grade | `9d4e950c25e1fd97e5825b1ef487444180a0255967d1a613d9f5b0e7c531b404` |
| Candidate v1 report | `a542e4eaa4a11b8d20153b35107304f829f4c67389edaf4e9f45c0bf156331be` |
| Candidate v1 grade | `ffcc202c893beb0db46e58e4430c261678d341d443443cb2f9d817c94bb0eb4f` |
| `tools/canary.py` | `67809f836022b29e0d23d580538f078907f9e4425dd1e0a2c449cf6bc4483596` |
| `tools/canary_runtime.py` | `d528b02654d1cd1440d80b38dba3caae229659e31c1ea00883b965fd3a586ac2` |
| Global `evals/graders/review.md` | `3f8c4ec60e397e6df96cd9c6921886f52a8224fd0422df5f1398a84e1864df25` |
| Frozen engine identity | `40df1bb684f719db6013129e741cce106b7176714d0b5ace9bc0a3eed80d4fe2` |
| Frozen global grader identity | `17f84dbcc760a443f99076038e60faf52daa3c000f22d2b50f2f92d963244012` |
| HMR-01 migration baseline report | `0dcb1e0cbba7155d99f6e23f3f3416980db5e661753259e247b5ee59bf3a297a` |
| HMR-01 migration grade | `8acf3804ec41bd825ebff3e68a7271efb1d74f5fab7fa77f500e4b73270748f1` |
| HMR-01 archived case tree | `91774bf506d4d9727dd6297b95a3080a1024614eb7c43c7e61589c1d3e392143` |
| HMR-01 archived rubric | `9c5ede6727fdd9e797215bda7b2b53bfb123a6508b79998c2d7a37c2186d63d1` |
| HMR-01 reader input | `9387b7ab4dc958e38f487b7e25c6ff4dd1e8a21505bd364e9f344d95206cc2f8` |
| HMR-01 reader reply | `ad1bc1a7118c40c796f29c09bc69ce58045282ecebdba871dcb64ec0510ebc59` |
| HMR-01 full plan | `f07d533237467abb06e59333cb8aa9157e2a7b3b12d7e455e6fbbaf15de6a6b5` |

[br]: ../validation/canary/20260907T083357-6a32abd825c64f7f8a395cb66f3598e8/report.json
[cr]: ../validation/canary/20260907T083526-ef8930ed28164847b88cf633a9cc20a6/report.json
[mr]: ../validation/canary/20260907T085129-a6833bc193fb46b8816096e236a818b8/report.json
[mcr]: ../validation/canary/20260907T085243-10ea4c3268af46558499da7933657b04/report.json
