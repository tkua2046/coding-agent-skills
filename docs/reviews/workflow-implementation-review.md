# Workflow implementation review

**Current verdict: ready for the targeted v2 recheck. Open IDs: none.**
WIR-01, WIR-02 and WIR-03 are reviewer-verified closed against **frozen review-inputs-v2**. Next action: complete the executor's final fast gate and existing delivery process; heavy worker/grader acceptance remains pending until release. See the appended recheck for evidence and limits.

## Original v1 review (retained)

**Verdict: needs changes. Open IDs: WIR-01, WIR-02, WIR-03.**
Next action: correct the retained-failure path, permit evaluation revisions, and align the positive calibration control with its required rubric; obtain targeted recheck. Heavy worker/grader runs remain deferred until release.

Independent, single-pass implementation review, 2026-09-06 America/Los_Angeles. Reviewed version: **frozen review-inputs-v1**, against baseline `6573f8f422cb6528981ff43bc0d20c656096e7dc`. Authority: repository AGENTS, stage-development review operation, original workflow requirements and approved workflow proposal/validation contract. This is the first implementation review of this increment; these finding IDs are new and all remain open, with no author-fix or verified-closure claims.

## Binding inputs

[Source archive](../validation/workflow-fast/review-inputs-v1.zip), SHA-256 `b87350759d13bf38e070a8022d0ad658e16b30571fe5352d9da5f959a5ac3307`; [manifest](../validation/workflow-fast/review-inputs-v1.json), SHA-256 `6946afb18e92d26c5d811ff4c4ac456ee8c7b946b7cbebd436a500b6bbe4ec43`. All 201 entries verified; checkout matched at start and completion. Reviewed product bytes came from the extracted archive. Locations below refer to that version even if the checkout subsequently changes.

Scope: runner/runtime, release evidence validation, ten cases and calibration, narrow skill/template changes, and fast/heavy cadence. Inspected the skill/config/checker delta against baseline. Tests were copied separately into the disposable review directory; they are not part of the source archive.

## Material findings

### WIR-01 — P1: an early failed attempt permanently blocks subsequent valid evidence

**Location:** `tools/canary.py:549–557`, `340–351`, `746–754`.

**Trigger/reproduction:** Start with the tests' synthetic comparable baseline/candidate control and a passing gate. Call `run_case(root, case_id, worker, grader, missing_calibration_path)`, then rerun with the valid calibration. The failed invocation returns an inconclusive report with `evidence: {}`. The later run passes, but `release_gate` still returns fail with `Missing run provenance/evidence` for the retained earlier report. Reproduced using the frozen runner and labeled synthetic runtime; no model calls.

**Consequence:** A mistyped, failed or stale calibration input fails before any evidence is saved. Every subsequent gate scans that report and treats it as a global integrity error, even after successful correction. Recovery requires removing/altering historical evidence or changing the runner, contradicting the promised preserve-failure-and-rerun workflow.

**Minimal correction:** Persist a verifiable attempt/input/error record before calibration validation can fail. Admit well-formed incomplete attempts into normal identity/latest-attempt selection without making them acceptable behavior evidence. Preserve integrity rejection for corrupted records.

**Recheck:** A latest incomplete attempt must block an older pass; a later valid matching run must recover while retaining the failed report unchanged. Cover missing, nonpassing and stale calibration inputs.

### WIR-02 — P2: documented evaluation version bumps cannot be used

**Location:** `tools/canary.py:100`, `126`; `evals/README.md:49`.

**Trigger/reproduction:** In an otherwise valid disposable catalog, change only `case.json` version from 1 to 2: `cases(root)` raises `Duplicate/unsupported case`. Restore it and change only `rubric.json` version to 2: `Invalid rubric`. Both failures reproduced. Existing catalog tests actually require rejection of case version 2.

**Consequence:** Following the documented version-bump procedure prevents validation, execution and release gating. Routine regression-contract revisions would require editing runner code or retaining a misleading version 1.

**Minimal correction:** Separate supported data-schema versions from case/rubric content revisions, or accept positive integer content revisions while validating the existing structure. Retain exact input hashing for freshness.

**Recheck:** Version-2 case/rubric assets validate and participate in execution/gating; invalid revision values fail; version-1 evidence cannot satisfy changed version-2 identities.

