# S1 implementation handoff

State: implemented; independent code review and human review pending. No open
document findings: the prior [document review](design-current.json) is ready, and
every recorded SHA-256 matched at intake. No code-review verdict is claimed.
Next action: the user-designated independent agent reviews this candidate against
[REQUEST](../docs/REQUEST.md), [D2](../docs/DESIGN.md), and [S1](../docs/PLAN.md),
records findings separately, then supported fixes receive checks and re-review.
Human acceptance remains pending afterward; S1 is not yet accepted.

The engine now prechecks every order before deductions, rejects shortages without
partial changes, and continues in order. Both APIs, validation and caller inputs
are preserved. README explains usage; SPEC owns current behavior. Design/plan
status and links were updated without changing the reviewed D2 behavior. Original
requirements, S0 history, supplied skills and prior review remain unchanged.

Candidate: base `934b68b9c49f4e46e24743f4541359017dd8d0e3` plus
[captured diff](s1-candidate.patch) and [content hashes](s1-candidate.json).
Manifest SHA-256: `91fadf1b5a954574e78ec8e575dd76c8a30ba67b51d2fa1a542fe8648e66aa52`.
The diff includes D2/plan edits already present at intake; the manifest identifies
the full current content, prior report and new evidence. Handoff/manifest are
excluded from their own content hashes. Implementation edits are frozen for review.

Checks on 2026-09-07 using the prepared runtime (no packages or external services):

| Check | Result | Evidence |
| --- | --- | --- |
| Intake `"$CANARY_PYTHON" -m unittest discover -s tests -v` | Exit 0; 6 baseline tests | Consistent with preserved [baseline](../docs/PLAN.md#verified-baseline) |
| Candidate `"$CANARY_PYTHON" -m unittest discover -s tests -v` | Exit 0; 8 tests | [Raw output and resolved command](s1-tests.log) |
| Candidate `"$CANARY_PYTHON" hooks/pre-commit` | Exit 0; 8 tests; installed full gate | [Raw output and resolved command](s1-gate.log) |
| New decisive test with `HEAD:inventory.py` loaded in memory | Expected failure: 8 failed prefix/API subtests, no errors | [Counterexample output and method](s1-counterexample.log) |
| `git diff --cached --check` and staged-content inspection | Exit 0; intended files staged; no hook changes | Final handoff verification |

The decisive regression checks every prefix through both APIs, including earlier
success, later-item shortage, continuation, exact depletion, empty order/batch,
exhausted stock, nested input preservation, copied stock, and integer/boolean
types. Invalid JSON tests include valid prefixes followed by invalid orders and
verify reservation is never called. The existing success tests remain.
The initial whitespace check flagged a blank patch context line and trailing
space in unittest output. The patch was recaptured with `--unified=0`, and
trailing whitespace was trimmed from the counterexample log; no result changed.
The counterexample used an isolated Python process and did not alter working files.
No product/test changes followed passing tests or gate; later edits only clarified
document status and added review evidence. The gate does not modify files, and no
separate lint/format command is configured by this fixture.

Git emitted sandbox warnings about the platform cache/global ignore file, but
the required Git operations succeeded. No commit, push, version change or release
was made. The staged snapshot is provided for review, not approval or acceptance.
