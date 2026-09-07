# Stage 1
Implement validated optional step and meaningful regression tests. Preserve default
add behavior and state on error. Full gate and required review precede commit.
No stage 2 in scope.

## Current delivery record

Stage 1 implementation and local validation are complete. [Round 1 independent
review](reviews/round-1.md) reports ready, with no open material findings and R1
reviewer verified fixed. The [original R1 input](reviews/input-R1.md) is preserved.
Human acceptance remains pending. Next: the separate independent recheck of this
handoff and the candidate below against [FEATURE.md](FEATURE.md). That recheck is
pending; the round-1 verdict does not authorize a commit or stage advancement.

Candidate: base commit `c75616c8b8167e4f5eb1fe2edc7489ff27ce5458` plus the
[captured patch](evidence/stage-1/candidate.patch), SHA-256
`2a2be5dcc9f22305b14f0213868cd299f77d3f9dfb2154aa1e748595c6999a2a`.
This preserves the otherwise uncommitted implementation, tests, usage and
changelog. Requirements, AGENTS.md, DEVNOTES.md, gate configuration and supplied
skills are unchanged from the base; use them there to interpret this candidate.
This record and raw evidence are delivery metadata outside the candidate patch.

On author resumption, [fresh identity and check evidence](evidence/stage-1/author-resume.txt)
confirmed that both working-tree and staged candidate diffs still exactly match
the captured patch above. Relevant requirements, instructions, operations, gate
and skills match the base; the installed hook and original R1 input also match
the reviewed inputs. The prepared runtime remains Python 3.12.4. R1's existing
regression covers both booleans, rejection without mutation and subsequent valid
use, so the reviewer-verified resolution remains applicable. No implementation
or test changes were needed. Focused discovery and the full local gate were each
rerun and passed all 8 tests, exit 0. Prior reports and evidence remain unchanged.

The baseline working tree was clean. [Original baseline output](evidence/stage-1/baseline.txt)
preserves the pre-existing negative-step failure: both focused tests and the full
gate ran 3 tests and exited 1. Validation now rejects invalid steps before mutation.
Tests cover default and explicit steps, invalid types (including booleans), state
preservation and recovery, integer initial values, subclasses and large integers.

[Candidate check output](evidence/stage-1/checks.txt) records the actual prepared
Python 3.12.4 runtime and commands. Focused unittest discovery and the full
`hooks/pre-commit` gate each passed all 8 tests with exit 0. The installed
`.git/hooks/pre-commit` is byte-identical to the checked gate script. No packages
were installed. These results apply to the captured candidate; mandatory review
rechecks and the commit-time hook remain required at their prescribed points.

[Staging checks](evidence/stage-1/staging.txt) confirm the staged candidate exactly
matches the captured patch and code/documentation pass `git diff --cached --check`.
The supplemental whole-index whitespace check exited 2 on preserved raw output's
final blank lines and patch context lines. Those evidence bytes are retained
unchanged. Git also emitted sandbox cache/global-ignore access diagnostics; its
staging and diff operations succeeded. Neither diagnostic affects the Python gate.

Intended implementation, documentation, review reports and evidence files are
staged for recheck; reviewed content is paused. Commit and PR text preparation
remain pending the separate recheck and human acceptance. No commit, version
bump, installation, external action or later stage was performed. This block
owns current delivery status.
