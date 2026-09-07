# Contributor notes

Use the existing Python environment. `CANARY_PYTHON`, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.

## Checks and coverage

From the repository root, run:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The full unittest suite uses the directory and custom pattern in
[quality.ini](quality.ini). Zero discovered tests and test failures fail the gate.
The intentional custom discovery predates tools/check.py; the earlier direct
command was `python3 -m unittest discover -s qa -p 'check_*.py' -v`.
Use tools/check.py as the maintained entrypoint.

When that interpreter already provides coverage, the normal command measures the
suite and prints coverage with missing lines, then writes the JSON report.
[.coveragerc](.coveragerc) owns the application-only source selection, branch
measurement and artifact paths (`artifacts/.coverage` and
`artifacts/coverage.json`). There is no required coverage percentage. Each run
refreshes these generated files; archive reports before rerunning when retaining
evidence. If coverage is unavailable, the command explicitly reports that limit
and runs the same stdlib gate without coverage reports. No packages are installed.

## Local commit hook

[hooks/pre-commit](hooks/pre-commit) delegates to tools/check.py and runs the full
suite for every invocation, including documentation-only changes. The installed
local copy uses the same prepared interpreter. To restore a missing installation
in this checkout:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Verify it without creating a commit:

```sh
.git/hooks/pre-commit
```

In a sandbox that disallows system temporary directories, provide a writable local
one for either command, for example `mkdir -p .tmp` followed by
`TMPDIR="$PWD/.tmp" .git/hooks/pre-commit`.

## Background and evidence

User usage and the CSV/JSON contract live in [README](README.md).
[Development history](docs/development-history.md) preserves implementation
rationale and the 2 September session record; it is not current verification.
Current setup validation is recorded in
[the local workflow verification](docs/workflow-verification-20260907.md).
Detailed run output belongs under artifacts; retain separate evidence for failed
and successful runs instead of overwriting earlier evidence.
