# One-off grading recovery: primary review requested

**Implemented for review; no real regrades executed.** The ignored executable is `artifacts/regrade_outcome.py`; its [frozen exact source](../validation/outcome-regrade/regrade_outcome.py.txt) has SHA-256 `3b2efdf5bb4693ef4e64fc8353b91a154dbf74fd620ec502a02d863bc1538d3e`. ORR01 has an author-proposed implementation; independent acceptance remains pending.

The helper supports only these two original v1 reports, pinned by their full SHA in the script:

| Source | Original report SHA prefix | Current status |
|---|---|---|
| [v1 baseline](../validation/canary/20260907T084242-fd4d0ca28f534e23a8ef73b934ce8d97/report.json) | `5ebfad94a8dfd` | Inconclusive: invalid evidence quotation |
| [v1 candidate](../validation/canary/20260907T084327-e8210bfcd7074d0581846925e88a1acf/report.json) | `c56425fd2cb18` | Inconclusive: invalid evidence quotation |

## Recovery contract

1. **Qualify without a model.** Verify the pinned report, exact evidence inventory, frozen engine/grader, copied calibration and original case/bundle/config identities. Recheck completed worker/reader executions, literal reader inputs, preservation, zero commits/tags and recorded deterministic checks. Require the original grading error to be invalid quotation and its proposed criteria to contain no semantic failure/inconclusive judgment. This narrow path does not support other cases, conditional phases, hooks or oracle replay.
2. **Reuse original evidence.** Create a unique new canonical behavior record with explicit `regrade` metadata. Copy the original report and all evidence under `source/`, including the rejected grading reply; copy original worker/reader artifacts unchanged into the canonical locations. Keep original observations and timing. Record **0 fresh worker calls, 0 fresh reader calls, at most 1 fresh grader call**. New record timestamps identify the scoring attempt, not a new worker execution.
3. **Score the identical packet once.** Reconstruct `artifacts/`, `initial/`, requests, rubric and schema from retained inputs. Preserve their hashes and the exact frozen grading prompt. Use canonical `runtime.probe` and `grade_packet`, with `gpt-6-astra / medium / 600 seconds` and the same calibration. The new grader receives neither the old rejected verdict nor an expected answer or quotation-repair instruction. No plain-text derivative log is added.
4. **Validate before publishing acceptance.** Reject packet mutation and validate quotations against immutable original bytes. `verify_regrade` checks source linkage, copied evidence, reuse counts, inherited identities/timing and helper/prompt snapshots, then calls canonical `verified_behavior`. The helper performs this on a disposable finalized preview before writing a passing/failing final record. A grading failure or interruption produces a retained inconclusive record. A semantic failure remains a failure. Existing recovery attempts prevent an implicit retry.

The canonical release gate accepts the resulting standard evidence when it passes and participates in its existing latest-result selection. The frozen gate does not interpret the extra reuse metadata; **`verify_regrade` supplies the additional lineage audit**. Consumers counting fresh executions must use `regrade.fresh_*_calls`, not recount the copied phase records. Actual new grading time is separate from reused worker time.

## Verification

- [Initial control run](../validation/outcome-regrade/controls-round1.json): **29 passed in 30.59 seconds**, using [retained no-model controls](../validation/outcome-regrade/controls-round1.py.txt). Scratch clones contain the real immutable inputs but synthetic grader responses, clearly labeled as controls. No synthetic behavior reports enter the real canary catalog.
- Positive baseline/candidate children passed both `verify_regrade` and canonical `verified_behavior`; canonical `release_gate` passed for the scratch catalog containing this one case. This is not a claim that the real repository's full release gate passes.
- Faults covered changed/missing/extra evidence, source SHA/report tampering, incomplete workers/readers, changed preservation/reader excerpts, failed deterministic or semantic results, mismatched engine/grader/calibration/config/environment, malformed/invalid new grading, timeout/interruption, modified packets, duplicate recovery, and tampered child linkage/reuse/timing.
- [Strengthened packet control](../validation/outcome-regrade/controls-round2.json) changes both a copied artifact and the grader's quote so ordinary quote validation succeeds against the altered packet; the helper must still reject it. [Final control source](../validation/outcome-regrade/controls-final.py.txt) preserves that stronger counterexample. [Actual sandbox probe](../validation/outcome-regrade/real-no-model-isolation.json) tests workspace I/O and denied private reads/network without calling a model.

The frozen engine remains `40df1bb684f719db6013129e741cce106b7176714d0b5ace9bc0a3eed80d4fe2`. No canonical runtime/tests, skills, cases, global grader or calibration were changed. Original reports remain untouched. Full model behavior and independent review are pending.

## Execution after review

Run the script once per approved source, supplying its full pinned SHA. Without `--execute`, it only validates eligibility and creates no attempt. Adding `--execute` makes one real scoring call. Invoke the two sources separately; there is no batch loop or retry mode. Keep failed children and investigate their cause before considering any new recovery scope.

## Newly observed v2 records: separate scope

The [v2 baseline](../validation/canary/20260907T084545-77792470ee6b483c847a6350fe4c3237/report.json) and [v2 candidate](../validation/canary/20260907T084628-39042d9c978f40198562574d39a34da4/report.json) show the same escaping-layer mismatch: the decoded quote contains one backslash before `n`, while the raw nested-JSON artifact contains two. Strict rejection is correct. No validator relaxation or quote rewriting is proposed.

The v2 candidate additionally proposes **failure of first-screen comprehension**; that criterion's literal evidence independently validates as a failure. Its overall report remains inconclusive because another criterion contains invalid quotations. Preserve this negative observation; it is not an all-pass worker result awaiting a formatting repair. Neither v2 report is admitted by this helper.

No recovery expansion is proposed in this increment. Changed cases, rubrics or readers require fresh standard baseline/candidate runs. A derived plain-text execution log would change the grading packet and is outside this helper. The primary review should assess necessary integrity checks versus duplicated machinery before any execution; this helper is evaluation overhead, not a reusable workflow requirement.
