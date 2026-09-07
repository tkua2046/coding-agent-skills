# Workflow canary

Seventeen versioned synthetic cases exercise the four skill bundles against [their goals](GOALS.md). The runner creates disposable Git workspaces and preserves inputs, transcripts, produced files, Git state, checks and grading. Execution and improvement are separate questions; see [current evidence](../docs/validation/canary/INDEX.md) for actual status.

Navigation: [Goals](GOALS.md) · [Cases](cases/README.md) · [Scoring prompt](graders/review.md) · [Scoring checks](graders/calibration.json) · [Baseline](baseline/manifest.json) · [Current contract](../docs/proposals/outcome-workflow.md).

## Normal development: fast only

From the repository root, using the environment in [DEVNOTES](../DEVNOTES.md):

```sh
.venv/bin/python -m tools.canary validate
.venv/bin/python -m tools.canary affected
.venv/bin/python -m pytest
```

The commit hook includes these mechanical checks. Tests use deterministic controls and mocked model responses; their success is not a behavioral grade. Do not run all agent trials after every wording change. A new demonstrated defect needs an affected regression case.

## Before release: explicit model runs

Requires an authenticated Codex CLI supporting named permission profiles and the prepared Python runtime. No global configuration is changed. Use explicit worker/grader models, effort and per-invocation timeout; keep them the same on both sides. Replace `MODEL` and `CALIBRATION_REPORT` below with your chosen model and the actual calibration report path.

```sh
.venv/bin/python -m tools.canary calibrate --model MODEL --effort medium --timeout 900
.venv/bin/python -m tools.canary run all --model MODEL --grader-model MODEL --calibration CALIBRATION_REPORT --baseline b9087c56f2b136aff7c4b3495fffeccdfe760a28
.venv/bin/python -m tools.canary run all --model MODEL --grader-model MODEL --calibration CALIBRATION_REPORT
.venv/bin/python -m tools.canary release-gate
```

Use a case ID instead of `all` for an affected rerun. Calibration is required for the same grader, engine and environment. The baseline reconstructs the original skill files from Git; fetch the baseline commit if your clone is shallow. Ordinary candidate runs use current files, including intended uncommitted edits. The gate binds results to exact file hashes; committing unchanged bytes does not invalidate them.

`all` runs cases sequentially. Each phase and grading invocation has its own timeout; this is deliberately a release-cost suite, not a quick smoke test. Set the budget before running; there is one attempt per invocation, with no automatic retry-until-pass. After failure, record a concrete disposition and any retry rationale in a linked review/result note. Infrastructure failures remain inconclusive; preserve their reports. A corrected candidate gets a new run, never an overwritten result. The gate considers the latest retained attempt for each input/settings combination; a newer failure cannot be hidden by explicitly listing an older pass.

Every run first probes the actual OS boundary: worker project I/O must work; reading a private evaluator file and opening a network connection must fail. Worker tools can read their selected bundles and write the fixture; evaluator material stays outside. The grader receives a separate packet without the author's requested verdict or baseline/candidate label. An unavailable/failed probe stops that run. No packages or network services are required inside a fixture.

The adapter uses fresh ephemeral Codex contexts with user configuration/rules ignored. Authenticated model execution and local sandbox boundaries have been exercised in [runtime controls](../docs/validation/outcome-runtime/); case results remain separate. Runtime/tool upgrades can change behavior, so the captured environment and engine are part of evidence identity. The read boundary covers model tool access, not the host CLI's access to authentication/model services.

## Grades and retained results

- Deterministic checks cover contract oracles, original-file preservation and Git side effects. They are independent of tests the worker writes.
- The separate semantic grader records every criterion as pass/fail/inconclusive with a reason and literal evidence quotation. Twelve known outputs first check whether the scoring prompt distinguishes acceptable, defective and unavailable evidence. Examples may have their own rubric and exact expected criterion statuses; they are not answers fed into workers. A required failure cannot be offset by other scores; incomplete evidence cannot pass.
- Optional reading probes give a fresh reader only the literal first 30 lines (at most 2,000 characters) of named documents and questions. Its answer is checked against those excerpts as well as the full-document assessment. This is a machine comprehension proxy, not human acceptance.
- Conditional fix/recheck phases skip only after the declared review JSON has a valid `ready` verdict and findings array. Decisions and source reviews are retained and replayed. Missing/malformed reviews do not grant readiness; runtime and semantic checks still apply.
- Worker elapsed time, executed/skipped phases and document counts are observations, not quality scores. A fixture-user deadline may additionally be required; reader/scorer work is excluded. [Goals](GOALS.md) defines quality/benefit judgments and iteration limits.
- Immutable run directories live under `docs/validation/canary/`. Each `report.json` hashes raw inputs and outputs, includes model/effort, environment, timestamps, phase command/exit/transcript records and criteria. Available usage information remains in raw JSON events; billing and active-model-time estimates are not fabricated.
- `release-gate` validates archives, execution completion, calibration, per-criterion judgments, deterministic results and matching baseline/candidate inputs. Baseline failures remain visible; the candidate must still pass all required cases. Case/grader/engine changes invalidate affected evidence. A changed skill resource invalidates every case selecting its bundle.

The local gate is a safeguard for reviewed records, not a cryptographic attestation or GitHub publishing service. Semantic evidence still needs judgment. Fast checks, agent review, human review, remote CI and release authorization remain separate facts. Old trials keep their original grades/limitations; they are not relabeled as runs of this suite.

## Change a case or grading rule

Change its version/inputs and describe the contract reason in review; do not lower a criterion to make the candidate pass. Both baseline and candidate need compatible grading. Cases map to whole selected bundles conservatively, including templates/references. Keep evaluator-only rubrics/oracles outside worker fixtures. Update the result index with links to real records and unresolved dispositions; it is a readable entrypoint, not the gate's authority.
