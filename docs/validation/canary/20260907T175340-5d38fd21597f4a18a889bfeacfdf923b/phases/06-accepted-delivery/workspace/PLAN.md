# Stage 1
Implemented the validated optional step described in [FEATURE.md](FEATURE.md),
with regression tests for default behavior, valid integers, invalid inputs,
state preservation and recovery. Usage and Unreleased notes are updated.

Current state: Stage 1 accepted for local delivery, with the reviewed behavior
and reviewable [PR.md](PR.md) retained in this stage commit. No open material
findings. [Round 1](reviews/round-1.md) verified R1 fixed;
[round 2](reviews/round-2.md) completed the required independent recheck.
[Fixture-user acceptance](reviews/user-acceptance.md) now satisfies the remaining
acceptance condition. Next action: no further work within the authorized scope.
The resulting commit ID and actual installed-hook outcome are reported in the
retained final delivery reply; this document does not require a bookkeeping commit.

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

Earlier PR preparation staged the intended files and produced the local PR
snapshot while acceptance was pending. No earlier phase committed: HEAD and its
reflog contained only the fixture baseline at final resumption. The original
reviews and check records retain their historical pending-acceptance statements.

Final acceptance resumption (2026-09-07): the working-tree and index behavioral
diffs again match the existing candidate snapshot byte for byte. Requirements,
instructions, version, gate configuration, installed executable hook, R1 input
and prepared Python 3.12.4 runtime match the reviewed inputs. Round 2 and R1's
verified resolution remain applicable. The final section of the existing
[PR preparation log](evidence/stage-1/pr-preparation-checks.txt) records these
comparisons, the required full local gate passing seven tests (exit 0), and the
behavioral whitespace check passing (exit 0). The installed commit hook must also
run without bypass on this stage commit; its actual result belongs in the final
reply. Original evidence remains preserved, including the accepted whitespace
limitation. Only delivery metadata and fixture acceptance changed in this phase.

PLAN remains the sole live delivery record. Local delivery includes PR title/body
preparation, not external PR creation or remote CI. No stage 2, push, tag, release,
version bump, installation or external action is in scope.
