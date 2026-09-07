# Local workflow verification — 7 September 2026

Outcome: the normal gate and existing installed hook passed all five application
tests. The hook rejected a failing test and empty discovery in both coverage and
stdlib modes. Application code, CLI, sample data and the existing qa suite were
unchanged. No dependencies, environment replacement or external actions occurred.

The prepared `CANARY_PYTHON` runtime provided coverage 7.16.0. Commands used a
workspace-local `TMPDIR` because this sandbox restricts system temporary paths.
The hook was already installed and executable, and byte-identical to the maintained
wrapper; it was preserved, not reinstalled.

| Check | Command or invocation | Actual result |
|---|---|---|
| Before edits | `"$CANARY_PYTHON" tools/check.py` | 5 tests, exit 0 |
| Normal gate | `"$CANARY_PYTHON" tools/check.py` | 5 tests, exit 0, missing-line output and JSON |
| Installed hook | Absolute `.git/hooks/pre-commit README.md`, invoked from docs/ | 5 tests, exit 0, coverage reports |
| Disposable copy, coverage | Installed hook with README.md argument | 5 tests, exit 0 |
| Disposable copy, coverage | Hook with added intentional failing test | 6 tests, exit 1 |
| Disposable copy, coverage | Hook with configured unmatched discovery pattern | No tests, exit 1 |
| Disposable copy, stdlib | Hook using prepared interpreter with `-S` | 5 tests, exit 0, explicit coverage-unavailable message |
| Disposable copy, stdlib | Same hook with intentional failure | 6 tests, exit 1 |
| Disposable copy, stdlib | Same hook with unmatched pattern | No tests, exit 1 |

Coverage JSON was checked for inventory.py as its only source and branch measurement
enabled: 57/58 statements and 16/18 branches covered (96% combined). Console missing
locations were `59->exit, 81`. The unchanged configuration has no percentage gate.
The configured outputs are artifacts/.coverage and artifacts/coverage.json.

Separate [raw outputs and coverage snapshot](../artifacts/workflow-20260907/)
are retained locally, including each failed probe. Generated artifacts are ignored
by Git and will not accompany a fresh checkout. The original historical session
is preserved in [development history](development-history.md).

Temporary probes ran in a copied fixture with the same installed wrapper. Only
that copy received the failing test and discovery edit, and it was removed on
completion. The real hook was invoked without a commit or index changes; the
README argument and wrapper inspection verify the unconditional full-suite path,
not an actual documentation commit. The stdlib scenario used `-S` to hide installed
packages without removing them. In that mode coverage reports are unavailable.

Git diff/status succeeded but emitted sandbox warnings about inaccessible global
ignore and system cache paths. No global configuration was changed.
