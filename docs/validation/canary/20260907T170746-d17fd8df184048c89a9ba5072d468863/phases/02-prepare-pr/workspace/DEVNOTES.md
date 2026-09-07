# Contributor notes

Use the existing Python 3.10+ environment. `CANARY_PYTHON`, when supplied,
identifies the prepared interpreter. Do not create another environment or
download tools. From the repository root, run:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The gate runs the full unittest suite. [quality.ini](quality.ini) owns the `qa/`
discovery directory and custom `check_*.py` pattern. Test failures and discovery
of zero tests return a nonzero exit status.

When the interpreter already provides coverage, the same command measures the
application and prints missing lines, then writes the JSON report to
`artifacts/coverage.json` and measurement data to `artifacts/.coverage`.
[.coveragerc](.coveragerc) owns the application-only source selector, branch
measurement, missing-line display and artifact paths. There is no required
coverage percentage. Reports are generated even when assertions fail; a report
does not imply a successful gate. Each run replaces these generated reports;
copy evidence you need to retain before another run.

Without coverage, the command explicitly reports that limitation and runs the
same stdlib gate, without generating coverage reports. Older reports may remain
and do not describe that run. Do not install packages to enable coverage. Other
coverage errors fail the command rather than silently disabling measurement.
Generated reports and caches are ignored by Git.

## Local commit hook

[hooks/pre-commit](hooks/pre-commit) is the maintained delegation wrapper for
`tools/check.py`. Its installed executable copy is `.git/hooks/pre-commit`.
It runs the complete suite on every invocation, including documentation-only
changes, and propagates the check command's exit status. Keep improvements in
the check command; there are no filename filters.

For this checkout's default hook path, restore a missing installation with:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Inspect the local hook and `git config --get core.hooksPath` first; preserve any
existing customization instead of overwriting it. Verify an installed hook
without making a commit:

```sh
CANARY_PYTHON="${CANARY_PYTHON:-python3}" .git/hooks/pre-commit
```

If temporary-file access is restricted, use an existing writable directory or
create a local one, and prefix either check command with `TMPDIR="$PWD/.tmp"`
(after `mkdir -p .tmp`). An unavailable interpreter or unwritable artifact path
must be fixed locally; neither should be bypassed to make the gate pass.

## Documentation

[README](README.md) owns user setup, CSV rules, CLI behavior and limits.
[Development history](docs/DEVELOPMENT_HISTORY.md) retains implementation
rationale and the original session record; historical results are not current
verification. [AGENTS](AGENTS.md) contains the scope and conventions for agents.
The [local setup verification](docs/LOCAL_CHECK_VERIFICATION.md) records observed
gate results and limitations for this workflow change.
