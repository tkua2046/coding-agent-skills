# S1: whole-order inventory reservation

State: reviewing; implementation complete, stage acceptance pending.
Review policy: agent-only work authorized; independent code review and human review pending.
Requirements/design: [REQUEST](../docs/REQUEST.md), [SPEC](../docs/SPEC.md),
[D2 / S1](../docs/PLAN.md). Scope: reservation, regression tests, usage and progress documentation.

## At a glance

Orders with any shortage now return `accepted=False` without deducting stock;
later orders continue. Both APIs, validation and input preservation remain intact.
Next action: the separately assigned independent agent reviews this frozen candidate,
then findings are resolved and human review follows. No open finding IDs have been
reported; this is not a code-review verdict. Human review: pending. No commit created.

## Evidence

Candidate: base `4fe441bb260ccebf797139ceb8a2ed4bda23c06e` plus [captured diff](s1-evidence/candidate.diff.gz)
and [SHA-256 manifest](s1-evidence/candidate.json). The diff includes pre-existing
D2/S1/SPEC edits; this phase changes their status and baseline wording only.
Source, tests, usage, authorities, historical review and both hooks are identified
in the manifest. Checks below ran against this code/test content; subsequent edits
were documentation/evidence only. Hook inspection found no source changes.

| Exact command | Result | Raw evidence |
|---|---|---|
| `"$CANARY_PYTHON" -m unittest discover -s tests -v` (baseline) | PASS, 6 tests | [output](s1-evidence/baseline-tests.txt) |
| `"$CANARY_PYTHON" .git/hooks/pre-commit` (baseline) | PASS, 6 tests | [output](s1-evidence/baseline-installed-gate.txt) |
| `"$CANARY_PYTHON" -m unittest discover -s tests -v` (new tests, old engine) | Expected FAIL, 10 shortage subcases | [output](s1-evidence/regression-before-fix.txt.gz) |
| `"$CANARY_PYTHON" -m unittest discover -s tests -v` (candidate) | PASS, 8 tests | [output](s1-evidence/tests.txt) |
| `"$CANARY_PYTHON" hooks/pre-commit` (candidate) | PASS, 8 tests | [output](s1-evidence/source-gate.txt) |
| `"$CANARY_PYTHON" .git/hooks/pre-commit` (candidate, installed gate) | PASS, 8 tests | [output](s1-evidence/installed-gate.txt) |
| `/Library/Developer/CommandLineTools/usr/bin/git diff --cached --check` | PASS, exit 0 | [output](s1-evidence/staged-check.txt) |

New regression coverage exercises seven reservation scenarios through each API,
including early/late shortage, rejection alone, current remaining stock, continuation,
prior success, exact depletion, multi-item success and empty orders/batches. It checks
ordered IDs, boolean outcomes, copied stock, nested input preservation and nonnegative
integer counts. Twenty invalid JSON cases assert validation fails before the engine
is called, including an invalid order following a valid one.

## Review and current state

[Prior independent document review](design-current.json): ready, no findings.
All its recorded file hashes matched on entry ([verification](s1-evidence/document-snapshot.txt));
there was no unresolved document blocker. The original report is preserved unchanged.
Current document edits report implementation progress, without new behavior decisions.
[Historical S0](../docs/history/completed.md) and original requirements remain unchanged.

Independent code review: pending with the separately assigned reviewer; no self-review
is presented as independent approval. Full installed gate: passing. No separate lint,
format or release-only suite is configured. Human review: pending; stage not accepted.
No packages, external services, commit, push, release or version change were used.

The initial system Git launcher emitted sandbox cache warnings while returning results;
final Git checks use the installed Command Line Tools binary directly. Intended files
are staged for inspection as required by the execution skill; staging is not a commit.

Raw diff and failing-test output are gzip-compressed without changing their bytes.
The first staged whitespace check flagged spaces inside those raw artifacts
([preserved output](s1-evidence/initial-staged-check.txt.gz)); compression resolves
those artifact-only warnings. The manifest diff hash identifies the uncompressed diff.
