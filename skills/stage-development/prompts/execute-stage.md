# Execute the current stage

If the request only asks to summarize or reconcile existing status/evidence, use [Hand off](handoff-stage.md) and stop here. An independent review or finding recheck uses [Review stage](review-stage.md). Requested implementation or gate execution stays here, even when a gate-only request excludes code edits.

## Establish the remaining work

Read the requested outcome and relevant code, current handoff, findings and check evidence. On resumption, distinguish completed work from pending work and compare the affected candidate with its reviewed content. Reuse applicable verification under the shared contract in SKILL.md; an author's fixed label is not closure.

Investigate material unknowns, then proceed within authorization. Use an applicable baseline or run a focused comparison when needed; identify pre-existing failures. If an assumption fails, revise the affected decision/outcome and obtain a decision or targeted review before dependent work when consequences or policy require it.

## Implement and verify

Make the scoped change while preserving unrelated work. For a supplied finding, repair the whole affected invariant, including failure state and later recovery, rather than only its reported symptom. Use existing checks and add regression coverage where changed behavior or material risk needs it; retain meaningful existing expectations.

Run focused checks during repair and the required project gate. Inspect actual results, collection and hook edits; do not suppress a failing baseline or empty suite. An executed hook can establish the same suite's result under applicable inputs/runtime; installed configuration alone cannot. Repeat checks for affected changes, new uncertainty or an explicit requirement, preserving the project's fast/expensive cadence.

Update affected usage/developer documentation and significant Unreleased impact under project conventions. Private renames or extra tests do not by themselves require design/plan changes.

## Review and resolve

Inspect the complete intended deliverable, including new files and expected generated artifacts, against the original goal: behavior, compatibility, justified complexity and reviewability. Apply the shared review policy; do not start additional rounds merely to polish wording.

For required or warranted external review, identify stable content through an existing commit/tree or capture otherwise unavailable relevant diff and new-file content once. Supply original requirements, actual changes and check context without a preferred verdict. Keep the reviewed content stable and disclose unavailable independence. Preserve original findings and evidence through immutable references within the work's scope and repository retention policy.

Fix supported material findings, verify the whole affected concern and obtain required reviewer verification. Widen checks for newly affected boundaries. Keep partial fixes open; a verified complete fix should close. Evidence-based refutation or an accepted nonblocking limitation should remain distinguishable from repair. Use the optional [feedback example](../assets/review.template.md) if helpful when reporting findings.

## Complete or resume coherently

Confirm the agreed outcome against the original goal, actual gate results and required review/approval. An intentionally partial stage must leave a usable state and expose what remains. Continue to the next authorized outcome when prerequisites and required approvals are satisfied.

When committing is authorized, stage only intended files and inspect the complete staged diff after hook fixes; never bypass hooks. Report the actual commit and hook result afterward. A committed record need not contain its own resulting hash.

Use the Delivery section of [final checks](../references/artifact-checks.md), then deliver the completed behavior, observed validation and any material remaining condition. Update one existing handoff when useful or required; the [record example](../assets/stage-record.template.md) is optional. A trivial completion needs no additional record unless required; finished work needs no invented next step.
