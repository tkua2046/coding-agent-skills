# Workflow burden: focused repair proposal

Recommendation: reduce repeated status, snapshot and verification work in the existing operations. Keep meaningful checks and original evidence. Adding another general “avoid complexity” instruction will not resolve these concrete conflicts.

Scope: static inspection of current skills at `d76bb80fa15a01e8240a9c328a0bac485b95564b` and the two original runs below. No reader regrading, model trials, live skill/case/runtime edits, commits or external actions. Attribution below is an instruction-to-observation hypothesis, not a demonstrated causal effect.

## What actually consumed effort

| Run | Observed work | Attribution |
|---|---|---|
| [Inventory][i-report] | 619 seconds across five executed phases. Both reviews accepted immediately; four fix/recheck phases were skipped. Final status reconciliation alone took 107 seconds. | The [case][i-case] requires planning, combined document review, implementation, code review and final handoff. These are not agent-invented rounds. |
| [V6][v-report] | 945 seconds across six prescribed phases. First review already resolved R1; the subsequent author phase took 158 seconds without changing the implementation. | [Requests][v-case] force that phase, a second independent review, resumption, and later fixture-user acceptance. The extra verification machinery within those phases was an agent choice. |

Times include model/tool/service waiting, not just useful work. Markdown/text totals grew from 52 to 373 lines for inventory and 25 to 739 for V6, **including raw evidence**; those totals are not human reading requirements. The clearer burden is duplicated live content and work done to maintain it:

- Inventory's [author plan][i-plan] reached 99 lines: stage row, done condition, full review procedure, commands, baseline, and another current-state section repeat overlapping facts. Final handoff updated delivery status in DESIGN, PLAN and SPEC and archived two full documents. The [execution][i-handoff] shows these actual edits. Preserving those uncommitted reviewed versions was justified once status had been embedded there; manufacturing three mutable status copies was avoidable.
- V6's [first review][v-r1] already verified R1, including baseline sensitivity. The author then created a [69-line verifier][v-script]; it failed to import the application, then generated whitespace failures while staging raw diagnostics. The [original execution][v-fix] preserves the resulting script/log repair detour. Later PR preparation generated an [810-line verification JSON][v-verification], recording 75 Git calls and hashes for 59 paths, including 19 unchanged supplied skill files. Repeated sandbox diagnostics inflate that file; no skill explicitly asks for 810 lines.
- V6 made a second commit solely to record the first commit's hash and hook output, as its [final execution][v-delivery] states. Whether the case may reject this is the contract reviewer's decision. Independently, self-recording delivery created extra work.

## Narrow replacements to review

1. **One live delivery status.** In [document ownership](../../skills/dev-workflow/references/documents.md), distinguish design-decision status from execution/review status. Replace the universal status-opening instruction with: “Design/spec retain their contract and decision status; link to the existing plan/handoff for current delivery, checks and acceptance.” In the [stage record](../../skills/stage-development/assets/stage-record.template.md), combine State, At a glance and trailing review/gate fields into one current-state block followed by evidence links. Update that block instead of copying the same statuses into SPEC, DESIGN, PLAN and PR. Preserve originals/reviews; link an available immutable version, and capture an uncommitted reviewed version when otherwise unavailable.

2. **Identify the reviewed change without auditing the whole workspace.** Replace [execute-stage](../../skills/stage-development/prompts/execute-stage.md) step 5 with: “Identify the candidate once using a commit/tree, or base plus captured changed-file diff and new-file content. Include relevant requirements/check configuration; later reports cite this identity. On resumption compare affected content with that snapshot.” Replace step 10's “Record the actual commit and evidence” with: “Report the resulting commit and hook outcome in the durable delivery response or established external check record; a commit need not contain its own resulting ID.” A fixture that explicitly requires an in-repository completion record takes precedence. Keep original evidence, but remove automatic full-workspace hash inventories and a second commit solely for self-reference.

