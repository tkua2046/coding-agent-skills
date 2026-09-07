# Contributor notes

Use the existing Python environment. CANARY_PYTHON, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.

## Checks and coverage

From the repository root, run:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The command runs the full unittest suite, with discovery owned by
[quality.ini](quality.ini). Test failures and zero discovered tests fail the gate.
When the interpreter already provides coverage, measurement starts before discovery
and uses [.coveragerc](.coveragerc): inventory only, including branches, with missing
lines printed and JSON written to `artifacts/coverage.json`. Measurement data goes
to `artifacts/.coverage`. There is no required coverage percentage.
Without coverage, the command explicitly reports the limitation and runs the same
stdlib unittest gate; it cannot produce fresh coverage reports. Existing reports
may be stale. No packages are installed by the check command.

Generated artifacts are ignored. Normal coverage runs replace their configured
reports; copy any evidence that must be retained to a distinct location first.
If the environment restricts system temporary directories, create `.tmp/` locally
and set `TMPDIR="$PWD/.tmp"` when running checks.

## Local commit hook

[hooks/pre-commit](hooks/pre-commit) delegates to tools/check.py and always runs
the full suite, including for documentation-only changes. Keep this delegation;
check improvements belong in tools/check.py.

For this checkout's default hook location, install or restore the wrapper with:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Inspect existing hooks and `git config --get core.hooksPath` first; preserve any
custom hook path or unrelated hook logic. The hook uses CANARY_PYTHON when supplied,
otherwise python3; set that variable when the prepared runtime is required.
Invoke `.git/hooks/pre-commit` directly to verify the installed gate without a commit.

## Navigation

- [README](README.md): user setup, CSV contract and CLI behavior.
- [Development history](docs/development-history.md): implementation rationale and
  the original September 2 session record, not current verification.
- [AGENTS](AGENTS.md): agent scope and repository conventions.