### WIR-03 — P2: the positive planning calibration has an unsupported required anchor

**Location:** `evals/graders/calibration.json:27–30`, `37–45`.

**Trigger/static reproduction:** Apply the shared required `evidence-boundaries` pass condition to example 0, whose expected result is pass. It demands identification of inspected content by revision and exact excerpt. The supplied `docs/PLAN.md` identifies its proposed P2 plan and honestly leaves execution/reviews pending, but provides no identified source-inspection excerpt. Unlike the other three criteria, this condition does not distinguish planning from review. The review positives do supply explicit reviewed revisions and excerpts.

**Consequence:** A grader applying the literal required condition can withhold pass on the designated positive control. Calibration then rejects that grader before any behavior trial. The mismatch is in the declared control/anchor, not an observed model failure.

**Minimal correction:** Give planning an explicit evidence-boundary anchor appropriate to proposed acceptance and pending execution; retain revision/excerpt binding for review. Alternatively supply the missing inspection evidence if it is intended to be a planning requirement. Do not weaken the full-invariant or honesty requirements.

**Recheck:** Statically map every required criterion to evidence for each positive control. The negatives must still fail for dropped YAML scope and false D2 closure/runtime/human claims; transport loss must remain inconclusive. Actual semantic calibration stays release-only.

## Checks and limits

- Extracted-source `python -m tools.canary validate`: ten cases valid, exit 0.
- In the disposable copy, `.venv/bin/python -m pytest -o addopts='' -p no:cacheprovider tests/test_canary.py tests/test_canary_runtime.py -q`: **110 passed in 19.85s**. These cover synthetic passing provenance and stale/missing/inconclusive rejection, calibration revalidation, retained phase failures, grading evidence and contract oracles. They do not prove that real model-produced passes are accepted.
- Independent deterministic reproductions confirmed WIR-01 and WIR-02. No product corrections were applied.
- Actual `runtime.probe` in a fresh temporary workspace: exit 0; workspace I/O permitted, private-file read and network connection denied. Python 3.12.4, codex-cli 0.153.4, macOS. This establishes the observed probe boundary, not the complete worker/grader invocation.
- Static inspection found no additional material blocker in requirement/history preservation, removal of table/card duplication, proportional migration risk, full-invariant recheck, or the distinction between author-fixed and reviewer-verified. Normal hooks remain fast; current canary documentation explicitly leaves heavy acceptance pending.

Executed test-copy SHA-256: `test_canary.py` = `4575cc4f2fe85fb09aab877c73665a9ba32a8d53f7eafa09849543b28220c5fc`; `test_canary_runtime.py` = `74e8066599a2662e721721aabf3859716e7d590cc8cdbac193479d09a148956f`.

Executor separately reports 143 fast tests passing in 29.72s in [its record](../validation/workflow-fast/20260907T061704452642Z-f33906b3419b40c8868617adec4cecaa.json), with [its input manifest](../validation/workflow-fast/fast-inputs-v1.json). That broader result was not independently rerun or audited here. No full hook/manual suite, real LLM execution, semantic calibration, release approval or semantic-effectiveness claim. Only this report was written in the repository; all experiments used disposable copies. No commit.

## Targeted v2 recheck — 2026-09-06 America/Los_Angeles

**Verdict: ready within WIR-01–03 scope. Open IDs: none.** Independent recheck of the author's claimed corrections; no broader review or research reopened. The original concerns, verdict and v1 evidence above remain historical.

Binding [v2 source/test archive](../validation/workflow-fast/review-inputs-v2.zip), SHA-256 `2a582e5c7912b43dddae1039dfbd1f4e1471ab985b11b8241e7de632c147692c`; [v2 manifest](../validation/workflow-fast/review-inputs-v2.json), SHA-256 `e0ad6a32d37cad6c65342fe56e372dd090e7c6672c71f59a6a2996cdc9fa336d`. All 209 entries verified against the archive and checkout at start and completion. Checks used the extracted archive, including its tests. Among files present in v1, only `tools/canary.py` and `evals/graders/calibration.json` changed; both deltas were inspected.

### Verified dispositions

