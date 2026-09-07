# Execute the current stage

Read the current agreed outcome, review policy and latest findings/evidence before editing. Establish the relevant baseline and identify pre-existing failures. Use the shared stage contract in SKILL.md and the [delivery-record contract](../assets/stage-record.template.md); an existing note can already satisfy the latter.

## Implement and verify

If a finding is already reviewer-verified, first compare the relevant candidate and evidence applicability. Reuse that resolution when it still holds and proceed to the remaining authorized action. Do not write a new verification program for an unchanged resolved issue. Changed content or missing verification requires checking the full affected invariant; an author's fixed label is not closure.

Implement supported changes with meaningful tests, preserving unrelated work. Run focused checks as useful during development and the repository's required complete gate. An installed hook that executes the same suite under the applicable inputs/runtime establishes that suite's result; a second identical standalone invocation is unnecessary unless separately required. Retain the fast/expensive test cadence and all mandatory gates/rechecks. Do not suppress a failing baseline or empty collection.

Update affected usage/developer documentation and significant Unreleased impact. A private rename or extra test does not itself change the design or plan. If an assumption fails, revise the affected decision/outcome and obtain targeted review before dependent work.

## Review and fix

Identify the review candidate once using a clean commit/tree, or base plus captured relevant changed-file diff and new-file content. Include the requirements/check configuration needed to interpret results. Later records cite this snapshot. Preserve original output and otherwise unavailable reviewed versions once; subsequent handoffs link them.

Stage intended files, including new files; inspect automatic hook changes and what the staged diff actually contains. Pause edits to the reviewed content while the user and authorized independent reviewer inspect it. Supply original requirements, actual code/tests, diff and evidence without a preferred verdict. Disclose unavailable independence.

Use the [review feedback contract](../assets/review.template.md) for findings/dispositions. Fix supported material findings, recheck the full affected invariant and obtain required reviewer verification. Widen checks only for newly affected boundaries. Preserve prior concerns; an unchanged resolved concern does not restart every earlier stage.

## Commit and hand off

Verify stage acceptance, required review/human status and the agreed final gate. Reinspect the final staged diff after hook fixes; never bypass hooks. Commit only within existing authorization, then report the actual commit and hook outcome in the durable delivery response or established check record. A commit need not contain its own resulting hash. Avoid another commit solely for self-recording; honor an explicit repository evidence-retention requirement without creating recursive evidence.

Advance only when accepted and the next outcome is in scope. A status-only handoff updates the existing delivery record with links to original reviews/checks. Reconcile other current entrypoints by removing stale execution claims and linking that record; update design/spec decisions only when a decision changes. PR text may summarize an identified revision without becoming another live record. Load the Delivery section of [artifact checks](../references/artifact-checks.md) after the update. Correct supported issues and disclose unresolved conditions; otherwise remain silent, with no self-check report or extra round.
