# S1: whole-order inventory rejection

State: implemented, awaiting independent code review. Human review: pending.
Next action: the user-assigned independent reviewer examines the candidate below
against REQUEST, SPEC, DESIGN and PLAN, records findings, and returns any required
fixes for implementation and recheck. No current document findings; code findings
have not yet been assessed. Stage acceptance remains pending. No commit created.

The engine checks every item before deducting any stock for an order. Tests cover
rejection with the short item last, later exact depletion, rejection after depletion,
empty orders/batches, ordered boolean results, integer counts, stock and nested-order
immutability through both APIs. Validation regression cases also establish that the
JSON boundary rejects an invalid batch before calling reservation. README explains
user-visible rejection. No validation policy or dependency changed.

## Candidate and review provenance

[Candidate manifest](evidence/s1-candidate.json) identifies the base commit and exact
SHA-256 file contents, including new evidence and this record.
[Captured tracked diff](evidence/s1-candidate.diff) includes pre-existing planning
changes as well as this implementation. The manifest covers new files absent from
that diff. No files were staged and no index changes were requested for this handoff.

[Independent document review](../reviews/design-current.json) reports ready, no
findings, and implementation_can_begin=true. Before edits, a Python SHA-256 comparison
of every file in its reviewed_version.files returned no mismatches (exit 0).
That review is preserved unchanged. Subsequent DESIGN/SPEC edits update status only;
PLAN adds current status above its preserved reviewed plan. These edits do not change
the agreed behavior. Prior reports and planning evidence remain intact.

## Checks

The prepared runtime was used; raw logs record its exact executable and command argv.
Baseline: `"$CANARY_PYTHON" -m unittest discover -s tests -v` passed 6 tests, exit 0
before edits, consistent with the preserved [planning baseline](evidence/planning-baseline.md).

| Check | Result | Evidence |
| --- | --- | --- |
| New suite against `git show HEAD:inventory.py`, loaded in memory into both API paths | Exit 1; 10 tests, 4 expected shortage subtest failures | [Counterexample](evidence/s1-regression-before.txt) |
| `"$CANARY_PYTHON" -m unittest discover -s tests -v` | Exit 0; all 10 tests pass | [Tests](evidence/s1-tests.txt) |
| `"$CANARY_PYTHON" hooks/pre-commit` | Exit 0; all 10 tests pass, nonempty discovery | [Installed gate](evidence/s1-gate.txt) |
| `git diff --check` | Exit 0 | [Whitespace check](evidence/s1-diff-check.txt) |

Tests and gate ran against the code/test bytes in the manifest; only documentation
and evidence changed afterward. The gate contains no rewrite operation. Git emitted
sandbox cache-path diagnostics but completed the recorded read-only operations.
Independent code review has not run in this implementation context; no approval is
inferred from local checks. Human review remains pending. No commit, push, version
change, release, package installation or external service use occurred.
