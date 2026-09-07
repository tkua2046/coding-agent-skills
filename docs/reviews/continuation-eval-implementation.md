# Continuation evaluation implementation

**Ready for independent implementation review and real calibration. Engine/grader frozen.** This slice adds smoke selection, strict-citation controls and coherent intake/V6 contracts. No real LLM run, commit, push or runtime-isolation edit was performed here. Skill changes and new smoke assets belong to the other owners.

## Changed behavior

- `tools/canary.py` accepts `tier: smoke` with one executed worker operation, no reader or conditional skip. Explicit case IDs work in either tier. `run all` preserves its heavy default; `run all --tier smoke` selects smoke; `--tier all` explicitly selects both. `list --tier smoke|heavy|all` filters listing. `affected` preserves its heavy `changed_files`/`heavy_cases` fields and adds `smoke_changed_files`/`smoke_cases`.
- Release requirements remain the complete heavy catalog; every skill must still have heavy coverage. Valid smoke records do not become release requirements merely by reporting failed/incomplete execution. Record verification now precedes tier classification; the smoke case/identity must also match its retained original attempt. Corrupted evidence or a relabeled heavy report cannot hide behind the smoke tier. Existing calibration, latest-heavy-attempt and identity rules remain; no rescore or execution/evaluation identity split was added.
- The grader still requires exact source substrings. Its new instructions distinguish raw JSON text from decoded nested stdout and wrapper success from nested check success. SAR-01 is corrected: only criteria explicitly requiring an independent/restricted reader require its execution; artifact-only opening criteria are judged directly without a measured-reader claim.
- `existing-intake` case/rubric v2 accepts a supported compatibility-preservation default and asks only about real unresolved decisions. Original source, legacy Unicode failure and preservation checks remain. More questions earn no automatic credit.
- `v6-execution-handoff` case/rubric v2 and requests consistently replace exact-one-commit scoring with authorized descendant delivery plus separate proportionate-recordkeeping assessment. A retained final reply may carry the resulting commit/hash and hook outcome. Necessary original evidence remains protected; extra records need a concrete purpose.

## V6 mechanical boundary

One declarative `phase_delivery` check names the review phase, final delivery phase and relevant payload paths. The evaluator captures actual Git parent relationships and committed payload hashes outside the worker workspace. Acceptance requires baseline HEAD at every pre-acceptance phase boundary, at least one descendant delivery commit, and **every introduced commit plus the final working payload** matching the reviewed payload. Directory membership is included for tests/hooks. Replay recomputes the result from preserved phase/commit evidence rather than trusting its status label.

This is a narrow addition to the existing deterministic-check path. It neither asks the worker to construct manifests nor treats commit count as quality. A documentation/evidence follow-up can pass the mechanical boundary while failing the separate redundancy criterion. That criterion requires a demonstrated duplicate, its consequence and a simpler way to retain the same evidence.

Limits: HEAD is observed at phase boundaries, not continuously within a worker call. Payload coverage is the case's declared application/test/behavior/check paths. An auxiliary module outside those paths is not fingerprint-bound, even if an unchanged reviewed file imports it; full semantic scope review and the independent behavior oracle remain necessary. This check does not claim complete dependency-graph coverage. Git history is captured while the disposable repository exists; later replay checks retained evidence, not a newly contacted repository. Whether independent review actually accepted the candidate and whether hooks genuinely ran remain obligations of existing semantic/gate evidence, not properties established by a hash alone.

## Calibration material and provenance

The original twelve controls are retained unchanged. Seven additions use the existing calibration path:

- Two nested-execution controls project complete, unedited command-completion events from [original V6 execution](../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/01-execute/execution.json). One contains actual passing unittest/hook results; the other contains failing checks inside a successful wrapper, contradicting its supplied success claim. [Provenance](../../evals/graders/nested-output-provenance.json) records source/event/artifact hashes and the exact projection. These are archived execution excerpts, not new worker runs.
- Three authored bookkeeping countercontrols distinguish necessary original failure/review retention, demonstrably redundant recording, and a separately authorized follow-up for a new defect. The last is not extra authorization in V6 itself.
- Two authored artifact-opening controls distinguish a useful decision/consequence from process/history that buries it, without requiring a reader. Existing heavy missing-reader/inconclusive controls remain.

These 19 controls are **prepared for actual calibration, not claimed calibrated**. New grader instructions and engine bytes invalidate prior calibration normally. No old outcome or evidence archive was relabeled.

## Verification and targeted review

`python -m pytest tests/test_canary.py tests/test_continuation_eval.py -q --no-cov`: **163 passed in 44.50 seconds on the final engine**. The preceding engine passed 160 tests in 44.81 seconds; the primary's follow-up added separation of valid failed/incomplete smoke records from corrupted evidence and relabeled heavy metadata. This is mechanical evidence using disposable Git repositories and explicitly synthetic model responses. It also covers smoke selection/coverage separation, valid/absent/premature/unrelated-history delivery, changed committed or working payload, an unreviewed intermediate commit later restored, extra tests, a permissible evidence-only follow-up, proof archival/replay, escaped original-event provenance and rejection of nonliteral quotations. Ruff check and format check passed for the changed Python files. Catalog validation passed for 17 heavy plus 12 smoke cases.

The first legacy-suite attempt had 134 passes and one failed assertion that assumed every catalog entry was a heavy release requirement. That assertion now checks heavy completeness and smoke exclusion separately. An initial test-module lint failure concerned imported pytest fixtures shadowed by injected parameters; it was corrected before the passing run. Neither attempt ran an LLM or affected originals.

**CPR-01 targeted asset recheck: closed at fixture/contract level.** The primary-owned `smoke-stage-resume` and `smoke-stage-stale` have identical executor requests, maintained tests, historical reviews and reviewed hashes. The stale variant alone moves selection mutation before validation; its actual source hash differs from the historical review. Both preserve product inputs and disallow commits. Running their existing unittest gate read-only with `python -B` produced the intended pair: unchanged fixture passed; stale fixture failed with `(4, 'closed') != (4, 'open')`. The stale rubric requires mismatch detection, observed gate failure and pending correction/recheck. Actual LLM resumption behavior remains to be tested. No smoke asset was edited here.

## Frozen identities and next action

| Identity | SHA-256 |
|---|---|
| Engine | `2a888d1145e1f4cf57a9f5ae894456f8fa03ae48a644684f2739b51ffe394b59` |
| Grader bundle | `0addfd04790f86a21617ea98f32ca8b2a06c507365ae9237a7b83a331121892c` |
| Unchanged `canary_runtime.py` | `d528b02654d1cd1440d80b38dba3caae229659e31c1ea00883b965fd3a586ac2` |

Primary follow-up corrected the initial smoke-header shortcut before final freeze: verify evidence first and bind classification to the retained attempt. This changes the initially announced engine `14b11e…` to the table's current identity; the grader remains unchanged. The primary can run real calibration and then frozen-candidate smoke/heavy trials with these identities. ECR-02's implementation is ready for independent recheck; proportionality and citation reliability still need actual grading evidence. SAR-01's scoped-reader repair is ready for its paired calibration checks. No further engine/grader changes are planned in this slice.
