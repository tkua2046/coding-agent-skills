# Workflow setup — targeted scoring-boundary recheck

**Verdict: ready for retest. OSR02's measurement correction is reviewer-verified; no material finding remains in this scoped review.** Run a fresh baseline/candidate pair with workflow-setup version 2 and matched settings. The original version-1 results remain inconclusive; this review does not rescore them or establish skill quality.

Reviewed independently on 7 September 2026. Scope: the archived-to-current case diff, actual scorer packet boundary, and conjunction of semantic and independent checks. No broader grader framework, skill review or full-suite assessment was performed.

## What was verified

All 17 case files were compared against both original runs' `inputs/case/` snapshots. Only `case.json` and `rubric.json` differ. The complete change is the two version increments (1 → 2) and `effective-existing-gate.pass_when`: it now assigns worker-evidence assessment to the scorer and independent oracle acceptance to the runner. Requests, fixture, oracle, phase order, selected skill, checks, required flags, failure conditions and all other rubric criteria are byte-identical.

The correction matches the actual [runner source](../../tools/canary.py): `run_case` writes `deterministic.json` separately, then constructs the scorer packet from phase artifacts, initial files and requests (lines 873–899). `grade_packet` adds the rubric (lines 479–494). The evaluator's oracle source and deterministic result are not copied into that packet. The unchanged [scoring instructions](../../evals/graders/review.md) require actual, attributable artifact evidence and distinguish mechanical checks from semantic judgments.

Neither obligation is waived:

- The corrected semantic criterion still requires real worker execution showing suite success, failing-test rejection, empty-discovery rejection and restoration. A hook file or unsupported claim remains insufficient. `validate_grade` also continues to require literal artifact evidence for pass/fail judgments (lines 330–363).
- `installed-gate-contract` still executes the unchanged evaluator oracle. Final acceptance joins semantic status with **every** deterministic status: any failure fails, otherwise any inconclusive result blocks a pass (lines 900–912). The archived-result verification path preserves that conjunction and checks the expected deterministic IDs (lines 1002–1034).

The current runner, runtime and shared scoring prompt also match the [initial-wave source archive](../validation/outcome-contract/initial-wave-inputs/inputs.zip) byte-for-byte. This is a case-local measurement correction, not a runtime or shared-grader change.

## Original evidence and OSR02 disposition

| Retained version-1 run | Observed result | Disposition |
|---|---|---|
| [Baseline report](../validation/canary/20260907T085907-3cb838e09ec448fd9dc50289753193b4/report.json) | All six deterministic checks pass. Semantic `effective-existing-gate` is inconclusive solely because the rubric requires an evaluator-oracle result absent from the packet; the other four semantic criteria pass. | Preserve as inconclusive under the original rubric. The old scorer correctly identified its missing input; it did not establish worker failure. |
| [Candidate v1 report](../validation/canary/20260907T085908-9ab1d583aa654b1083fb9f6efeae5f6e/report.json) | All six deterministic checks pass. Grader timed out after 600.019 seconds, with no completed semantic judgment. | Preserve as inconclusive. The timeout is distinct from OSR02 and supplies no semantic verdict. |

Both archived oracle executions exited 0 without timeout; all ten internal probes passed, including documentation-only staging against a known failing baseline and workspace restoration. These are retained observations, not newly executed tests. SHA-256 verification matched all 216 baseline and 188 candidate evidence entries recorded in their reports.

**OSR02: ready-for-retest.** The contradictory scoring obligation is corrected without changing task scope or removing acceptance checks. A fresh matched pair can now assess version 2; no outcome is presumed. No new generic conditions are proposed.

## Exact reviewed identity

All hashes below are SHA-256. The case tree uses the runner's `fingerprint(hashes(files(case_dir)))` convention.

| Content | Hash |
|---|---|
| Current case tree, version 2 | `b9318ee7a4b0a57b108e191b96d9340ad269512073977ff9a5f66fde842c401f` |
| Archived case tree, version 1 | `b6fcdb87e7c39e8f3a3b9c122699ecdcd2601ad6e63361774b9dbdc8269d2e6d` |
| Current `case.json` | `bd38139f412c7fb7f8213a64704c51974a9b8dfd72f4f8a43dc9950f5955fe21` |
| Current `rubric.json` | `45ffacd80a604807c69f4dcacc495b195122d2bb515d1cf51d5b6cd603bfb3b0` |
| Unchanged oracle | `42127aa172895c51f3f9d28079449c85528c120530ca67a769adecb5ead08a9e` |
| `tools/canary.py` | `67809f836022b29e0d23d580538f078907f9e4425dd1e0a2c449cf6bc4483596` |
| `tools/canary_runtime.py` | `d528b02654d1cd1440d80b38dba3caae229659e31c1ea00883b965fd3a586ac2` |
| Shared scoring prompt | `3f8c4ec60e397e6df96cd9c6921886f52a8224fd0422df5f1398a84e1864df25` |
| Baseline report | `552c35f49a66b3a49fa3f970021beb3606defff959a94203bae5f3ae36fdeddf` |
| Candidate v1 report | `6c2496255aae5d69119f080d4d2c47ee1b735ac5bf8b7a4ebd2b3a3fb7ed70ce` |

Checks performed: targeted source inspection, exact file/JSON diff, archive comparison and evidence-hash verification. No models, oracle reruns or test suites were run. Only this review report was written; runtime, cases, skills and existing evidence were not edited. Human acceptance and subsequent behavioral results remain outside this verdict.
