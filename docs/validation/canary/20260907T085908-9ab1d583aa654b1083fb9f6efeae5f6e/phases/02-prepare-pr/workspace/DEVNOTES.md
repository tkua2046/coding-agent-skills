# Contributor notes

Use the existing Python environment. CANARY_PYTHON, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.
Run `"${CANARY_PYTHON:-python3}" tools/check.py` from the repository root.
The suite location and discovery pattern are configured in quality.ini.

Test failures, discovery errors and zero discovered tests fail the gate. Keep
unittest, qa/ and the intentional custom discovery pattern in quality.ini.

When the interpreter already provides coverage, the normal command starts
measurement before discovery imports the application, prints missing lines, and
writes coverage data and JSON. [.coveragerc](.coveragerc) owns the application-only
source, branch measurement and artifact paths (`artifacts/.coverage` and
`artifacts/coverage.json`). There is no required coverage percentage. Each covered
run replaces these generated reports; archive evidence separately before rerunning
if it must be retained. Generated artifacts and Python caches are ignored.

Without coverage, the command explicitly states the limitation and still runs
the stdlib gate, including its failure and empty-discovery checks. It produces no
new coverage reports; existing reports are from an earlier run. Do not install
packages to enable coverage for this setup.

## Local commit hook

The maintained wrapper [hooks/pre-commit](hooks/pre-commit) delegates to
`tools/check.py` using the same interpreter selection as above. The installed
`.git/hooks/pre-commit` runs the full suite on every invocation, including
documentation-only changes; there are no filename filters. Improvements belong
in the check command; keep this delegation scheme.

To restore a missing installation, verify the repository with
`git rev-parse --show-toplevel` and check `git config --get core.hooksPath`.
Preserve existing hooks and custom hook paths. For this repository with its
default hook directory and no conflicting installation:

```sh
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
.git/hooks/pre-commit
```

The final command exercises the installed gate without creating a commit.
No commits, tags, pushes, releases or external actions are part of local setup.

## Document navigation

[README](README.md) owns user-facing usage and the CSV/JSON contract.
[Development history](docs/DEVELOPMENT_HISTORY.md) preserves implementation
rationale and the original 2 September session record, explicitly historical.
[Local workflow verification](docs/reviews/local-workflow-2026-09-07.md) records
this setup task's actual checks and limitations.