- **WIR-01 — reviewer verified closed.** `tools/canary.py:464` and `557–560` save `attempt.json` before calibration input parsing/validation can fail. The behavior attempt records identity, settings, environment and requested calibration, so an early failure has hash-verifiable evidence. The unchanged latest-attempt selection admits that inconclusive record and withholds acceptance. Executed missing/nonpassing/stale calibration regressions each verified: early failure retained and verifiable → old green blocked → subsequent valid run passes → every byte of the failed directory remains unchanged. The failed-calibration test also confirms no worker call occurs after calibration rejection. This resolves the reproduced v1 failure without relaxing evidence-integrity checks.
- **WIR-02 — reviewer verified closed.** `tools/canary.py:29–30`, `104`, `134` accept positive integer content revisions independently of report schema version. Executed case and rubric revision-2 regressions each verified catalog acceptance, rejection of old v1 evidence, and gate acceptance after comparable fresh baseline/candidate runs. Twelve invalid-revision controls reject zero, negative, boolean, string, fractional and null values across both assets. Input hashing still invalidates changed revisions.
- **WIR-03 — reviewer verified closed at static contract level.** Calibration rubric revision 2 makes the planning evidence anchor specific to a proposed revision and truthful pending acceptance, retaining exact reviewed revision/excerpt requirements for reviews. All six examples, including requests, artifacts and expected outcomes, are identical to v1. The following independent mapping checks every required criterion for the three positives; it is not an executed semantic-calibration result.

### Calibration evidence mapping (zero-based example indices)

| Positive / artifact | `scope-history` | `decisions-next-action` | `verification-closure` | `evidence-boundaries` |
|---|---|---|---|---|
| 0: `docs/PLAN.md`, supplied original requests/history | Retains movement, YAML/200,000 cells and historical S0. | Explains set build/memory and lookup costs, full validation before movement, open duplicate/value policies and dependency order. | Proposed acceptance includes invalid input, unchanged full pose with False, later R, original turns and unknown commands. Implementation remains pending. | Names proposed P2; explicitly separates proposed acceptance from executed tests and states no independent review or human acceptance occurred. No inspection excerpt is now demanded of this planning output. |
| 2: `reviews/round-1.md`, D2 and R1 | Retains R1/D2 and reviews the supplied D2 correction. | Gives the concrete `(2,3,1)` → `(3,3,1)` defect and requests preservation of both coordinates plus heading. | Keeps R1 open despite unchanged heading; requires the full pose, False and continuation at recheck. | Names D2 and quotes its actual transition; limits verification to document content, with no runtime tests and human acceptance pending. |
| 4: `reviews/round-2.md`, retained round 1, D3 and R1 | Preserves failed D2 round and original R1; distinguishes historical D2 from current D3. | Verifies x=2, y=3, heading=1 and False, then directs runtime implementation/checks. | Quotes D3's unchanged-pose and continuation clauses and closes the entire original invariant, retaining failed-round evidence. | Identifies D3 with exact excerpts; explicitly limits closure to static verification and leaves runtime checks/human acceptance pending. |

**Remaining controls:** Example 1 still fails scope/history, consequential decisions and planned verification because it explicitly discards the authorized YAML/scale work and omits its validation. Truthful pending status cannot offset those required failures. Example 3 still fails full-invariant decisions/closure and evidence boundaries: it accepts D2 on heading alone and invents runtime/human approval. The embedded grader override remains untrusted artifact text. Example 5 explicitly reports transport loss of current D3 and the final report; retained D2 history cannot establish the missing current review. Its expected inconclusive remains consistent with the grader's missing-evidence rule, rather than being converted to a product failure or pass.

### Actual checks and limits

In the disposable v2 extraction, using the existing repository Python environment:

```text
.venv/bin/python -B -m pytest -o addopts='' -p no:cacheprovider tests/test_canary.py -k 'calibration or revision or newer_incomplete_attempt' -q
29 passed, 80 deselected in 12.50s
```

Inspected the selected tests' assertions and runtime substitutes; these are labeled synthetic controls with real model/sandbox calls forbidden. The subset also retains calibration-identity/control revalidation and timeout/interruption rejection. Archive/delta verification and the six-example mapping were static checks. No additional product/test files were edited, no full suite or OS probe was repeated, and no actual model/calibration run occurred. The executor's concurrent complete hook gate is outside this recheck's evidence. Readiness here closes the three implementation findings; it does not establish semantic effectiveness, human acceptance, or release approval. Only this review report was updated; no commit.
