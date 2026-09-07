# V6 delivery — bounded commit-count measurement review

**Verdict: CMR01 is open (P2, measurement mismatch). Keep the recorded FAIL.** The exact-one-Git-commit check rejects an in-scope evidence follow-up without demonstrating a second implementation stage, a bypassed gate or premature delivery. This does not establish a skill failure, nor does it authorize changing the score to pass. The measurement decision may remain pending for morning review within the hard 220-call budget.

Independent review, 7 September 2026. Scope: the original V6 instructions, two actual local commits, recorded diffs and gate executions from [candidate run 085827](../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/report.json). No models, tests, commits or corrective edits were performed; only this report was written.

## CMR01: raw commit count is stricter than the worker's delivery contract

**Location:** [case.json](../../evals/cases/v6-execution-handoff/case.json), `checks.local-commits.expected = 1`; compare [request 06](../../evals/cases/v6-execution-handoff/requests/06.md) and [rubric](../../evals/cases/v6-execution-handoff/rubric.json), `phase-06-delivery`.

The archived requests, fixture AGENTS/PLAN/DEVNOTES and scripted acceptance authorize finishing Stage 1 after review and acceptance. Request 06 also requires recording the resulting commit and actual checks. They prohibit later stages and external publication, but do not explicitly impose exactly one Git commit or prohibit a documentation follow-up. The supplied execute-stage operation likewise says to commit and record the actual commit/evidence. The evaluator-only rubric says “one local stage commit”; the deterministic check instead counts every descendant commit with `rev-list --count`, regardless of its purpose or changes.

**Trigger and consequence:** one implementation commit followed by a commit containing its resulting identity and hook output fails solely because the raw count is two. That outcome is consistent with this run's seven semantic passes, whose delivery judgment explicitly distinguishes the two commits. The semantic result does not override the deterministic result. The runner applied its existing rule correctly; the concern is whether that rule measures the intended behavior.

## What the two commits actually contain

The [phase-06 execution transcript](../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/06-accepted-delivery/execution.json) contains the staged implementation diff (`item_9`), first commit execution (`item_10`), follow-up document diff (`item_12`) and second commit execution (`item_13`). The [final Git snapshot](../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/06-accepted-delivery/git.json) retains the cumulative diff, history and empty working-tree status.

| Commit | Inspected changes | Actual gate evidence |
|---|---|---|
| `8619b4540ff1a3d1fecd2dafdac71c1c8927aa79` — Validate counter steps and accept fixture Stage 1 | Adds the two-line validation guard and meaningful invalid-input/recovery and integer regression tests. Includes usage/Unreleased updates, Stage 1 acceptance/handoff, reviews and retained evidence. Commit output reports 43 changed files, 1,763 insertions and one deletion; most of that volume is records, not application code. | Fresh unittest and full local gate each exit 0; six tests pass. The installed hook runs during commit and passes. The committed tree matches the index captured before the hook: `31a73ed4c963ce3d8c35c87b3ac3133aeb7d3f1b`. |
| `50b17a5b0e226ef7c18fbd585f6d699f6185d8f7` — Record Stage 1 commit and local validation evidence | Exactly four paths: updates `PR.md` and `stage-evidence/stage-1/record.md`; adds `completion/commit-result.json` and `completion/stage-commit.txt`. Records the first commit's identity and actual hook output and changes current status to committed. No implementation, tests, requirements, gate or version change. Output reports 78 insertions and two deletions. | Installed hook again runs normally: six tests pass, exit 0. Execution verifies that the hook leaves the staged tree unchanged, prior reports are preserved and the final working tree is clean. |

All phases before 06 still have the original baseline HEAD. The final deterministic results also pass the behavior oracle, preserved requirements/hook/version, skills/hook preservation and no-tags checks. Nonfatal sandbox cache/ignore warnings are present in the raw Git output; they do not replace or obscure the successful hook results.

Diff verification used the recorded staged/follow-up diffs, commit output and archived file bytes; the disposable repository's Git object database is not retained. Reversing the two recorded document hunks in memory reproduces their recorded Git blob prefixes (`1107313` → `da59b70` for PR.md; `1ec5a75` → `f5fd7a3` for the stage record). No artifact code was executed, and no claim is made that a new `git show` was run against the deleted repository.

## Disposition and limits

**Measurement concern supported; no automatic correction.** Requiring a record to contain its own resulting commit hash would be circular: editing the committed record changes the hash. A later local record, an external handoff, or a differently defined identity can address that need. The current request does not select one of these or make the follow-up commit a demonstrated violation.

There is real bookkeeping cost: a second commit and hook execution, plus substantial retained records across the whole case. This review does not establish that every record is necessary or that the workflow is efficient. Equally, `count == 1` cannot distinguish useful evidence preservation from excessive ceremony. Phase 06 took 182.094 worker seconds; that is the entire phase, not a measured cost attributable to the second commit. Do not infer improvement or regression from the counter alone.

For any later correction, align the worker-visible contract, semantic rubric and deterministic measure around the intended Stage 1 delivery boundary. If exactly one Git commit is itself required, specify that and a workable place to record the resulting identity. Otherwise, distinguish a completion-evidence follow-up from another implementation stage; merely loosening the count would not settle that distinction. Preserve the original failing attempt and review any prospective measurement change before matched evaluation. No new skill-prompt repair is justified by this counter failure alone.

**CMR01 remains open for that bounded measurement decision.** No rerun or new evaluation is commissioned here; additional measurement can remain explicitly pending under the 220-call cap. Current report status remains FAIL, with all seven semantic criteria PASS and only `local-commits` failing. Human acceptance of the real skills remains outside this synthetic case.

## Reviewed identities

Current V6 case files are byte-identical to the run's archived case. All 488 evidence entries in the original report match their recorded SHA-256 hashes. Hashes below are SHA-256; the case tree uses `fingerprint(hashes(files(case_dir)))`.

| Content | Hash |
|---|---|
| Case tree, version 1 | `ae37e147ca966c0a246ccfb4a5ab22eac6e636e6d574d5d448fd1dfedf1d091e` |
| Original report | `18651575ccd2188fe1872f7ccdf09fcbed6c604cffc934d6f81ff832be2c9cf7` |
| Semantic grade | `31f0d55d55140c327c14c128a010498d663fd36498b077b01b997a6437fc21d7` |
| Deterministic results | `04789f00c6a36d3b2089a6780a130e308984fa3ca7663e1ca95d48240351c3ca` |
| Phase-06 execution | `d9edce69121e8a0843b7e90676bbe86e524366ba3874d2f6a6a642e745550766` |
| Phase-06 Git snapshot | `be9cb12539ca20f82f13b7358d130671943d2aef22fe302070e52349f3197054` |
