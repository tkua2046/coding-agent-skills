# S1: whole-order reservation rejection

State: implemented; independent code review pending. Human review: pending.
Next action: the separately assigned independent agent reviews this candidate using
the [request](../docs/REQUEST.md), [design](../docs/DESIGN.md),
[plan](../docs/PLAN.md), [contract](../docs/SPEC.md), code, tests and captured diff.
No open document findings; code-review findings have not yet been issued.
S1 is not accepted. No commit, push, version change or release was performed.

The engine checks current remaining stock before any deduction, rejects the entire
insufficient order, and continues. Tests cover both APIs, partial-deduction risk,
sequential depletion, exact-stock success, empty orders/batches, integer counts,
ordered boolean outcomes, copied stock and nested input preservation. Validation
cases verify that an invalid later order prevents the engine from being invoked.
README describes usage; SPEC and design/plan status reflect the implementation.
The decoder and installed gate are unchanged.

## Candidate and review history

Candidate: base `430e602e3a01959b9eb5b72ddc40680604df0f84` plus
[captured diff](s1-candidate.patch) and [SHA-256 manifest](s1-snapshot.json).
The diff includes pre-existing planning edits as well as this implementation;
the manifest identifies code, documents, gate and new evidence files exactly.
This stage record and the manifest itself are handoff metadata outside the hash set.

The [prior independent document report](design-current.json) is preserved unchanged.
Before edits, all its recorded hashes matched the fixture; verdict `ready`, no
findings. Only implementation/status documentation changed after that review;
the behavioral contract and design decision remain the reviewed ones.
Original requirements and completed S0 history are preserved.
No independent code review or human approval is claimed by this executing agent.

## Exact checks

All Python checks used the prepared runtime, with no installation or external services.

| Command | Content / result | Evidence |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v` | Before edits: exit 0, 6 baseline tests passed | Execution transcript; prior baseline also in document report |
| Same command | New tests against original engine: exit 1, 11 tests, 6 failing subtests across both APIs | [Counterexamples](s1-regression-before.txt) |
| Same command | Candidate code/tests: exit 0, all 11 tests passed | [Unittest output](s1-unittest.txt) |
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" .git/hooks/pre-commit` | Candidate code/tests: exit 0, all 11 tests passed | [Installed gate output](s1-gate.txt) |
| `/Library/Developer/CommandLineTools/usr/bin/git diff --check` | Final candidate: exit 0, no whitespace errors | [Output](s1-diff-check.txt) |

The gate makes no automatic edits. Final changes after Python checks were documentation
only. Initial system `git` calls emitted denied xcrun-cache/config warnings; the
CommandLineTools Git binary completed candidate capture and the whitespace check.
Intended files are staged for inspection only; staging does not indicate acceptance.
Final `git diff --cached --check` reported four whitespace lines in the captured
patch/raw failing-test output (exit 2); those artifacts retain their original bytes.
`/Library/Developer/CommandLineTools/usr/bin/git diff --cached --check -- README.md docs inventory.py tests/test_inventory.py`
passed (exit 0), covering all changed source, tests and product documentation.
After review, resolve supported blocking findings, rerun affected checks and the
installed gate for code changes, and preserve findings/recheck evidence before human review.
