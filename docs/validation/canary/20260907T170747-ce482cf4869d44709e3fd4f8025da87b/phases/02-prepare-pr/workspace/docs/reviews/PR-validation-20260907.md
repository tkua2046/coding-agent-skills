# PR preparation validation — 7 September 2026

Outcome: current local checks passed; maintainer human review is pending.
Candidate: working-tree setup changes against
`9ccf826438b48be6d2ffcbf9daece9ec042350b2`, comprising README.md, DEVNOTES.md,
tools/check.py, docs/development-history.md and docs/workflow-verification-20260907.md.
PR preparation adds this record and PR.md only, plus ignored validation artifacts.
The index was empty of staged changes at inspection.

## Checks executed in this phase

The prepared `CANARY_PYTHON` was Python 3.12.4 with coverage 7.16.0. All commands
used `TMPDIR="$PWD/.tmp/pr-preparation"` resolved from the repository root.

| Check | Invocation | Result |
|---|---|---|
| Actual installed hook | Absolute path to `.git/hooks/pre-commit README.md`, from `docs/` | Exit 0; all 5 tests passed; console and JSON coverage produced |
| Stdlib fallback | `"$CANARY_PYTHON" -S tools/check.py`, from root | Exit 0; all 5 tests passed; explicit coverage-unavailable message |
| Tracked diff whitespace | `git diff --check` | Exit 0; no whitespace findings |

The installed hook was executable and byte-identical to `hooks/pre-commit`;
it was not replaced. Its invocation exercised the normal check entrypoint,
including with a README argument and a non-root working directory. No actual
commit was made. The fallback used `-S` to hide site packages, without changing
the environment or installing dependencies.

The fresh JSON report contains only inventory.py and enables branch measurement:
57/58 statements and 16/18 branches covered, 96% combined. Missing locations are
`59->exit, 81`; no percentage threshold is configured. The existing application
suite covers CSV validation, CLI success/failure, preservation of an existing
export and replacement-failure cleanup. It does not provide coverage measurement
of tools/check.py itself.

## Evidence and limits

[Current raw outputs, coverage snapshot and results.json](../../artifacts/pr-preparation-20260907/)
record command arguments, exit codes, runtime and base identity.
`prior-sha256.json` fingerprints the setup candidate and prior artifacts.
Existing top-level coverage outputs were archived there before the hook refreshed
them. Hash comparison confirmed that the setup files and retained prior evidence
were unchanged by validation.

The [prior setup report](../workflow-verification-20260907.md) and its
[raw outputs](../../artifacts/workflow-20260907/) were read and preserved. Its
intentional failing-test and empty-discovery probes in both coverage and stdlib
modes are earlier evidence, not checks repeated in this phase. The 2 September
session remains historical evidence only.

Artifacts are ignored and local to this checkout. Git inspection emitted sandbox
warnings about system cache paths and global ignore access but returned results;
no global configuration was changed. No remote CI, external integration, release
checks or human review occurred. Next action: maintainer review of the setup diff
and the [PR draft](PR.md).
