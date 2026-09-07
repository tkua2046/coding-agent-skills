# Validate Counter steps before changing state

`Counter.add(step=1)` now rejects booleans, non-integers, zero and negative
steps with `ValueError` before changing the stored value. For example,
`Counter(4).add(True)` previously returned 5; it now raises and leaves the value
at 4. Default calls still add one, and positive integer steps return the updated
value. Usage and Unreleased notes describe the behavior.

Regression coverage includes invalid-input state preservation and recovery,
integer subclasses, and arbitrary-size integers. On the unchanged payload,
[independent round 2](reviews/round-2.md) records six passing tests, a passing
full local gate, 75 invalid-input boundary cases, and regression replay that
detects the baseline boolean defect. R1 is reviewer-verified resolved; no open
findings remain. This preparation verified the working/index manifest and
captured patch against that review; it did not rerun the unchanged test suite.

Human review and acceptance remain pending. This is a local PR draft; no commit
or remote PR has been created. Validation covers the supplied fixture and
prepared Python runtime; no remote CI or external integration checks ran.
VERSION remains 0.1.0. See the [stage handoff](stage-evidence/stage-1/record.md)
for exact candidate identity, retained evidence and the remaining acceptance gate.
