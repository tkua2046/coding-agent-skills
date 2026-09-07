# Stage 1
Implemented the validated optional step described in [FEATURE.md](FEATURE.md),
with regression tests for default behavior, valid integers, invalid inputs,
state preservation and recovery. Usage and Unreleased notes are updated.

Current state: author resumption complete; no open material findings.
[Round 1](reviews/round-1.md) found the candidate ready and marked R1 reviewer
verified fixed. The separate independent recheck and human acceptance remain
pending. Next action: independent recheck of the candidate and updated handoff.
Pause candidate edits during review; do not commit or advance.

Candidate: base `448b79a90ea1a526dfdd0b35e3b9bf0f4b2b4769` plus
[candidate.patch](evidence/stage-1/candidate.patch), SHA-256
`e5d8f7d8494b5cad806a9637d2f0d03e74250e21a90617e8b993fe2e52bbed42`.
The patch preserves the implementation, tests and usage/changelog changes.
Original requirements, repository instructions and [gate configuration](DEVNOTES.md)
remain at the base revision, including `hooks/pre-commit`. This plan and evidence
are delivery metadata outside the behavioral candidate.

On author resumption (2026-09-07), both working-tree and index behavioral diffs
matched this snapshot byte for byte. Requirements, repository instructions and
gate configuration still match the base; the installed hook matches the gate.
The prepared Python 3.12.4 runtime and R1 input identity match round 1.
Only delivery metadata was added or updated in this phase; code and regression
tests remain unchanged. R1's independently verified resolution therefore remains
applicable: existing coverage rejects both booleans, preserves state and checks
successful recovery. No additional correction or duplicate probe was needed.

Evidence (2026-09-07, prepared CANARY_PYTHON, Python 3.12.4):

- [Baseline](evidence/stage-1/baseline.txt): both unittest discovery and full gate
  collected three tests and failed the existing negative-step test. The initial
  working tree was clean; the baseline log's untracked evidence directory was
  created by baseline capture.
- [Candidate checks](evidence/stage-1/checks.txt): unittest discovery and full local
  gate each passed all seven tests; diff whitespace check passed. The installed
  hook matches the checked gate script. Git emitted sandbox cache/config warnings
  while returning success; test commands returned zero without those warnings.
- [Staged whitespace check](evidence/stage-1/staged-check.txt) returned 2 after
  evidence was added: blank context lines in the saved patch and terminal blank
  lines in raw logs trigger whitespace diagnostics. These original evidence bytes
  are retained. The implementation diff check and required full gate passed;
  this additional evidence-format check did not.
- [Fresh author checks](evidence/stage-1/author-resume-checks.txt): identity
  comparisons passed; focused unittest discovery and the full gate each collected
  and passed seven tests (exit 0). The behavioral diff whitespace check passed.
  Git emitted sandbox diagnostics while succeeding; Python checks passed without
  those diagnostics. Round 1 records the fuller evidence-only whitespace list;
  that accepted nonblocking limitation remains, and original bytes are retained.

Original review evidence: [R1 input](reviews/input-R1.md) and
[independent round 1](reviews/round-1.md), preserved unchanged. Round 1 reproduced
the baseline boolean defect and verified the candidate fix, including 52 independent
cases. The historical baseline log above concerns negative steps. Fresh author
checks retain the applicable review evidence but do not fulfill the separate
independent recheck, which remains mandatory and pending.

Delivery: intended files staged for review, no commit or PR text prepared.
Commit and PR text preparation are authorized only after required reviews and
human acceptance, with the final gate and installed commit hook honored.
No stage 2, version bump, installation or external action is in scope.
