# Prepare or revise a pull request

Read the complete feature diff, original requirements, stage/review records, repository contribution rules, and requested delivery scope. Check that changes outside the task are not accidentally staged or pushed.

Verify the complete feature's behavior and relevant integration/regression checks. Local hooks are feedback, while CI verifies the requested change in the remote environment. Inspect the actual final code after fixes, formatting and conflict resolution.

Update affected README usage, DEVNOTES operations, significant Unreleased changes and implementation status. Keep test counts/logs in validation evidence. If this feature PR is also the agreed release preparation, include the chosen version and release notes together for review. If several features feed one release, leave the ordinary feature version unchanged.

Write a concise PR title/body around the final problem and resulting behavior. Include a concrete example when useful, important tradeoffs, actual validation, and material limitations. Do not narrate abandoned approaches or copy an entire design doc.

When authorized, push the intended branch and open or update the PR. Do not create a new PR for each stage commit. Follow CI/review results; verify findings, fix with regression checks, and re-review changed content. Merge only within the user's authorized scope and repository rules. If asked only to prepare, return the reviewable artifacts without publishing them.

For a newly created empty remote, an authorized initial commit/push may establish the default branch; do not create an artificial empty-base PR. Record exactly which remote/branch/PR actions happened rather than implying approval or merge from a successful push.
