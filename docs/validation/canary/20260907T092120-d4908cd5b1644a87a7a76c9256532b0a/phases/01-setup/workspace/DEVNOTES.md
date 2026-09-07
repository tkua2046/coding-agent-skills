# Contributor notes

Use the existing Python environment. `CANARY_PYTHON`, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.

## Checks and coverage

From the repository root, run:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

This is the normal check command and the hook's gate. It runs the complete
unittest suite, including for documentation-only edits, and fails on test failures
or zero discovered tests. `quality.ini` owns the suite directory and custom
filename pattern; retain `qa/` and that configuration.

When the interpreter already provides coverage, the command measures tests from
before discovery, prints coverage with missing lines, and writes coverage data
and JSON to the paths in [.coveragerc](.coveragerc). That file owns application-only
source selection, branch measurement and report settings. There is no required
coverage percentage. Coverage/reporting errors fail the command. If coverage is
unavailable, the same unittest gate runs with an explicit notice; it generates no
coverage reports. Existing reports then describe earlier runs, not the latest gate.
Do not install packages to enable coverage.

Generated reports live in ignored `artifacts/`. Archive reports needed as evidence
before another run replaces them. Keep durable development records under `docs/`.
In a restricted workspace, set `TMPDIR` to an existing writable local directory
(e.g. `mkdir -p .tmp` and `export TMPDIR="$PWD/.tmp"`) for the suite's temporary files.

## Local hook

The repository's local hook is copied from [hooks/pre-commit](hooks/pre-commit)
into `.git/hooks/pre-commit` and marked executable during checkout setup. It
chooses `${CANARY_PYTHON:-python3}` and delegates to `tools/check.py`; improvements
belong in that command. It does not filter changed filenames.

To restore a missing installation, first check `git config --get core.hooksPath`
and preserve any existing hook or custom hook path. For this checkout's default
hook location:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
.git/hooks/pre-commit
```

Invoke the installed hook directly to verify the gate without creating a commit.

## Project records

- [README](README.md) owns user setup, CSV requirements and CLI behavior.
- [Development history](docs/development-history.md) preserves implementation
  rationale and the 2 September checkpoint and session record.
- [Local workflow verification](docs/workflow-verification.md) records this setup's
  exercised checks and limitations.
- [AGENTS](AGENTS.md) contains agent scope and repository conventions.
