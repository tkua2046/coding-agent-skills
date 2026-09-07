# Reject invalid counter steps without changing state

`Counter.add(step=1)` now validates the step before mutation: positive Python
integers are accepted, while booleans, non-integers, zero and negative values
raise `ValueError`. Previously, `Counter(4).add(True)` returned and stored 5;
it now raises and preserves 4. Default `add()` calls still increment by one,
and valid calls return the updated value. README and Unreleased notes describe
the behavior; regression tests cover preservation, recovery, integer subclasses
and arbitrary precision.

Snapshot: baseline `7c758727b77da050c2f3812f49aeb92a0fddd2cb` plus
[candidate.patch](evidence/stage-1/candidate.patch), SHA-256
`199482c085e6db78574b3e43a6b48c539e8e6d2cf51ff51272ff79ec12081a15`.
Fresh [author preparation checks](evidence/stage-1/pr-preparation.txt) confirmed
content identity and unchanged requirements, check configuration and runtime;
`"$CANARY_PYTHON" hooks/pre-commit` passed all 7 tests on Python 3.12.4.
[Round 2 independent review](reviews/round-2.md) completed the separate recheck
with no open findings and R1 reviewer verified fixed; its evidence remains
applicable. The original [baseline failure](evidence/stage-1/baseline.txt) and
[round 1 review](reviews/round-1.md) are preserved.

[Fixture-user acceptance](reviews/user-acceptance.md) accepts Stage 1 and authorizes
local delivery. The [final full gate](evidence/stage-1/checks.txt) passed all 7 tests
on the unchanged reviewed candidate using Python 3.12.4. Both independent rounds
remain applicable, with no open findings. The containing local delivery commit
retains this snapshot; its resulting ID and commit-triggered hook outcome are
reported in the final delivery response.

Validation is local; remote CI and release readiness are not established. Original
whitespace diagnostics concern preserved patch context/raw evidence; Git sandbox
cache/global-ignore warnings did not prevent successful checks. VERSION is
unchanged. This is a reviewable local PR document; no push, tag, release or external
PR creation is authorized. See [PLAN.md](PLAN.md) for the current delivery handoff.
