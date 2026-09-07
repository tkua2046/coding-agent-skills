# Contributor notes

Use the existing Python environment. CANARY_PYTHON, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.
Run `"${CANARY_PYTHON:-python3}" tools/check.py` from the repository root.
The suite location and discovery pattern are configured in quality.ini.
The intentional `qa/` / `check_*.py` discovery convention predates tools/check.py.
The gate runs all unittest tests and fails for test failures or zero discovered
tests. The historical direct command was
`python3 -m unittest discover -s qa -p 'check_*.py' -v`; use tools/check.py for the
normal gate, including its empty-suite protection and coverage reporting.

When the selected interpreter already provides coverage, the normal command
automatically measures coverage using [.coveragerc](.coveragerc). That file owns
the application-only source selection, branch measurement, missing-line display,
and artifact paths (`artifacts/.coverage` and `artifacts/coverage.json`). There is
no required coverage percentage. Without coverage, the command states that
reports are unavailable and still runs the stdlib unittest gate. Do not install
packages to enable coverage. Generated artifacts and Python caches are ignored.

The repository's local hook is copied from hooks/pre-commit into
.git/hooks/pre-commit and marked executable during checkout setup. It delegates
to tools/check.py, so improvements belong in the check command. Keep this scheme.
If restoring a missing local installation, copy that wrapper and chmod it locally.
No commit is needed to invoke .git/hooks/pre-commit and verify the gate.
The hook runs the complete suite even for documentation-only changes; it does
not select tests based on filenames. Invoke it with
`CANARY_PYTHON="${CANARY_PYTHON:-python3}" .git/hooks/pre-commit`.

If a restricted environment denies access to the system temporary directory,
create a local `.tmp/` and prefix the check or hook command with
`TMPDIR="$PWD/.tmp"`. This lets the existing tests use a writable temporary
directory without changing their behavior.

[README](README.md) owns user usage and the CSV/JSON contract.
[Development history](docs/development-history.md) preserves the implementation
notes and the 2 September session record; it is not current verification.
