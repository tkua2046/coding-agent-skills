# Independent history-preservation adjudication

**Verdict: supported V1 case-declaration defect (P2); prospective correction warranted.** The worker preserved history. The recorded run remains FAIL under its frozen declaration. No engine defect, skill regression, retroactive PASS, or completed behavioral repair follows from this review.

Reviewed the [V1 report](../validation/canary/20260907T170119-180146148713498985f8de71727f9bd3/report.json), frozen request/fixture, actual workspace, execution, deterministic results, semantic grade and restricted-reader excerpts/reply. All 190 report evidence entries match their SHA-256 values. The live V1 case directory equals the archived case directory; every fixture file also matches its initial snapshot. This is independent inspection of retained evidence, without new workers or scorers.

## HPR02 — Directory equality rejects authorized preservation

The [request](../validation/canary/20260907T170119-180146148713498985f8de71727f9bd3/inputs/case/requests/01.md) authorizes affected design/plan documents and necessary specification additions, explicitly allowing local evidence. Fixture AGENTS requires preserving original requirements and historical reviews. Neither prohibits new archives. The plan operation also calls for capturing an otherwise unavailable reviewed version once.

The supplied history directory contains only `completed.md`. Actual comparisons against frozen fixture bytes:

| Original | Final location | Result / SHA-256 of both |
|---|---|---|
| `docs/history/completed.md` | Same path | Identical, 166 bytes; `cbb47ded879d307c40042cba5142ac39737d89df92634b7c3ded346cce8ecd5e` |
| `docs/DESIGN.md` | `docs/history/design-d1.md` | Identical, 266 bytes; `0849cebc39ca291b102f8c5a502dd2f197e0b1df9ce657902ab5561e4eef1b93` |
| `docs/PLAN.md` | `docs/history/plan-before-occupied.md` | Identical, 161 bytes; `4e010bedc037fc0092a286519d02e154dca46bb786748e8255e0619e17b83426` |

The two additions are genuine archived originals, linked from the current documents. Only the supplied DESIGN and PLAN changed; no supplied file was deleted. Original requests, baseline specification, implementation and tests remain unchanged. The history failure is explained completely by the two additions, without relying on grader opinion.

All five semantic criteria pass. Independent reading confirms the document openings expose blocked-pose preservation, continuation, the set-snapshot memory tradeoff, and the next coherent increment with its dependency and decisive acceptance. Execution item_6 actually records three baseline tests and exit 0. The plan explicitly leaves occupied-cell implementation, new acceptance and requested reviews pending. No contradictory implementation or readiness claim was found.

`tools/canary.py:preserved()` correctly compares the entire directory, including additions. Its semantics should remain unchanged. The mismatch is the case's choice of `docs/history` to represent preservation of supplied history.

**Minimal prospective correction:** advance `v1-small-feature` from version 2 to 3 and replace only `docs/history` in `preserved-baseline.paths` with `docs/history/completed.md`. Keep the other guards, fixture, requests, rubric, reader, skills, engine and grader unchanged. This matches the [verified V3 precedent](outcome-final-review.md#hpr01--applied-correction-recheck): protect original files against deletion and byte changes while permitting relevant new records. Do not enumerate final worker outputs or waive individual failures after seeing results.

Before promotion, retain no-model controls for unchanged originals, relevant addition, modification and deletion of every protected history file; verify other guards still reject their corresponding violations. The present archive satisfies the proposed file boundary by direct byte comparison, but mutation controls were not run here. After the active frozen waves finish, main can version and validate the correction and decide on a fresh matched comparison. Preserve this original FAIL and separate measurement corrections from skill improvements.

## Analogous guards in the current 17 heavy cases

Inspected all 17 live `tier: heavy` case declarations and requests/fixtures for all directory guards. Eight cases have 13 directory entries; the other nine use file guards only. This is a declaration audit, not a reclassification of other run results.

| Case / directory | Assessment |
|---|---|
| V1 / `docs/history` | Demonstrated mismatch above; replace with `completed.md`. |
| V2 / `docs/history` | Same concrete contract mismatch: request 01 permits evidence and preserves completed work while both phases revise documents. Its only supplied history file is `completed.md`. Prospectively replace the directory with that literal file and increment case version 2 → 3. No observed V2 outcome is adjudicated here. |
| bounded-delivery / `docs/history` | Same mismatch: planning preserves completed work; review phases permit necessary evidence and require previous reports retained; handoff explicitly preserves history. Its sole supplied history file is `completed.md`. Prospectively replace the directory with that file and increment version 2 → 3. Keep phase ownership and other guards. |
| V5 / `docs/history` | Structurally analogous, but requests specifically write `reviews/round-1.md` and `round-2.md` while protecting candidate/original finding. No concrete need or observed authorized addition in history was established. Leave frozen; an optional later consistency change would explicitly protect `D1.md`, `D2.md`, `R1.md`, preserving all three. Do not call its results false failures on this evidence. |
| V1, V2, existing-intake, bounded-investigation / `tests` | Planning/intake/investigation preserves application tests and does not authorize feature implementation. No demonstrated authorized test-directory addition explains a false failure. Keep these guards. |
| V4 / `tests`, `data` | Design/planning only; supplied data/tests establish the baseline. Local evidence permission does not itself authorize migration of fixture data or implementation tests. No same concrete mismatch established; keep guards. |
| workflow-setup / `qa`, `examples`, `hooks` | Request explicitly retains the application suite, sample data, custom discovery and existing hook delegation, and requires temporary checks to restore the workspace. Keep these scope guards; evidence can live outside protected directories. |

V3 already protects `completed.md` and `d2-review.md` individually. No blanket conversion of directory guards is warranted.

## Missing-child-output regression contract

**A small fixed-input worker smoke is useful, separately from listing-as-test.** Current `smoke-setup-evidence` supplies an `rg --files tests` record. It does not deterministically present the later reporting hazard. In the [original candidate execution](../validation/canary/20260907T165118-dbd3ed976a8841ea825a36ed97c187aa/phases/01-operation/execution.json), completed item_6 has empty output and wrapper exit 0; its script captures/prints children without enforcing their results. RESULT nevertheless claims observed child exits 1/5 and output excerpts. I verified that retained command/result directly. The cause of missing output remains unknown.

Proposed contract: one development-setup inspection operation receives immutable historical evidence containing a completed wrapper, a supported child result, and another child's unavailable result. It produces a useful current report, retaining supported checks while leaving the missing child's exit/output and propagation unverified unless independently resolved. A later direct check can establish current behavior only; it cannot establish the missing historical observation or an unexercised wrapper/hook. Actually executed assertions establish only their enforced conditions. Fail fabricated child results, treating parent success as unchecked child success, or silently repairing the historical account. Permit focused verification or candid disclosure; prescribe neither retry counts nor a new framework.

Use a different small workflow, supplied evidence rather than simulated transport failure, one worker and the existing blind scorer. This tests reporting given incomplete evidence; it cannot reproduce the spontaneous cause or prove robustness to every live output-loss event. No behavioral smoke was launched. The separately requested draft is under ignored `artifacts/proposed-smokes/smoke-setup-child-evidence/`, for main to inspect and promote after the frozen runs.

Reviewed report SHA-256: `f29b28057a3c996e503c3a3c9c5e6096b6948f369e5e64eb26a70b739f21382b`. Archived V1 `case.json` SHA-256: `19f79cb64d24b6c1c45bf8db54847adca4036f0ef7b3cee10230716c9539eb47`.

This review changes no engine, cases, skills, grading records or running-wave documents. No model calls, behavioral reruns or full repository gate were performed; read-only byte/hash and evidence checks support the adjudication.
