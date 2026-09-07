# Validation results

The repair removes raw archives from the source PR and makes workflow depth depend on the task. Scoped tests found two intake defects, now corrected in the retained outputs; one final invocation still timed out. This is a reviewed draft, **not release certification or evidence of dependable speedup**. [Original evidence](EVIDENCE.md) includes failures, inputs, outputs and independent reviews.

## What was actually tested

| Scope | Observed result | What it establishes |
|---|---|---|
| Fresh source export and documented setup | Complete hook gate passed: 250 repository tests, 94% tool coverage, 77.8 seconds | Packaging, runner, checks and offline fixtures work without restoring historical archives; coverage does not measure skill quality |
| Storage changes | Missing/changed shared calibration and report aliases are rejected; newer failed/unfinished attempts remain blocking | An older pass cannot conceal the tested newer failure paths; independent storage review verified the correction |
| Source package | 38 skill resources; raw run directories removed; original history pinned and 17 historical links verified | Reviewers can inspect maintained source separately from original evidence; retained Git history is not erased |
| Final source gate and remote PR | [Commit checks on PR #1](https://github.com/tkua2046/coding-agent-skills/pull/1) | The archived local attempt passed tests but detected a concurrent author documentation edit; its failure and disposition are preserved. Final commit hooks/CI establish the delivery check. |

## Actual agent behavior

Workers used `gpt-5.6-sol`, medium effort. Independent reviewers inspected actual artifacts, commands and required outcomes; mechanical check success was never substituted for quality. The archive contains 26 worker invocations: original paired comparisons, scoped correction checks and one implementation follow-up. Original requests/rubrics were retained; case definitions now total 17 small operations and 19 complete-task cases. Defining a case does not mean it was run on the final skills.

| Task / goal | Result and consequence |
|---|---|
| Maintain a plan after a local change; review partially fixed findings; resume with stale review; prepare a PR handoff | Both versions satisfied the four original cases. These unchanged skill bundles have direct candidate evidence. |
| Keep a PR focused while preserving required generated output | Both versions passed the new regression. Useful export data stayed; unrelated preview output was excluded from the proposed PR. No demonstrated superiority in this pair. |
| Clarify incompatible requirements | First candidate silently chose precedence: failed. A generic intake correction now leaves the consequential choice with the owner. Intermediate run passed; the final artifact also satisfies the criteria, but its invocation timed out at 300 seconds without a final reply. **Final run remains inconclusive.** |
| Preserve already settled requirements | Intermediate and final candidates passed the no-conflict neighbor. No implementation or extra approval workflow was introduced. Some optional questions still make intake longer than necessary. |
| Investigate uncertain existing code and make the next step readable | First candidate did useful experiments but buried the recommendation: failed readability. Final candidate passed, including a separate reader given only the actual opening. Supporting experiments remain accessible. |
| Complete a transcript-search feature | Both versions passed independent functional and scope review; code, tests and README were enough. This is evidence for the earlier candidate bundle, before intake-only corrections. |
| Complete a safe ZIP import feature | Both first attempts failed independent review: a damaged compressed block escaped the promised API error types; candidate CLI also printed a traceback. Existing tests had missed it. Follow-up verification is recorded separately below; original failures stay failed. |

Packet follow-up: independent recheck closed both defects after one scoped fix under the unchanged stage-development skill. The strengthened checker passes the repaired output and rejects both originals; actual partial-write, final-placement, cleanup and retry probes also pass. The skill prompt was not expanded to encode this particular bug.

## Cost and limits

Small/uncertain operation workers took about 77–300 seconds; complete features took about 299–548 seconds. The packet fix used another 242 seconds. These are individual worker times; reader/reviewer time is separate. Records retain available token usage. Shorter instructions did not consistently reduce elapsed time, and single paired observations with concurrent calls cannot establish a productivity gain.

The original transfer tasks were independently authored before seeing skill edits. However, an evaluator copy remained readable under `/tmp` during those runs. No evaluator-path access appeared in 110 audited command events; that is not proof of complete isolation. The exposed copy was removed before the fix follow-up. Treat the original transfers as independently reviewed observations, **not isolation-certified release evidence**.

No new calibrated full release suite was run. Historical passes belong to their original inputs; whole-task observations before the final intake edits are not relabeled as final-bundle results. Human usability, the user's VS Code installation and stable completion latency still need real-world acceptance. [Plan](IMPLEMENTATION_PLAN.md) owns remaining work.
