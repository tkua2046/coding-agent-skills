# Contributor notes

Use the existing Python 3.10+ environment. CANARY_PYTHON, when supplied, identifies
the prepared interpreter. Do not create another environment or download tools.
From the repository root, run:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The normal check discovers the full unittest suite using [quality.ini](quality.ini).
The `qa/` directory and custom `check_*.py` pattern are intentional. Failed tests,
import errors and zero discovered tests fail the gate.

When the interpreter already provides coverage, the check measures before test
discovery and, on success, displays missing lines and writes the JSON report.
[.coveragerc](.coveragerc) owns the application-only source selector, branch
measurement, report options and artifact paths (`artifacts/.coverage` and
`artifacts/coverage.json`). There is no required coverage percentage. Paths resolve
from the repository root. Coverage or report errors fail the check; only an absent
coverage package falls back to the stdlib gate, with an explicit limitation message.
That fallback still checks the entire suite but produces no coverage reports.
Reports from earlier runs are not evidence for a failed or fallback run. Archive
reports you need to retain before another run replaces them.

## Local commit gate

The repository's local hook is copied from [hooks/pre-commit](hooks/pre-commit) into
`.git/hooks/pre-commit` and marked executable during checkout setup. It delegates
to the normal check command using the same interpreter selection. Keep this scheme;
check improvements belong in tools/check.py. The full suite runs unconditionally,
including for documentation-only edits, and failures propagate to the hook exit.

To restore a missing installation in this checkout (preserve any existing hook or
custom hooks path):

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Invoke `.git/hooks/pre-commit` directly to verify the installed gate; no commit is
needed. No package installation is required.

## Navigation

- [README](README.md): application usage and CSV/JSON contract.
- [Development history](docs/DEVELOPMENT_HISTORY.md): implementation rationale and
  the original September 2 session record, not current verification.
- [Local setup verification](docs/validation/2026-09-07-local-setup.md): exercised
  commands, outcomes and limitations for this workflow change.
- [AGENTS](AGENTS.md): agent scope and repository conventions.
