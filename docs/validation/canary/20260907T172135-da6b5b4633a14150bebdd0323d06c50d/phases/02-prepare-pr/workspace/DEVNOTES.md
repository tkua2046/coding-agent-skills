# Contributor notes

Use the existing Python environment. CANARY_PYTHON, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.
Run the normal check from the repository root:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The full unittest suite uses the directory and discovery pattern in quality.ini.
Test failures and zero discovered tests fail the gate. Keep the custom discovery
configuration and the existing application tests.

When the interpreter provides coverage, the same command measures the application
with .coveragerc: inventory only, branch coverage, missing lines in the terminal,
coverage data in artifacts/.coverage and JSON in artifacts/coverage.json. There
is no percentage threshold. Coverage starts before test discovery imports the
application. Reporting errors also fail the command. Without coverage, the command
states the limitation and runs the stdlib unittest gate; it generates no fresh
coverage reports, so any existing reports may be stale. Do not install packages
just to enable coverage.

The local hook is an executable copy of hooks/pre-commit at .git/hooks/pre-commit.
It delegates to tools/check.py and always runs the full suite, including for
changes only to documentation. Keep this delegation; check improvements belong
in tools/check.py. To restore a missing installation in this checkout:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Preserve any existing custom hook or hooks path before changing an installation.
Invoke `.git/hooks/pre-commit` directly to verify the installed gate; no commit is
needed. It uses CANARY_PYTHON when supplied, otherwise python3.

Tests need a writable temporary directory. In a restricted checkout, use
`mkdir -p .tmp` and prefix the check or hook invocation with `TMPDIR="$PWD/.tmp"`.
Generated reports and scratch files are ignored by Git.

See [README](README.md) for usage, [implementation notes](docs/DESIGN.md) for
exporter choices, and [development history](docs/DEVELOPMENT_HISTORY.md) for the
preserved September checkpoint and session record.
