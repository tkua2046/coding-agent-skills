# Validate Counter steps before changing state

`Counter.add(step=1)` rejects booleans, non-integers, zero and negative steps
with `ValueError` before changing the stored value. For example,
`Counter(4).add(True)` previously returned 5; it now raises and leaves the value
at 4. Default calls still add one, and positive integer steps return the updated
value. Usage and Unreleased notes describe the behavior.

The six regression tests pass in both fresh unittest discovery and the full
local gate using CANARY_PYTHON. Coverage includes invalid-input state preservation
and recovery, integer subclasses, and arbitrary-size integers. The unchanged
implementation matches the reviewed candidate. [Independent round 2](reviews/round-2.md)
also verified 75 invalid-input cases and baseline regression sensitivity;
R1 is reviewer-verified resolved and no findings remain open.
[Fixture-user acceptance](reviews/user-acceptance.md) satisfies the required
synthetic user review. See the [stage record](stage-evidence/stage-1/record.md)
for commit identity and [current raw checks](stage-evidence/stage-1/completion/gate.txt).

Validation is limited to this fixture and prepared Python runtime; no remote CI
or external integration checks ran. Historical baseline failures and auxiliary
check failures remain preserved in the stage evidence. VERSION remains 0.1.0.
This is local PR preparation only; no push, tag, release, or external PR occurred.

Local stage commit: `8619b4540ff1a3d1fecd2dafdac71c1c8927aa79`. Its installed pre-commit
hook passed all six tests and left the staged tree unchanged. The documentation
follow-up records that commit and its [actual output](stage-evidence/stage-1/completion/stage-commit.txt).
