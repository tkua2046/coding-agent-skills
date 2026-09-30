# Workflow behavior checks

Complete canaries and smaller operation smoke tests exercise the four skill bundles against [their goals](GOALS.md). Both use the same isolated runner and preserve inputs, transcripts, produced files, Git state, checks and grading. Execution and improvement are separate questions; see [current evidence](../docs/VALIDATION.md) for actual status.

Navigation: [Goals](GOALS.md) · [Cases](cases/README.md) · [Scoring prompt](graders/review.md) · [Scoring checks](graders/calibration.json) · [Baseline](baseline/manifest.json) · [Continuation contract](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/continuation-repair.md).

## Selected priority-scoring migration

`v1-small-feature`, `v3-maintenance` and `bounded-delivery` use `priority-v1`:
P1 scores 1–5 (3 is sufficient), explicit P0 boundaries and advisory presentation
preferences. Other cases keep their binary contracts. The existing runner,
calibration command and immutable records serve both; this is a partial migration,
not complete release calibration. See the [scope and budgets](../docs/proposals/priority-canary-pilot.md).

These cases qualify only the readiness boundary: P1 1–2 versus 3–5, with
separate P0 and missing-evidence controls. Their 4/5 distinctions are not
calibrated and cannot establish superiority. Original narrower expectations and
failed scorer attempts remain in the evidence; current outcomes are in validation.

For one selected case, first calibrate its scorer, then use the returned report:

```sh
.venv/bin/python -m tools.canary calibrate --case v1-small-feature --model gpt-5.6-sol --effort medium --timeout 300
.venv/bin/python -m tools.canary run v1-small-feature --model gpt-5.6-sol --effort medium --timeout 600 --grader-model gpt-5.6-sol --grader-effort medium --grader-timeout 300 --calibration CASE_CALIBRATION_REPORT
```

The scorer's model, effort and timeout must match its calibration. Worker calls
are capped by their remaining case/phase hard allowance; development reviews,
fixes, checks and handoff consume that allowance. Usable targets and hard stops
remain distinct. Reader/scorer overhead and whole-run elapsed time are retained
separately. Known required failures survive an incomplete later step. Authored
calibration packets test grading; they are never records of real worker behavior.

## Normal development: mechanical checks

From the repository root, using the environment in [DEVNOTES](../DEVNOTES.md):

```sh
.venv/bin/python -m tools.canary validate
.venv/bin/python -m tools.canary affected
.venv/bin/python -m pytest
```

The commit hook includes these mechanical checks. Tests use deterministic controls and mocked model responses; their success is not a behavioral grade. Do not run all agent trials after every wording change. A new demonstrated defect needs an affected regression case.

When authoring a case, provide prerequisites it calls existing (such as an API or gate), or explicitly defer them outside the requested assessment. Make preserved-file scope visible to the worker. Expected readiness must follow the supplied evidence; do not instruct the worker to approve. Diagnose a contradictory fixture separately from a skill failure, preserve the original attempt and version any correction before a fresh comparison.

## Focused prompt feedback: small LLM smoke tests

A smoke runs one real worker operation on a small realistic input, then a separate blind grader assesses the actual result. For example, the same resume task must reuse an unchanged verified fix but recognize a changed candidate whose old review is stale. These are actual skill tests; the grader's known-output calibration tests a different thing.

```sh
.venv/bin/python -m tools.canary list --tier smoke
.venv/bin/python -m tools.canary calibrate --case smoke-design-review-ready --model MODEL --effort medium --timeout 300
.venv/bin/python -m tools.canary run smoke-design-review-ready --model MODEL --grader-model MODEL --effort medium --grader-effort medium --timeout 300 --calibration CASE_CALIBRATION_REPORT
.venv/bin/python -m tools.canary run all --tier smoke --model MODEL --grader-model MODEL --calibration CALIBRATION_REPORT
```

`--case` selects that case’s complete linked control set. It checks exact current criteria, original-source copies and pass/fail contrasts for every required criterion before calling a model; missing coverage names the missing items and stops locally. A contrast is a coverage guard, not proof that the rubric is complete.

