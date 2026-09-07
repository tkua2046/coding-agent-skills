# Execute the current stage

Read the requested outcome, applicable review policy and relevant findings/evidence before editing. Use the shared stage contract in SKILL.md. Reuse an applicable baseline or run a focused check when a comparison is needed; identify pre-existing failures. Consult the [delivery-record example](../assets/stage-record.template.md) when a durable handoff is useful or required.

## Implement and verify

Investigate concrete unknowns that could change the implementation. Once the evidence is sufficient, proceed; reopen the approach only when new evidence or scope affects a decision. For an existing finding, reuse reviewer verification while its content and evidence remain applicable. Changed content or missing verification requires checking the affected invariant; an author's fixed label is not closure.

Implement supported changes, preserving unrelated work. Use existing checks and add tests where needed to verify changed behavior or a material risk. Run focused checks during development and the repository's required gate. An installed hook that executes the same suite under applicable inputs/runtime establishes that result; repeat it only for a separate requirement or new uncertainty. Preserve the fast/expensive test cadence and mandatory rechecks. Do not suppress a failing baseline or empty collection.

Update affected usage/developer documentation and significant Unreleased impact. A private rename or extra test does not itself change the design or plan. If an assumption fails, revise the affected decision/outcome; obtain a decision or targeted review before dependent work when the consequences or established policy require it.

## Review and fix

Inspect the complete intended deliverable, including new files and expected generated artifacts, for goal fulfillment, compatibility, unnecessary complexity and reviewability. Follow the established review policy and requested review work. Otherwise, focused verification and self-review can suffice for an understood local reversible change; add review where uncertainty, consequences or boundaries justify it.

For required or warranted external review, identify the candidate through an existing commit/tree or capture otherwise unavailable relevant diff and new-file content once. Include the requirements and check context needed to assess it. Keep that content stable while reviewers inspect it; supply original requirements, actual changes and evidence without a preferred verdict. Disclose unavailable independence. On resumption, compare affected content and evidence applicability, linking the original reference rather than copying it again.

Use the [review feedback contract](../assets/review.template.md) for findings and dispositions when reporting review. Fix supported material findings, verify the affected invariant and obtain required reviewer verification. Widen checks for newly affected boundaries. Preserve original concerns and evidence through immutable references; retention is scoped to the relevant work and actual repository policy.

## Commit and hand off

Verify the agreed outcome against the original goal and disclose any intentionally partial result, with actual required review/approval and final gate status. When committing is authorized, stage only intended files, including needed new artifacts, and inspect the complete staged diff after hook fixes. Never bypass hooks. Report the actual commit and hook outcome in the delivery response or established record; a commit need not contain its own resulting hash.

Continue to the next authorized outcome when its prerequisites and required approvals are satisfied. Report completed behavior, actual validation and remaining conditions. Update an existing delivery record when one is needed, linking original reviews/checks; otherwise the response suffices. Update design/spec only when decisions change. Load the Delivery section of [artifact checks](../references/artifact-checks.md) after the handoff. Correct supported issues and disclose unresolved conditions; otherwise remain silent.
