# Local workflow verification — 7 September 2026

The normal check now uses installed coverage when available. Application code,
CLI, examples, application tests, quality.ini, .coveragerc and both hook wrappers
were unchanged. No packages or environment were installed or replaced.

The prepared CANARY_PYTHON provided coverage 7.16.0. Checks used a workspace-local
TMPDIR because the sandbox restricts system temporary directories.

| Execution | Observed result |
| --- | --- |
| Baseline: prepared Python, tools/check.py | 5 tests, OK, exit 0 |
| Updated tools/check.py | 5 tests, OK, exit 0; coverage report and JSON |
| Installed .git/hooks/pre-commit | 5 tests, OK, exit 0; coverage report and JSON |
| Installed hook with only README staged in a temporary alternate index | Full 5 tests, OK, exit 0 |
| Installed hook with temporary failing test | 6 tests, one failure, exit 1 |
| Installed hook with temporary unmatched discovery pattern | No tests discovered, exit 1 |
| Installed hook using prepared Python with -S to hide site packages | Coverage-unavailable notice; 5 tests, OK, exit 0 |
| Same stdlib hook with failing test / unmatched pattern | Both exit 1 with the expected failure / no-tests message |

Coverage reported 96%, missing line 81 and branch 59->exit. The JSON at
artifacts/coverage.json was checked for inventory.py as its only measured file,
branch coverage enabled and missing line 81. No percentage threshold was added.
The maintained and installed hook copies were byte-identical and executable;
the existing local installation needed no replacement.

Temporary tests, discovery edits, interpreter wrapper and alternate index were
removed or restored in finally blocks. Successful coverage reports were restored
after negative probes. The real Git index was not used for temporary staging.
There were no prior artifacts in this checkout to overwrite. Historical README
records were preserved in docs/DEVELOPMENT_HISTORY.md.

Limits: without coverage the gate checks tests only and does not refresh reports.
System Git emitted sandbox warnings about its system cache and global ignore
file; the local Git operations used for inspection and temporary staging still
succeeded. No external integration, commit, tag or push was performed.

Document ownership: README contains user usage; DEVNOTES owns contributor
operations; docs/DESIGN.md records implementation choices; development history
retains the earlier checkpoint. No additional setup action is pending.
