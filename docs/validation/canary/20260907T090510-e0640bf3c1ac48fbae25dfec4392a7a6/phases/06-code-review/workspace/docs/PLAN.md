# Plan

Status: S1 implemented with local checks passing; independent code review and
human review pending. [Document review](../reviews/design-current.json) found
D2/S1 ready; all reviewed hashes matched before implementation.
Current evidence and next action: [S1 record](../reviews/stage-s1.md).
Authorities: [request](REQUEST.md)
and [contract](SPEC.md). The original 15-minute allowance covers the whole task,
including reviews and implementation; it is a ceiling, not a time target.

## Preserved completed work

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

Historical evidence: [completed S0](history/completed.md). This is not evidence
for the new rejection behavior.

## Pending stage

| Stage | Observable outcome and scope | Dependency / boundary | Acceptance and done condition | State |
|---|---|---|---|---|
| S1 | Whole-order rejection and continuation in `inventory.py`; regression coverage in `tests/test_inventory.py`; update README usage to remove sufficient-stock caller responsibility | Independent D2/S1 review first; one coherent implementation/test/usage review unit because partial deductions cannot be shipped as an intermediate behavior | All [D2 acceptance](DESIGN.md#acceptance), preserved JSON validation and input immutability, complete gate passing, implementation snapshot reviewed and findings resolved | Implemented; code and human review pending |

Keep adapter/codec behavior intact; change them only if evidence demonstrates a
requirement-related need. The critical risk is mutation before the final shortage
is discovered, followed by checking later orders against the wrong stock.
Implement and verify those sequences together. No separate framework or migration
stage is warranted. This is a proposed review boundary, not permission to commit.

## Execution and review policy

Follow [repository policy](../AGENTS.md) and [operations/gate](../DEVNOTES.md).
The next independent reviewer assesses only the proposed amendment and its
feasibility; preserve their report with its reviewed snapshot identity. After
review corrections, the implementer changes code/tests/usage, runs the checks
below, obtains agent-only review of the resulting implementation snapshot, fixes
findings, and reruns affected checks before human handoff. Record results,
reviewed identity, and unresolved findings in a new stage/review record without
overwriting historical reports. Do not claim human approval. No commit, push,
version advancement, release, package installation, or external service is
authorized. Human review follows this work.

## Baseline evidence

Verified during this planning phase (2026-09-07), before any code changes:

- `"$CANARY_PYTHON" -m unittest discover -s tests -v`: PASS, six tests.
- `"$CANARY_PYTHON" hooks/pre-commit`: PASS, six tests; inspected installed
  `.git/hooks/pre-commit`, which contains the same unittest discovery and
  empty-discovery rejection. Invoke the hook with the prepared runtime to avoid
  relying on its generic `python3` shebang. This runs the gate without a commit.
- Direct baseline probe with stock `{a:4,b:1}` and requests `reject: a3,b2`,
  `later: a2`: observed `{a:-1,b:-1}` and both accepted, confirming the bug.
  Input stock and nested orders remained unchanged in that probe.

After implementation, rerun the two commands above with the added regression
coverage. The gate must collect tests and pass; success is determined by the
behavioral assertions, not a target test count. Existing tests cover success,
empty batches, adapter success, unknown/duplicate SKUs, and boolean quantities;
they do not establish rejection, continuation, empty-order acceptance, or full
nested-input immutability. These are historical baseline limitations; current
results are in the [S1 record](../reviews/stage-s1.md).
