# Validate counter steps before changing state

`Counter.add(step=1)` now accepts positive Python integers and rejects booleans,
non-integers, zero and negative steps with `ValueError` before mutation, matching
[FEATURE.md](FEATURE.md). For example, `Counter(4).add(True)` previously returned
5; it now raises and leaves the value at 4. Default `add()` still adds one and
returns the updated value. Ordinary integer subclasses remain supported.

Regression coverage exercises valid steps, large and negative initial values,
invalid inputs, state preservation and recovery. README usage and Unreleased
notes describe the behavior; version remains 0.1.0.

Validation: the full prescribed local gate (`"$CANARY_PYTHON" hooks/pre-commit`)
passed all 5 tests in the acceptance context; see [raw output](evidence/stage-1/acceptance-gate.txt).
[Identity checks](evidence/stage-1/acceptance-gate.txt) confirm unchanged reviewed
implementation tree `ab74bd69494b8cf9137da2d47b83434228faa3cc`, based on
`70da066553d48178e447c2ced60603351b90fc38`.
[Independent round 2](reviews/round-2.md) is ready with no open findings;
R1 is independently verified resolved. Historical baseline checks failed for
negative steps, as preserved in [baseline evidence](evidence/stage-1/baseline-tests.txt).

[Fixture-user acceptance](reviews/user-acceptance.md) and the required independent
recheck are complete; Stage 1 is accepted for local delivery. This is a local PR
draft for the synthetic exercise. Validation covers the prepared runtime and
local unittest gate; remote CI has not run. No separate lint/format or release
suite is prescribed. No push, tag, release, version bump or external PR creation
is authorized. See [PLAN.md](PLAN.md) for the current handoff and preserved
review/evidence history. The resulting local commit ID and actual commit-hook
outcome are reported in the retained final reply.
