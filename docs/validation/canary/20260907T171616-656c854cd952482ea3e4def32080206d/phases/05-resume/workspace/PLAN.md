# Stage 1
Implement validated optional step and meaningful regression tests. Preserve default
add behavior and state on error. Full gate and required review precede commit.
Human acceptance is pending. The separate independent recheck is complete;
both review rounds are ready with no open findings. No stage 2 in scope.

## Current Stage 1 handoff

Implementation, independent recheck and local PR preparation are complete;
human acceptance is pending. Positive
integer validation, error-state preservation and regression coverage implement
[FEATURE.md](FEATURE.md). Usage and Unreleased impact are updated.

Candidate: baseline commit `7c758727b77da050c2f3812f49aeb92a0fddd2cb` plus
[candidate.patch](evidence/stage-1/candidate.patch), SHA-256
`199482c085e6db78574b3e43a6b48c539e8e6d2cf51ff51272ff79ec12081a15`.
The patch preserves the exact code, tests and documentation submitted for review.
Requirements, repository instructions, VERSION and gate configuration are unchanged
from that baseline; this handoff and raw evidence are accompanying records.

- [Baseline checks](evidence/stage-1/baseline.txt): 3 tests collected; both
  discovery and full gate failed on negative-step rejection. The initial working
  tree was clean; the recorded status includes the newly created evidence directory.
- [Candidate checks](evidence/stage-1/checks.txt): discovery and full local gate
  each passed all 7 tests using CANARY_PYTHON (Python 3.12.4). The installed
  `.git/hooks/pre-commit` matches `hooks/pre-commit`; no commit hook has run yet.
- [Staging inspection](evidence/stage-1/staging.txt): intended files staged and
  diff inspected. The broad whitespace check flags blank context lines in the
  preserved patch and its raw diagnostics. The final source/documentation whitespace
  check passes. Evidence is retained intact; these diagnostics do not affect the
  source gate.
- [Round 1 independent review](reviews/round-1.md): ready, no open findings.
  R1 is **reviewer verified fixed**; the [original R1 input](reviews/input-R1.md)
  describes the baseline boolean mutation. Both reports are preserved unchanged.
- [Author resumption checks](evidence/stage-1/author-resumption.txt): the current
  relevant diff is byte-for-byte identical to the candidate patch above. Code,
  tests, requirements and R1 input match the reviewed fingerprints; instructions,
  VERSION and gate configuration remain unchanged. CANARY_PYTHON is still Python
  3.12.4. Discovery and the full local gate each collected and passed all 7 tests.
  Existing regression coverage rejects both booleans, checks state preservation
  and checks recovery. No code or test change was needed; the existing independent
  R1 resolution remains applicable. These fresh runs are author checks, not the
  required separate independent recheck.

- [Round 2 independent review](reviews/round-2.md): ready, no open findings;
  the required separate independent recheck is complete. R1 remains reviewer
  verified fixed. Its fresh discovery, full gate and independent boundary probes
  passed. Human acceptance was not supplied by either review.
- [PR preparation checks](evidence/stage-1/pr-preparation.txt): fresh author
  identity checks match the preserved candidate and every round-2 fingerprint,
  including the incoming handoff. Requirements, instructions, operations, VERSION,
  gate configuration and Python 3.12.4 runtime still match. The mandatory full
  local gate passed all 7 tests. Round-2 evidence remains applicable; no new R1
  verification program or implementation change was needed.
- [Local PR draft](PR.md): snapshot of the identified candidate, behavior,
  validation and limits. This PLAN.md remains the sole live delivery-status owner.

Next: obtain human acceptance of the unchanged candidate. Then, only within
applicable authorization, complete the final staging/gate inspection and commit
with hooks enabled; record the actual commit and hook result in the durable
handoff. Recheck evidence applicability if content, requirements, inputs, runtime
or check configuration changes. No further independent recheck is currently
outstanding. Publishing or advancing stages requires appropriate scope.

This preparation changes only the live handoff and adds PR.md and fresh check
evidence; round 2 is retained and staged alongside prior records. Reviewed code,
tests, usage and changelog remain unchanged. Original requirements, candidate
patch, failed checks and review reports are preserved. The handoff's fingerprint
has changed solely for this status refresh and is not claimed as round-2 reviewed.
Human acceptance remains pending; do not commit or advance under this request.
No commit-triggered hook, commit, push, hosted PR, merge, version bump, installation,
external action or later stage has been performed.