A passing `case-calibration` can support only that case with matching inputs, grader prompt, engine/settings and environment. Unrelated control edits do not invalidate it; changed relevant controls, rules, sources or grader dependencies do. Actual worker evidence also binds the selected case and skill bytes during revalidation. Use the returned report path for `CASE_CALIBRATION_REPORT`; settings must match. The two separate review cases have scoped controls; other cases may still report missing coverage.

A case calibration cannot support bulk unrelated cases or release acceptance. The existing full calibration can still support its declared complete run; diagnostic `--group` reports remain nonauthorizing. Add `--baseline REF` for the matching prior skill version. After a coherent change, select the affected responsibility and its neighbors; cover affected consumers and contrasting cases when shared contracts change. Smoke has one phase, no reader or fix loop. Its opening judgment is direct artifact review, not measured reader comprehension. It cannot replace complete canaries, and it is not automatically a release requirement. Available raw usage and worker/grader elapsed time let you assess its actual cost; shorter output alone is not a success criterion.

## Before release: explicit model runs

Requires an authenticated Codex CLI supporting named permission profiles and the prepared Python runtime. No global configuration is changed. Use explicit worker/grader models, effort and per-invocation timeout; keep them the same on both sides. Replace `MODEL` and `CALIBRATION_REPORT` below with your chosen model and the actual calibration report path.

```sh
.venv/bin/python -m tools.canary calibrate --model MODEL --effort medium --timeout 900
.venv/bin/python -m tools.canary run all --model MODEL --grader-model MODEL --calibration CALIBRATION_REPORT --baseline b9087c56f2b136aff7c4b3495fffeccdfe760a28
.venv/bin/python -m tools.canary run all --model MODEL --grader-model MODEL --calibration CALIBRATION_REPORT
.venv/bin/python -m tools.canary release-gate
```

Use a case ID instead of `all` for an affected rerun. Release evidence requires the complete calibration for the same grader, engine and environment. The baseline reconstructs the original skill files from Git; fetch the baseline commit if your clone is shallow. Ordinary candidate runs use current files, including intended uncommitted edits. The release gate binds results to exact file hashes; committing unchanged bytes does not invalidate them.

An unqualified `run all` selects complete heavy cases sequentially; `--tier smoke` explicitly selects the small tier, and `--tier all` selects both. Each worker and grading invocation has its own timeout. Choose an appropriate run scope and timeout; there is one attempt per invocation, with no automatic retry-until-pass. After failure, record a concrete disposition and any retry rationale in a linked review/result note. Infrastructure failures remain inconclusive; preserve their reports. A corrected candidate gets a new run, never an overwritten result. The release gate considers the latest retained heavy attempt for each input/settings combination; a newer failure cannot be hidden by explicitly listing an older pass.

Every run first probes the actual OS boundary: worker project I/O must work; reading a private evaluator file and opening a network connection must fail. Worker tools can read their selected bundles and write the fixture; evaluator material stays outside. The grader receives a separate packet without the author's requested verdict or baseline/candidate label. An unavailable/failed probe stops that run. No packages or network services are required inside a fixture.

