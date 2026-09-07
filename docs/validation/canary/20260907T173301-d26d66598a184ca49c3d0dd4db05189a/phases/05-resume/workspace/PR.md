# Validate counter steps before changing state

`Counter.add(step=1)` now rejects nonpositive integers, booleans and other types
with `ValueError` before changing the value. For example, `Counter(4).add(True)`
raises and retains 4; a subsequent `add(3)` returns 7. Existing `add()` calls still
add one. Positive integers, including ordinary integer subclasses and large
integers, remain supported. Usage and Unreleased notes describe the contract.

Snapshot: base `c75616c8b8167e4f5eb1fe2edc7489ff27ce5458` plus the
[candidate patch](evidence/stage-1/candidate.patch), SHA-256
`2a2be5dcc9f22305b14f0213868cd299f77d3f9dfb2154aa1e748595c6999a2a`.
Delivery metadata is outside that implementation snapshot.

The [required local gate](evidence/stage-1/pr-preparation.txt) passed all 8 tests
on Python 3.12.4 during PR preparation. [Round 2 independent review](reviews/round-2.md)
verified the same candidate, passed focused checks and independent boundary probes,
and reports no open material findings; R1 is reviewer verified fixed.

At preparation, human acceptance and commit remain pending. This is local PR text;
no PR was opened and no remote CI or release validation was performed. Preserved
raw evidence has a known, reviewer-accepted nonblocking whole-index whitespace
limitation, documented in [staging evidence](evidence/stage-1/staging.txt).
[PLAN.md](PLAN.md) owns live status and the remaining acceptance/commit gates.
