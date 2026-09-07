# Stage 1
Implemented the validated optional step described in [FEATURE.md](FEATURE.md),
with regression tests for default behavior, valid integers, invalid inputs,
state preservation and recovery. Usage and Unreleased notes are updated.

Current state: local PR preparation complete; no open material findings.
[Round 1](reviews/round-1.md) found the candidate ready and marked R1 reviewer
verified fixed. [Round 2](reviews/round-2.md) completed the required independent
recheck with verdict ready. Human acceptance remains pending.
Next action: human review and acceptance of the identified candidate.
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
checks retained the applicable review evidence but did not fulfill the separate
independent recheck; round 2 subsequently completed it.

Fresh author PR preparation (2026-09-07): working-tree and index behavioral
diffs still match the candidate snapshot byte for byte. Requirements, instructions,
gate configuration, installed hook, R1 input and prepared runtime still match
the reviewed inputs. Round 2 and R1's verified resolution remain applicable.
The [fresh PR checks](evidence/stage-1/pr-preparation-checks.txt) record the full
local gate passing all seven tests and the behavioral whitespace check passing.
Original review reports and evidence remain unchanged, including the accepted
nonblocking evidence-whitespace limitation. No duplicate R1 probe was needed.

Delivery: intended files staged for review; [PR.md](PR.md) is a local title/body
snapshot for the identified candidate. The current user request explicitly
authorizes this preparation before human acceptance, superseding the prior
PR-text restriction. No commit, push, remote PR, CI or release action occurred.
PLAN remains the sole live delivery record.

After human acceptance, the next author context may finish the previously
authorized commit: compare the candidate and evidence applicability again,
run the required final gate, inspect the final staged diff, and honor the
installed commit hook without bypassing it. Record the actual commit and hook
result in the durable handoff; do not create a commit just to record its own hash.
Until acceptance, do not commit or advance. External actions remain out of scope.
No stage 2, version bump, installation or external action is in scope.
