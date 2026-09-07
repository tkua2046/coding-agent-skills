# Outcome runtime independent code review

**Frozen runtime diff: ready. ORR01: open operational recovery gap.** The later v1 results expose a missing grading-only recovery path, documented below. Their rejection is correct; both cases remain inconclusive. No engine change is requested during the active waves. Human approval remains pending. This is a runtime code-review verdict, not acceptance of the skills or permission to release.

## Reviewed scope

Independent review on 2026-09-07 of the working-tree diff against `b9087c56f2b136aff7c4b3495fffeccdfe760a28`, restricted to the four files below. Read repository AGENTS, DEVNOTES and the stage-development review operation. No runtime, test, case or raw evidence files were changed; no behavior runs were launched.

Frozen engine identity, verified before and after review: `40df1bb684f719db6013129e741cce106b7176714d0b5ace9bc0a3eed80d4fe2`.

| Reviewed file | SHA-256 |
|---|---|
| [canary.py](../../tools/canary.py) | `67809f836022b29e0d23d580538f078907f9e4425dd1e0a2c449cf6bc4483596` |
| [canary_runtime.py](../../tools/canary_runtime.py) | `d528b02654d1cd1440d80b38dba3caae229659e31c1ea00883b965fd3a586ac2` |
| [test_canary.py](../../tests/test_canary.py) | `97a765ab63d3493435e20557147b231200bbf7582a4e5e96aec16c41c8789dad` |
| [test_canary_runtime.py](../../tests/test_canary_runtime.py) | `fc60dc1af2fbad1fd72b29f9f9f7676cec01a77169b59950436e6370632a9c0a` |

## Verification and consequences

- **Provenance and comparison:** independently replayed the [12-control calibration](../validation/canary/20260907T082604-813e3ca009e44d6cbd680a50b29f49a7/report.json), including its exact per-criterion expectations. Engine, grader, settings and environment matched. The completed baseline/candidate pairs for bounded investigation, bounded delivery and both document-review cases replayed successfully, preserving the baseline delivery failure. Explicitly recomputed the investigation and delivery pairs' input identities against the declared baseline Git ref or current candidate bytes; all matched. Settings were `gpt-6-astra / medium / 600 seconds` for both worker and grader.
- **Skip semantics:** missing, malformed, duplicated-key and non-ready reviews do not skip. Replay checks the exact previous review bytes, zero execution, absent reply and unchanged workspace/Git snapshot. A ready verdict only skips the specified phase; the final rubric and deterministic checks still determine the case result. The author/reviewer distinction remains a behavioral requirement, not an approval established merely by a JSON verdict.
- **Reader and oracle boundaries:** the reader receives only literal first-30-line, 2,000-character excerpts and questions in a separate workspace; replay recomputes those excerpts from the retained worker documents. Actual reader records include successful private-read/network denial probes and the disabled ambient-context settings. Oracle source remains evaluator-owned and executes after the worker within the restricted workspace. This review does not independently validate every case's oracle or rubric.
- **Failure handling:** calibration stops after an incomplete control and retains its execution. Reader/worker incompletion cannot establish acceptance. The retained incomplete v1 baseline report also failed acceptance replay because grading was absent. Targeted regression controls confirm a newer finalized failed/incomplete attempt blocks an older green result for matching inputs and settings.

Targeted automated checks used the following command, with coverage output and persistent pytest caching disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -o addopts='' -p no:cacheprovider tests/test_canary.py tests/test_canary_runtime.py -k 'ready_skips or nonready or reader or per_example or deadline or incomplete_calibration or copied_calibration or newer_ or stale_inputs or changed_evidence or recomputes_archived or commands_use or apple_git or capture or promote_partial or grading_and_replay'
```

Observed result: **55 passed, 99 deselected in 16.97 seconds**. These are runtime regression controls, not measurements of skill quality.

Two additional scratch subprocess controls exercised the real `capture` implementation: a one-second timeout and SIGINT to the isolated test parent. Both retained `started-control\n`, returned exit `-9`, and correctly distinguished `timed_out` from `interrupted` (1.009 and 0.571 seconds respectively). No LLM was called. Hard-kill/crash recovery was not tested.

Verified every listed hash in the retained [frozen-engine Git/privacy control](../validation/outcome-runtime/20260907T082202-git-fixed/manifest.json) and [earlier authenticated CLI smoke control](../validation/outcome-runtime/20260907T080930-smoke-fd55b56c/manifest.json). The latter is historical adapter evidence; the current-engine calibration and reader executions provide the current real-model evidence.

## Initial disposition, retained

Open ORR findings: **none**. No correction or refactor requested. Full release-gate acceptance, ongoing behavior runs, grading quality and human usability approval remain outside this bounded runtime review.

## Addendum: ORR01 — grading-only recovery absent

**P2 operational design gap; open recommendation, not a newly introduced false-pass defect.** Location: [grade_packet](../../tools/canary.py#L479), [run_case grading/finalization](../../tools/canary.py#L884), and [CLI operations](../../tools/canary.py#L1146). The available behavior operation repeats worker phases; there is no supported recovery operation for an otherwise intact run whose grader produced an invalid evidence quote.

The [v1 baseline](../validation/canary/20260907T084242-fd4d0ca28f534e23a8ef73b934ce8d97/report.json) and [v1 candidate](../validation/canary/20260907T084327-e8210bfcd7074d0581846925e88a1acf/report.json) both retained completed worker, reader and grader executions, but `scope-and-evidence` quoted test output at a different JSON-escaping layer from the literal `execution.json` artifact. Exact-quote rejection correctly made each result inconclusive. The grader proposed passing criteria; those proposals are not validated skill passes.

Independently verified both evidence manifests, original case/bundle identities, completed worker/reader replies, reader inputs and copied calibration. These archives suffice to reconstruct the original grader packet. Repeating the author task would consume additional time and replace the measured behavior merely to repair scoring; editing the original quote/report would lose the original failed attempt.

**Smallest evidence-safe recovery to consider after review:** one bounded, fresh grading call per affected immutable worker packet, with the same prompt, rubric, model settings and matching calibration. Reconstruct from retained inputs, requests, initial state and phase artifacts; do not give the new grader the rejected verdict or a desired answer. Preserve the original reports unchanged. Record a separate child grading attempt with the parent report hash, packet hashes, exact invocation and raw response. Recheck literal evidence against the original artifact bytes. Retain worker timing and record extra grading time separately.

Do not normalize escaping, silently repair quotes, retry semantic failures until green, or present an ad hoc regrade as an original engine execution. A successful child result needs an explicit, reviewed derivation check in the acceptance path before it can resolve the parent grading failure; until then it is supplemental evidence and the cases remain inconclusive. Verify that path with valid-parent recovery, changed-packet rejection, interrupted regrade and newer-invalid-child controls. No code, raw evidence or grading calls were changed or added in this review.