The adapter uses fresh ephemeral Codex contexts with user configuration/rules ignored. Authenticated model execution and local sandbox boundaries have been exercised in [runtime controls](https://github.com/tkua2046/coding-agent-skills/tree/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/validation/outcome-runtime); case results remain separate. Runtime/tool upgrades can change behavior, so the captured environment and engine are part of evidence identity. The read boundary covers model tool access, not the host CLI's access to authentication/model services.

## Grades and retained results

- Deterministic checks cover contract oracles, original-file preservation and Git side effects. They are independent of tests the worker writes.
- The separate semantic grader records every criterion as pass/fail/inconclusive with a reason and literal evidence quotation. Known outputs first check whether the scoring prompt distinguishes acceptable, defective and unavailable evidence, including nested execution logs and direct opening assessment versus required reader evidence. Examples may have their own rubric and exact expected criterion statuses; they are not answers fed into workers. A required failure cannot be offset by other scores; incomplete evidence cannot pass.
- Optional reading probes give a fresh reader only the literal first 30 lines (at most 2,000 characters) of named documents and questions. Its answer is checked against those excerpts as well as the full-document assessment. This is a machine comprehension proxy, not human acceptance.
- Conditional fix/recheck phases skip only after the declared review JSON has a valid `ready` verdict and findings array. Decisions and source reviews are retained and replayed. Missing/malformed reviews do not grant readiness; runtime and semantic checks still apply.
- Worker elapsed time, executed/skipped phases and document counts are observations, not quality scores. A fixture-user deadline may additionally be required; reader/scorer work is excluded. [Goals](GOALS.md) defines quality/benefit judgments and iteration limits.
- Immutable run directories live under `artifacts/canary/`. Shared calibration records are referenced by relative path and checked identity rather than copied into every run. Keep the complete evidence tree together when archiving/restoring. Each `report.json` hashes raw inputs and outputs, includes model/effort, environment, timestamps, phase command/exit/transcript records and criteria. Available usage information remains in raw JSON events; billing and active-model-time estimates are not fabricated.
- `release-gate` validates archives, execution completion, calibration, per-criterion judgments, deterministic results and matching baseline/candidate inputs. Baseline failures remain visible; the candidate must still pass all required cases. Case/grader/engine changes invalidate affected evidence. A changed skill resource invalidates every case selecting its bundle.

The local gate is a safeguard for reviewed records, not a cryptographic attestation or GitHub publishing service. Semantic evidence still needs judgment. Fast checks, agent review, human review, remote CI and release authorization remain separate facts. Old trials keep their original grades/limitations; they are not relabeled as runs of this suite.

## Change a case or grading rule

Use the [operation map](CONTRACTS.md#independently-testable-operations) to select a
meaningful responsibility before choosing its case. Fixed prerequisite documents
and prior findings are inputs, not extra worker operations. The new hook/coverage
cases keep real installed-gate/application checks; retry decision cases use frozen
offline observations, with live state acquisition retained in integration coverage.
Check [current validation](../docs/VALIDATION.md) before treating a definition or
authored scoring control as a passed model test.

Change its version/inputs and describe the contract reason in review; do not lower a criterion to make the candidate pass. Both baseline and candidate need compatible grading. Cases map to whole selected bundles conservatively, including templates/references. Keep evaluator-only rubrics/oracles outside worker fixtures. Update the result index with links to real records and unresolved dispositions; it is a readable entrypoint, not the gate's authority.

The current [specification mapping](CONTRACTS.md) links each skill goal to actual
case criteria. `goals` in each rubric is traceability metadata; the scoring AI
receives the concrete requirement/pass/fail text. Known-output controls with a
`case_source` use exact current case criteria, checked against drift by fast tests.
Their expected answers remain outside the scoring packet. These controls test
scoring decisions, not execution of a skill.

Preserve the original task constraints when authoring known outputs. Supply exact
relevant requirements/baseline files instead of an unchecked shortened retelling;
`input_sources` binds those copies to fixture files in fast checks. A deliberately
different scenario must state its own contract. Preserve original interfaces and
use executable code/tests when claiming executable output, even in scoring controls.

For a focused scoring check, select a named group, for example:

```sh
.venv/bin/python -m tools.canary calibrate --group specifications-effort --model MODEL --effort medium --timeout 300
```

This writes a `calibration-sample` record with exact inputs, raw replies, judgments
and expected-status comparisons. A sample cannot authorize worker runs or satisfy
the release gate. Omit `--group` for the complete calibration. Preserve mismatches
and resolve whether the input, criterion, expected answer or scorer is defective
before a justified rerun; never change an answer solely to obtain agreement.

## Evidence delivery

Local execution records are ignored working storage. Before claiming a delivered result, publish all cited runs and dependencies to a separate immutable evidence tree and update [the index](../docs/EVIDENCE.md). Preserve failed attempts and relative calibration links. Source commits carry definitions, necessary regression fixtures and concise results, not repeated run snapshots. A restored release collection must include all attempts; the gate discovers immediate run directories in `artifacts/canary`, the legacy location, and explicitly supplied report collections. Supply each original `report.json` within its complete collection; renamed report aliases are rejected. Scratch trees and captured application reports are not release evidence.
