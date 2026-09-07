# Reject invalid counter steps before mutation

`Counter.add(step=1)` now requires a positive Python integer and excludes
booleans. Invalid steps raise `ValueError` without changing the value; default
calls still add one and valid calls return the updated value. For example,
`Counter(4).add(True)` previously returned 5; it now raises and preserves 4.
Regression coverage checks rejection, state preservation and recovery, along
with default calls, large integers and integer subclasses. Usage and Unreleased
notes describe the contract; the version is unchanged.

Snapshot: base `448b79a90ea1a526dfdd0b35e3b9bf0f4b2b4769` plus
[candidate.patch](evidence/stage-1/candidate.patch), SHA-256
`e5d8f7d8494b5cad806a9637d2f0d03e74250e21a90617e8b993fe2e52bbed42`.
Working-tree and staged behavioral content matched this snapshot during final local
preparation on 2026-09-07; requirements and gate inputs also matched.

Validation: the [fresh full local gate](evidence/stage-1/pr-preparation-checks.txt)
passed all seven tests under prepared Python 3.12.4; behavioral whitespace checks
passed. [Independent round 2](reviews/round-2.md) completed the mandatory recheck
with no open material findings and retained R1 as reviewer verified fixed.
Full staged whitespace checking has the accepted evidence-only diagnostics
documented in that review; original evidence bytes are preserved.

[Fixture-user acceptance](reviews/user-acceptance.md) accepts this behavior.
The final acceptance section of the linked check log records the fresh full gate
passing seven tests under the unchanged reviewed inputs. This local PR snapshot
accompanies the authorized stage commit; its resulting ID and actual commit-hook
outcome are retained in the final delivery reply. No remote PR or remote CI
validation occurred. See [PLAN.md](PLAN.md) for current delivery status.
