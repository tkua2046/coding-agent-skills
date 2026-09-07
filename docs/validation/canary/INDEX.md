# Canary evidence

Current heavy status: **pending — no real worker/grader runs or semantic calibration for the new suite. Release is blocked.** Normal commits/PRs use fast checks.

The ten [versioned cases](../../../evals/cases/README.md), [grading controls](../../../evals/graders/calibration.json) and [runner](../../../evals/README.md) are implemented. Baseline files are pinned at `6573f8f422cb6528981ff43bc0d20c656096e7dc` before prompt edits. Historical tests retain their original status in [VALIDATION](../../VALIDATION.md); they are not substituted for the new canary.

| Check | Actual result | Original evidence |
|---|---|---|
| Current fast suite and complete pre-commit gate | 160 passed; tools coverage 90%; all hooks passed | [Final gate](../workflow-fast/20260907T062238969078Z-c1f80259861646bea0e1b6fbb97b1ae5.json), [tested/reviewed input hashes](../workflow-fast/review-inputs-v2.json) |
| Missing-heavy release check | Expected exit 1; all ten required case pairs missing | [Validate/impact/gate commands](../workflow-fast/20260907T061909572798Z-90e87b3a26734c2e9ddfd42f543b257c.json) |
| Actual OS boundary, no model | Workspace I/O allowed; private evaluator read and network denied | [Probe](../workflow-fast/20260907T061605159693Z-f7f7af94c8ae478f8997202dd4e5d3cf.json) |
| Independent implementation review | WIR-01–03 reviewer-verified closed; no open findings; 29 targeted recheck tests passed | [Finding/round record](../../reviews/workflow-implementation-review.md), [original input](../workflow-fast/review-inputs-v1.zip), [corrected input](../workflow-fast/review-inputs-v2.zip) |
| New heavy baseline/candidate suite and semantic calibration | Not run; all ten cases pending | Required before release; no behavioral grade assigned |

The 127 canary/runtime controls are included in the full count, alongside 33 checker/evidence tests. They cover preserved failures/interruptions, separate phase records, independent contract oracles, missing/forged grading evidence, stale inputs/calibration, matching passing provenance, newer failures invalidating older passes, later valid recovery and evaluation-version advancement. Mocked worker/grader output establishes runner mechanics only; neither these counts nor coverage measure skill quality.

Before implementation review, [143 tests passed](../workflow-fast/20260907T061704452642Z-f33906b3419b40c8868617adec4cecaa.json) and [hooks passed](../workflow-fast/20260907T061823166979Z-329be0c46af846bdaf856882133cab90.json), bound to [v1 inputs](../workflow-fast/fast-inputs-v1.json). Review exposed gaps despite that green result. The targeted [26-test recheck](../workflow-fast/20260907T062112717961Z-095026efae684a09982b91b25b832994.json) and final gate above retain the subsequent correction evidence. Coverage changed with the measured code; no threshold was lowered or invented.

The probe's earlier configuration and interpreter-access failures are retained as [initial](../workflow-fast/canary-isolation-initial.json), [follow-up](../workflow-fast/canary-isolation-followup.json) and [runtime correction](../workflow-fast/canary-isolation-runtime.json). The current probe above repeated the boundary successfully. This is not a complete model-invocation or cross-platform test.

Real heavy executions create a unique report directory here automatically. Preserve each attempt, including failures, and link dispositions/rechecks. Add a short case/baseline/candidate verdict table when actual runs exist; do not manufacture grades for pending cases.
