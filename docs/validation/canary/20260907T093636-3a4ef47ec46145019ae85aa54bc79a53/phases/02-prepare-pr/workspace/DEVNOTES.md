# Contributor notes

Use the existing Python 3.10+ environment. `CANARY_PYTHON`, when supplied,
identifies the prepared interpreter. Do not create another environment or download
tools. From the repository root, run the normal gate:

```sh
"${CANARY_PYTHON:-python3}" tools/check.py
```

The gate uses unittest and reads the suite directory and intentional custom
`check_*.py` discovery pattern from [quality.ini](quality.ini). It runs the full
suite and exits nonzero for test failures or zero discovered tests. For direct
stdlib debugging, the equivalent discovery command is
`python3 -m unittest discover -s qa -p 'check_*.py' -v`; use the normal gate for
zero-test protection and coverage.

## Coverage

When the selected interpreter already provides coverage, the normal gate starts
measurement before test discovery, shows missing lines, and writes reports using
[.coveragerc](.coveragerc). That file owns the application-only `inventory` source
selection, branch measurement, and artifact paths: `artifacts/.coverage` and
`artifacts/coverage.json`. There is no required coverage percentage. Paths resolve
from the repository root, including when the gate is invoked elsewhere.

Without coverage, the gate explicitly reports the limitation and still runs the
stdlib suite with failure and empty-discovery protection. It generates no new
coverage reports in that mode; any existing reports are from an earlier run.
Do not install packages just to enable measurement. Generated artifacts are ignored
by Git; archive evidence separately before rerunning if it needs to be retained.

## Local commit hook

[hooks/pre-commit](hooks/pre-commit) is the maintained delegation entrypoint.
The local installation is its executable copy at `.git/hooks/pre-commit`, which
calls `tools/check.py` using `CANARY_PYTHON` (or `python3`). It runs the complete
suite on every invocation, including documentation-only changes, without filtering
filenames. Improvements to checks belong in the check command.

For this checkout's default hook location, restore a missing installation with:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Inspect the local repository and any custom `core.hooksPath` or existing hook
before restoring; preserve existing delegation and hooks. Exercise the installed
gate directly with `.git/hooks/pre-commit`; no commit is needed.

## Navigation

- [README](README.md) owns usage, input/output rules and user-visible limitations.
- [Development history](docs/DEVELOPMENT_HISTORY.md) preserves implementation
  rationale and the 2 September session record, not current verification.
- [AGENTS](AGENTS.md) defines scope and conventions for coding agents.
