# Validate counter steps before mutation

`Counter.add(step=1)` now rejects zero, negative values, booleans and non-integers
with `ValueError` before changing the stored value. For example, `Counter(4).add(True)`
previously returned 5; it now raises and preserves 4. Default calls still add one,
and positive Python integers, including integer subclasses, return the updated value.

Regression coverage checks invalid inputs, state preservation and recovery, default
calls, explicit steps, repeated updates and large integers. Usage and Unreleased
notes reflect the behavior required by [FEATURE.md](FEATURE.md).

Validation: fresh focused unittest discovery and the full `hooks/pre-commit` gate
both passed all 7 tests with the prepared Python runtime. See [raw results](stage-records/stage-1/pr-preparation/results.json)
and [content identity](stage-records/stage-1/pr-preparation/initial-identity.json).
[Independent round 2](reviews/round-2.md) is ready for candidate-1; R1 is
reviewer-verified fixed, with no open findings. Implementation and tests remain
byte-identical to that candidate; subsequent edits only refresh delivery records.

Human acceptance and stage acceptance remain pending. This is a local PR draft;
no commit, push, hosted PR or CI run has occurred. Validation covers the prepared
runtime only; no release-only suite is specified. Version remains 0.1.0.
Historical evidence retains the whitespace diagnostics described in the
[handoff](stage-records/stage-1/record.md).
