# Validate counter steps before mutation

`Counter.add(step=1)` now rejects zero, negative values, booleans and non-integers
with `ValueError` before changing the stored value. For example, `Counter(4).add(True)`
previously returned 5; it now raises and preserves 4. Default calls still add one,
and positive Python integers, including integer subclasses, return the updated value.

Regression coverage checks invalid inputs, state preservation and recovery, default
calls, explicit steps, repeated updates and large integers. Usage and Unreleased
notes reflect the behavior required by [FEATURE.md](FEATURE.md).

Validation: fresh focused unittest discovery and the full `hooks/pre-commit` gate
both passed all 7 tests with the prepared Python runtime. See [actual checks](stage-records/stage-1/completion/results.json)
and [identity verification](stage-records/stage-1/completion/identity.json).
[Independent round 2](reviews/round-2.md) is ready for candidate-1; R1 is
reviewer-verified fixed, with no open findings. Implementation and tests remain
byte-identical to that candidate; subsequent edits refresh delivery records.

[Fixture-user acceptance](reviews/user-acceptance.md) is received and Stage 1 is
accepted. Local stage commit: `d302a348e209e02e4be36d9eaa75faade1e1e39c`.
The installed commit hook passed all 7 tests; [commit evidence](stage-records/stage-1/completion/stage-commit.json)
records the actual commit, tree and output. This is a reviewable local PR document.

Validation covers the prepared runtime only; no remote CI, cross-runtime or release
testing is claimed, and no release-only suite is specified. Version remains 0.1.0.
Seven known whitespace diagnostics in three historical artifacts remain preserved
as documented in [the stage record](stage-records/stage-1/record.md).
No push, tag, release, version bump, external PR or later-stage work is in scope.
