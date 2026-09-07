# Stage 1
Implemented the validated optional step described in [FEATURE.md](FEATURE.md),
with regression tests for default behavior, valid integers, invalid inputs,
state preservation and recovery. Usage and Unreleased notes are updated.

Current state: local implementation and checks complete; independent-agent review
in the next context and human acceptance are pending. No reviewer findings exist
yet; the author-observed baseline failure passes locally but is not independently
verified. Next action: independent review of the candidate below, with the required
review checks. Pause candidate edits during review.

Candidate: base `448b79a90ea1a526dfdd0b35e3b9bf0f4b2b4769` plus
[candidate.patch](evidence/stage-1/candidate.patch), SHA-256
`e5d8f7d8494b5cad806a9637d2f0d03e74250e21a90617e8b993fe2e52bbed42`.
The patch preserves the implementation, tests and usage/changelog changes.
Original requirements, repository instructions and [gate configuration](DEVNOTES.md)
remain at the base revision, including `hooks/pre-commit`. This plan and evidence
are delivery metadata outside the behavioral candidate.

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

Original review reports: none supplied or produced in this phase. Preserve future
reports and link them here; author checks do not constitute independent review.
Recheck evidence applicability against the candidate, requirements, gate and runtime
on resumption; required independent rechecks remain mandatory.

Delivery: intended files staged for review, no commit or PR text prepared.
Commit and PR text preparation are authorized only after required reviews and
human acceptance, with the final gate and installed commit hook honored.
No stage 2, version bump, installation or external action is in scope.
