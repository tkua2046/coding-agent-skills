# PR preparation validation — 7 September 2026

Current local checks passed. Maintainer human review remains pending. The tested
candidate is the setup working tree against baseline `771887e`: modified
`README.md`, `DEVNOTES.md`, `tools/check.py`, plus new
`docs/development-history.md` and `docs/workflow-verification.md`. The index was
empty. This handoff adds the PR draft and this validation record only, alongside
ignored validation artifacts.

Checks below were executed during this handoff at 09:24 UTC using
`CANARY_PYTHON`, with already installed coverage 7.16.0 and workspace-local
`TMPDIR=$PWD/.tmp`. No packages were installed.

| Command | Current result |
|---|---|
| `"$CANARY_PYTHON" tools/check.py` | Exit 0; all 5 tests passed; coverage data and JSON written |
| `.git/hooks/pre-commit README.md` | Exit 0; all 5 tests passed; coverage data and JSON written |
| `"$CANARY_PYTHON" -S tools/check.py` | Exit 0; all 5 tests passed; explicit coverage-unavailable notice |

The actual installed hook was executable and byte-identical to `hooks/pre-commit`.
Its direct invocation exercises full-suite delegation for a documentation filename
without making a commit. Both coverage-enabled runs measured `inventory.py` with
58 statements, one missing statement, 18 branches and two partial branches,
displaying 96%; missing output was `59->exit, 81`. There is no percentage threshold.
`-S` simulates unavailable site packages; it does not uninstall coverage and does
not produce fresh coverage reports.

[Raw current evidence](../../artifacts/pr-validation-20260907-092440/) contains
command output, separate coverage snapshots and `results.json` with interpreter
details, exit statuses and SHA-256 fingerprints of tested inputs and prior
evidence. Existing top-level coverage reports were archived there before running
checks. Hash comparisons confirmed the inspected setup files, application,
configuration, hooks and prior verification artifacts were unchanged afterward.
These ignored artifacts accompany this local checkout only.

[Prior setup verification](../workflow-verification.md) and its archived reports
were preserved. Its intentional failure and zero-test probes are historical
results, not checks rerun here. The 2 September session in
[development history](../development-history.md) is also historical.

Git inspection emitted sandbox cache/config warnings but returned the diff and
status successfully. No CI, external integration, actual commit, release check or
human review occurred. The next action is the maintainer's review of the setup
candidate and evidence linked from [the PR draft](PR.md).
