# Small behavioral checks

Purpose: cheaply detect a broken responsibility or interaction before rerunning a complete workflow. Each row produces an actual artifact/action in a fresh isolated workspace, followed by blind scoring. This is not a quiz about what the skill says. Cases use small slices of credible maintenance work; only the evaluated operation is shortened.

| Responsibility | Scenario and observable outcome | Countercase / adjacent regression |
|---|---|---|
| Intake | Existing text-label API adds an optional prefix; preserve old exceptions and defaults from inspected code without asking the owner to reconfirm them | A second request conflicts with existing Unicode behavior; identify that actual decision rather than silently selecting a behavior |
| Design | Extend an existing CSV exporter with a row limit; explain full validation vs early stopping and its invalid-tail consequence before preserved history | Transfer: revise a small configuration importer with interrupted activation risk; concise output must retain recoverability |
| Plan | Turn an agreed compatibility transition into independently useful delivery boundaries and acceptance | A private rename/new regression in a completed plan needs no rewritten stages or test inventory |
| Review | Review a sufficient small batch design without manufacturing process blockers | Recheck a partial state-preservation fix; keep the actual unresolved invariant open with a reproducible counterexample |
| Stage resumption | Resume a reviewer-verified fix on unchanged content; retain original review, run remaining required gate and give an accurate handoff | Run the same resumption operation with code changed after the recorded ready review: identify stale evidence and the actual regression, preserve pending correction/recheck and human acceptance |
| Development setup | Inspect existing tooling and a command log that listed tests without running them; execute the real check and document current evidence | A false green baseline and unnecessary tool migration fail even if a later command passes |

Initial suite: ten focused cases in the rows above, including the executor countercase added for independent finding CPR-01. A separate configuration-design transfer and PR evidence transfer are held out from the repair examples, then run on the frozen candidate. Exact names and counts are not product goals.

Use the existing runner with `tier: smoke`; one worker phase, no separate reader, no workflow fix/review loop. One calibrated grader inspects the result, including actual execution when relevant. Readability smoke scores whether the document leads with the useful decision; heavy cases retain the independent restricted-reader test. Preserve the same isolation and original-evidence guarantees at both tiers.

Evaluate semantic obligations and concrete consequences, not headings, length, keywords, function/test counts or a single preferred architecture. Relevant immutable inputs get mechanical preservation checks. Explicit no-edit/no-publication boundaries can be checked mechanically. Extra steps fail only when they create demonstrable redundant work, scope drift or a missing dependency, not because an arbitrary operation count was exceeded.

Run the changed responsibility and its neighbor after a coherent edit. Run all smoke cases before the complete affected canaries for this shared-contract change. Report worker and grading cost separately, with attempted runs retained. Smoke success is not release acceptance, whole-workflow proof or evidence that fewer tokens always means better work.
