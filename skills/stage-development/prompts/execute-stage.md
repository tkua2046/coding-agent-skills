# Execute the current stage

Inputs: target repository, stage plan/current stage, authoritative specs/design, review policy and existing findings. Read repository instructions and preserve unrelated changes. Establish current code and tests before editing; identify pre-existing failures explicitly.

## Implement and check

1. Implement the bounded behavior with relevant tests. Use independent expected outcomes; include failure behavior where it matters. Run focused tests as changes develop.
2. Update only documentation affected by this behavior or workflow: user instructions, developer operations, significant Unreleased changes, or stage progress. A private rename/new test does not require a design/plan rewrite. Keep code/test detail with the implementation and evidence with the stage record. Do not put test output in README or CHANGELOG.
3. Run the repository's agreed lint/format and complete commit checks. Honor its fast/expensive test cadence: release-only suites may remain explicitly pending for an ordinary stage/PR. A collection error, no tests, or failed required check cannot count as passing. If the project has a known failing baseline, explain it and establish the agreed gate; do not silently skip it.
4. Inspect any automatic changes made by hooks. Stage the intended files, including new files, and review what will actually be committed. Default pre-commit execution is not a promise to check every untracked file.

## Review and fix

5. Freeze an identifiable review snapshot: commit/tree when clean, or base commit plus captured diff and relevant new-file content/hashes. HEAD alone does not identify a dirty working tree. Record what tests ran against that content.
6. Pause implementation edits while the user and an authorized independent reviewer examine the snapshot. Give the reviewer the raw requirements, relevant code, tests and diff; do not supply a preferred verdict. If independent review is unavailable, report the limitation rather than simulating it in the same context.
7. Keep stable finding IDs and distinguish open, author-reported fixed, reviewer-verified, refuted with evidence, and accepted nonblocking limitation. Verify the claim before implementing a suggested fix. Preserve original findings and append each round's candidate, checks and disposition; keep current open IDs and next action first. Recheck the whole affected invariant, not only the part the author changed.
8. Make necessary fixes with regression tests. Rerun affected checks and obtain necessary review of changed content. If code changed after a check/review, its old result does not establish the new content's readiness.

## Commit and advance

9. Verify stage acceptance, the agreed full gate, review dispositions, required human-review status, and documentation. Recheck the final staged diff after hook fixes. Never bypass hooks to obtain a commit.
10. Commit when authorized by the task. Record the actual commit and evidence. Advance only when this stage is accepted and the next stage is in scope; otherwise state the next action and pending condition.

If the user delegated autonomous completion, use that recorded review policy instead of waiting for a fictional human approval. If human review is required, silence or elapsed time is not acceptance. Local checks, agent review and human review are separate statuses.

If implementation reveals a false design assumption, revise affected specs/design/plan and obtain targeted review before dependent work. Avoid an unbounded rewrite or restarting every previous review.

Before handing off or after context loss, use one short current-state record: candidate identity, completed outcome, next action, open finding IDs, latest check/review links, and human-review status. Resume from evidence; do not repeat completed stages or infer acceptance from an old “fixed” label. Keep previous reports available behind links; copying the entire conversation into the plan is unnecessary.
