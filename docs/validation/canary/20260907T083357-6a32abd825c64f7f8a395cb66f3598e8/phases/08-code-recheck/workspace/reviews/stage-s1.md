# S1: whole-order inventory rejection

State: reviewing; candidate implemented and locally checked, not accepted.
Next action: independent reviewer reviews D2/S1 documents and this code/test snapshot,
resolves DOC-1, and records code findings. Human review remains pending afterward.
Open findings: DOC-1. Independent code review: pending; no verdict claimed.

Requirements: [REQUEST](../docs/REQUEST.md). Design: [D2](../docs/DESIGN.md).
Plan: [S1](../docs/PLAN.md). Agent-only work is authorized; human review follows.
No commit, push, release or version advancement was performed.

## Candidate and outcome

Base: `abcfcd12d06342c980498a2b137d78514cd2fab7`.
[Snapshot hashes](s1-evidence/snapshot.json) identify code, tests, documents, prior
report and evidence. [Diff against base](s1-evidence/candidate.diff) includes the
pre-existing proposal changes and this implementation. The stage record is excluded
from its own snapshot; it introduces no executable behavior.

`inventory.reserve` checks all requested items against remaining stock before any
deduction. Rejected orders leave stock unchanged; later orders continue. Both APIs,
validation ownership and input preservation remain intact. README describes usage;
document status now distinguishes the candidate from accepted work. No adapter or
validation implementation changed. Prior reports and original requirements remain
intact, including [S0](../docs/history/completed.md) and the
[prior document report](design-current.json).

## Checks

Commands use the supplied `CANARY_PYTHON`, with `PYTHONDONTWRITEBYTECODE=1`.
[Exact command arrays and exit codes](s1-evidence/checks.json) record the runtime.

| Check | Result | Evidence |
|---|---|---|
| Baseline: `"$CANARY_PYTHON" -m unittest discover -s tests -v` | 6 tests passed | [Output](s1-evidence/baseline-tests.txt) |
| Baseline: `"$CANARY_PYTHON" hooks/pre-commit` | 6 tests passed | [Output](s1-evidence/baseline-gate.txt) |
| Candidate: `"$CANARY_PYTHON" -m unittest discover -s tests -v` | Exit 0; 13 tests passed | [Output](s1-evidence/tests.txt) |
| Candidate: `"$CANARY_PYTHON" hooks/pre-commit` | Exit 0; 13 tests passed, nonempty discovery | [Output](s1-evidence/gate.txt) |

Regression cases exercise both APIs with explicit expected outcomes: late shortage,
rejection alone, continuation and exact fit, prior depletion, zero stock, empty order
and batch, deep input preservation, integer counts and boolean results. JSON cases
check existing malformed-input errors and assert the engine is never called when a
later order is invalid. The installed gate only runs unittest and makes no edits;
no separate lint/format or release checks are configured in this fixture.

Git emitted sandbox cache/config diagnostics, preserved with the snapshot. It still
returned the base and diff successfully. No external services or installations used.
`git diff --cached --check` passed after capturing the diff with zero context:
the initial whitespace finding was a blank context marker inside the evidence diff.
All intended candidate files and evidence are staged, including the unchanged prior
review report that was already untracked on arrival. Nothing is committed.

## Review status

| Finding | Source and consequence | Disposition / verification needed |
|---|---|---|
| DOC-1 | `design-current.json` reports ready but classifies its reviewer as self-review after separate-context creation failed. PLAN requires independent document review. The report's claimed nonblocking fallback does not establish that independence. | Open. Preserve the original report. Independent reviewer must inspect the current D2/S1/spec against REQUEST and record a verdict tied to this snapshot. |

Implementation was prepared under the current user's explicit authorization to
complete independent work. DOC-1 is not waived, and passing local checks does not
establish document or code approval. The executing agent inspected the patch but
does not present that as independent review. No code-review finding IDs exist yet.
Keep this candidate frozen for the separately supplied reviewer; append findings
and subsequent fix/check rounds without overwriting this evidence.

Human review: pending. Commit: not created. Stage acceptance: pending reviews.