3. **Make an already-resolved finding a different execution path.** Replace the opening of execute-stage's fix/recheck instructions with: “Compare current content and the latest finding dispositions first. If the relevant content is unchanged and the finding is reviewer-verified, cite that resolution and proceed to the remaining authorized action. If content changed or verification is missing, check the full affected invariant.” Mirror this branch in [review-stage](../../skills/stage-development/prompts/review-stage.md). Keep explicitly required rechecks and gates. This targets V6's bespoke author verifier and repeated boundary matrix; it does not excuse the partial-fix failure covered by V5.

4. **Use check results once for the purpose they establish.** Replace [prepare-pr](../../skills/dev-workflow/prompts/prepare-pr.md)'s unconditional feature-verification paragraph with: “Compare the final behavior and check configuration with the latest verified candidate. Reuse applicable results; run newly affected checks and the repository's mandatory final gate.” In execute-stage step 3, specify that an installed hook executing the same suite can establish that suite's result; separate focused runs remain useful during changes, and explicit separate-command requirements remain binding. Inventory planning ran the same suite directly, through the source hook and through the installed identical hook. Do not generate a fresh verifier merely to restate a prior verified result.

5. **Lead templates with the decision/outcome, not workflow metadata.** The [design template](../../skills/feature-design/assets/design.template.md) places instructions and status before its overview; the [plan template](../../skills/implementation-plan/assets/implementation-plan.template.md) places execution policy before outcomes. Move drafting instructions out of generated content. Start design with “Outcome; chosen mechanism and reason; material cost/failure consequence with example”; follow with sources/decision status and a delivery-status link. Start plan with next observable outcome, dependency and acceptance; move policy to one link afterward. Delete the duplicated done-condition/procedure prose when already expressed by that outcome and linked policy. Inventory initially explained preflight on lines 4–6, but final DESIGN put a review-status paragraph first. This supports a structural repair hypothesis, not a new verdict on its reading probe.

## Behavioral checks and continued progress

- Replay inventory after the narrow edits: retain correct atomic rejection/continuation and both meaningful reviews; inspect whether status has one owner, policy is linked once, and status-only handoff avoids copying contract documents. Preserve older reviewed content and truthful pending human acceptance.
- Use V6 under its independently settled contract: unchanged verified R1 should require no new author test harness or expanded counterexample matrix. Required reviews/hooks still execute; partial fixes still fail V5. Check that commit reporting avoids self-reference work without losing durable evidence.
- Check plan maintenance with a private rename/new test: no second implementation inventory or unrelated design edits. Opening checks should inspect the proposed structure, while the main reviewer independently handles actual reader evaluation.

Make one coherent change, run the relevant behavioral checks, then choose the next repair from observed failure and effort. Broaden regression coverage when shared instructions change; run required release checks before release. Track elapsed work and redundant artifacts descriptively, not as new arbitrary pass quotas. An ineffective repair calls for reconsidering its cause, not retrying until green or stopping at a self-imposed total-call cap.

[i-report]: ../validation/canary/20260907T094228-9cae63d40af941b8be555400028d4817/report.json
[i-case]: ../validation/canary/20260907T094228-9cae63d40af941b8be555400028d4817/inputs/case/case.json
[i-plan]: ../validation/canary/20260907T094228-9cae63d40af941b8be555400028d4817/phases/09-handoff/workspace/docs/PLAN.s1-author.md
[i-handoff]: ../validation/canary/20260907T094228-9cae63d40af941b8be555400028d4817/phases/09-handoff/execution.json
[v-report]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/report.json
[v-case]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/inputs/case/case.json
[v-r1]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/02-review/workspace/reviews/round-1.md
[v-script]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/03-fix/workspace/stage-evidence/stage-1/author-recheck/verify.py
[v-fix]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/03-fix/execution.json
[v-verification]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/05-resume/workspace/stage-evidence/stage-1/pr-preparation/final-verification.json
[v-delivery]: ../validation/canary/20260907T085827-a49cbdf9e919485186ac029e4c1b96f3/phases/06-accepted-delivery/execution.json
