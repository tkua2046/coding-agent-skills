# Execute the current stage

Inputs: target repository, stage plan/current stage, authoritative specs/design, review policy and existing findings. Read repository instructions and preserve unrelated changes. Establish current code and tests before editing; identify pre-existing failures explicitly.

## Implement and check

1. Implement the bounded behavior with relevant tests. Use independent expected outcomes; include failure behavior where it matters. Run focused tests as changes develop.
2. Update only documentation affected by this behavior or workflow: user instructions, developer operations, significant Unreleased changes, or stage progress. Do not put test output in README or CHANGELOG.
3. Run the repository's agreed lint/format and complete commit checks. A collection error, no tests, or failed check cannot count as passing. If the project has a known failing baseline, explain it and establish the agreed gate; do not silently skip it.
4. Inspect any automatic changes made by hooks. Stage the intended files, including new files, and review what will actually be committed. Default pre-commit execution is not a promise to check every untracked file.

## Review and fix

5. Freeze an identifiable review snapshot: commit/tree when clean, or base commit plus captured diff and relevant new-file content/hashes. HEAD alone does not identify a dirty working tree. Record what tests ran against that content.
6. Pause implementation edits while the user and an authorized independent reviewer examine the snapshot. Give the reviewer the raw requirements, relevant code, tests and diff; do not supply a preferred verdict. If independent review is unavailable, report the limitation rather than simulating it in the same context.
7. Triage findings as pending, fixed, refuted with evidence, or accepted nonblocking limitation. Verify the claim before implementing a suggested fix. Keep original findings and append their dispositions.
8. Make necessary fixes with regression tests. Rerun affected checks and obtain necessary review of changed content. If code changed after a check/review, its old result does not establish the new content's readiness.

## Commit and advance

9. Verify stage acceptance, the agreed full gate, review dispositions, required human-review status, and documentation. Recheck the final staged diff after hook fixes. Never bypass hooks to obtain a commit.
10. Commit when authorized by the task. Record the actual commit and evidence. Advance only when this stage is accepted and the next stage is in scope; otherwise state the next action and pending condition.

If the user delegated autonomous completion, use that recorded review policy instead of waiting for a fictional human approval. If human review is required, silence or elapsed time is not acceptance. Local checks, agent review and human review are separate statuses.

If implementation reveals a false design assumption, revise affected specs/design/plan and obtain targeted review before dependent work. Avoid an unbounded rewrite or restarting every previous review.
