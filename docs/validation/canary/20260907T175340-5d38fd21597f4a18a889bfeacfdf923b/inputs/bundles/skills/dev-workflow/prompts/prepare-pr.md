# Prepare or revise a pull request

Read the current delivery record, original requirements, complete intended feature diff and repository contribution rules. Follow its links to relevant review/check evidence; open older records when resolving a discrepancy, not to reconstruct every completed stage. Check that unrelated changes are not staged or pushed.

Compare the final behavior, requirements, check configuration, relevant inputs/runtime and freshness needs with the latest verified candidate. Reuse applicable results; run newly affected checks and the repository's mandatory final gate. Code equality alone does not establish applicability. Inspect actual final content after fixes, formatting or conflicts. Local hooks and remote CI establish their own observed checks; do not imply remote validation from a local result.

Apply the project's agreed test tiers. Record release-only expensive checks as pending or tied to their previously tested inputs; fast checks can establish ordinary PR readiness without claiming release readiness. Update affected regression cases when behavior changes. Do not promote historic/self-reported output to current evidence.

Update affected README usage, DEVNOTES operations and significant Unreleased changes. One existing plan/handoff owns live delivery status; link it from contract documents. Keep raw logs in evidence. If this PR is also agreed release preparation, include the chosen version and notes together; otherwise leave the feature version unchanged.

Write a concise PR title/body around the final problem and resulting behavior, a useful example, tradeoffs, actual validation and limits. This is a snapshot for its identified revision, not a second live status record. For example: “Saved filters retain their labels after reload; unnamed filters still work. Existing and new round-trip checks passed on this candidate.” Include only claims supported by the actual task evidence.

When authorized, push the intended branch and open or update the PR. Do not create a new PR for each stage commit. Follow CI/review results; verify findings, fix with regression checks, and re-review changed content. Merge only within the user's authorized scope and repository rules. If asked only to prepare, return the reviewable artifacts without publishing them.

For a newly created empty remote, an authorized initial commit/push may establish the default branch; do not create an artificial empty-base PR. Record exactly which remote/branch/PR actions happened rather than implying approval or merge from a successful push.

After preparing the PR/handoff, load [delivery checks](../references/delivery-checks.md). Correct supported issues; disclose unresolved conditions. Otherwise remain silent, without a self-check report or another review round.
