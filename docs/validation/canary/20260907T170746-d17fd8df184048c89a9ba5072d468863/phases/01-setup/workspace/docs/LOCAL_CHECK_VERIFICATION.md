# Local workflow verification — 7 September 2026

The existing baseline passed all five application tests using
`TMPDIR="$PWD/.tmp" "$CANARY_PYTHON" tools/check.py` before edits.
The prepared runtime supplied coverage 7.16.0; no packages were installed.

After the workflow edit, the normal command and existing executable
`.git/hooks/pre-commit` passed all five tests. The installed wrapper was identical
to `hooks/pre-commit`, with no configured `core.hooksPath` override; it was reused.
`git hook run pre-commit` also passed all five tests with only README staged in a
temporary index. No commit was made and the real index was unchanged.

| Probe | Observed result |
|---|---|
| Normal command; installed hook with documentation-only staging | Exit 0, five tests, missing-line coverage output |
| Temporary failing test, normal command and installed hook | Exit 1, six tests, one assertion failure |
| Temporary discovery pattern matching no tests, normal command and installed hook | Exit 1, explicit no-tests diagnostic |
| Installed hook using prepared Python with `-S` to hide coverage | Exit 0, five tests, explicit coverage-unavailable diagnostic |
| Same stdlib hook with failing test / empty discovery | Exit 1 in each case, corresponding diagnostics |
| Installed hook after restoration | Exit 0, five tests, coverage output |

The JSON report at `artifacts/coverage.json` was parsed and checked to contain
only `inventory.py`, with branch coverage enabled and missing line 81. Coverage
displayed 96% (57/58 statements and 16/18 branches covered); no percentage
threshold was added. The fallback left existing reports unchanged and generated
no new coverage evidence. Empty discovery produced coverage no-data warnings
and a `NoDataError` after the explicit discovery failure; it remained a failing
gate and did not produce a fresh JSON report.

Per-case commands, observed output, asserted exit statuses and a passing JSON
snapshot are retained locally under
[artifacts/workflow-verification-8ccog4se](../artifacts/workflow-verification-8ccog4se/).
That ignored directory preserves probe failures separately from the final passing
report. Existing historical records were retained.

Temporary test, discovery changes, interpreter shim and alternate index were
removed or restored in cleanup. Byte comparisons confirmed the application,
sample data, original application tests, discovery and coverage configuration,
both hook copies, Git configuration and real index remained unchanged.
`git diff --check` passed. No dependencies, environment replacements, commits,
tags, pushes or external actions were performed.

Verification used a writable repository-local `TMPDIR` because system temporary
paths are restricted. The system Git launcher emitted cache-access warnings;
subsequent checks used the installed Command Line Tools Git binary directly.
Git also warned about inaccessible user ignore settings; the checked commands
still succeeded. Coverage absence was simulated with `-S`, not by uninstalling
anything. Coverage reports describe only the configured application and current
suite; no external integration was exercised. Current operations live in
[DEVNOTES](../DEVNOTES.md).
