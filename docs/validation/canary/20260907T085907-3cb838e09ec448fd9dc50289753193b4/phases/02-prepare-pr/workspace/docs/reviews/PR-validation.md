# Local PR validation — 2026-09-07

Current local checks passed; maintainer human review remains pending. Candidate:
working-tree setup changes against baseline `b74666a` in `README.md`, `DEVNOTES.md`,
`tools/check.py`, and new `docs/development-history.md`. No setup files were edited
during this handoff. The only additions are the PR draft and validation evidence.

## Checks run during this handoff

Used the supplied `CANARY_PYTHON` (Python 3.12.4), with `TMPDIR` pointing to the
checkout's `.tmp/`. No packages were installed.

| Command | Result |
| --- | --- |
| `"$CANARY_PYTHON" tools/check.py` | Exit 0; all 5 tests passed; coverage generated |
| `.git/hooks/pre-commit` with `CANARY_PYTHON` inherited | Exit 0; all 5 tests passed; coverage generated |
| `"$CANARY_PYTHON" -S tools/check.py` | Exit 0; all 5 tests passed; explicit coverage-unavailable message |
| `git diff --check` | Exit 0; no whitespace findings; system Git emitted sandbox cache-access diagnostics |

The installed hook is executable and byte-identical to `hooks/pre-commit`; local
Git configuration has no `core.hooksPath` override. Both coverage runs report
57/58 statements and 16/18 branches covered (96% combined); missing output is
`59->exit, 81`. Coverage is limited to the application module and has no threshold.
The `-S` check suppresses site packages in the prepared runtime to exercise the
fallback; it does not establish compatibility with another Python installation.

[Current summary and candidate SHA-256 fingerprints](../../artifacts/pr-validation-20260907T090226Z/summary.json)
record exact commands, exits, runtime and unchanged candidate hashes. Adjacent
`normal.txt`, `installed-hook.txt`, `stdlib-fallback.txt` and `diff-check.txt` retain
outputs; each coverage-enabled run has its own JSON snapshot. Existing top-level
coverage files were copied there as `prior-coverage.json` and `prior-.coverage`
before the normal checks refreshed them.

## Retained evidence, not current verification

[Prior setup summary](../../artifacts/workflow-verification-20260907-020113/summary.json)
and its adjacent logs record normal/hook success, stdlib fallback, and intentional
test-failure and empty-discovery probes exiting 1 with and without coverage.
Those negative probes were not rerun during this handoff. That directory is
preserved unchanged. The [September 2 record](../development-history.md) is older
historical evidence, not a current check result.

Raw artifacts are ignored by Git and available only in this local checkout.
No remote CI, release validation or human review is claimed. Next action is the
maintainer's review of the setup changes and this evidence.
