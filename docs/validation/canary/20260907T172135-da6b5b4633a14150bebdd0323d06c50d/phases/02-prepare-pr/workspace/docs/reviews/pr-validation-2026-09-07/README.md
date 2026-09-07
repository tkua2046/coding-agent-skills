# PR preparation validation — 7 September 2026

Fresh local checks for the uncommitted setup candidate based on
`1b6e3bf2cffed987854592f3f6e65982d0022e43`. This evidence supports the
[PR snapshot](../PR.md); it is not a human review or a replacement for the
[prior setup report](../2026-09-07-local-workflow.md).

The [candidate SHA-256 hashes](candidate-sha256.json) identify all setup files,
retained documents and relevant application/check inputs, including the installed
hook. Those bytes were verified unchanged after execution. Draft and validation
artifacts were added separately. [Runtime metadata](runtime.json) records the
prepared interpreter and confirms the installed hook is executable and
byte-identical to `hooks/pre-commit`.

Executed from the repository root with `TMPDIR="$PWD/.tmp"` and the supplied
`CANARY_PYTHON`; no packages were installed:

| Check | Result | Evidence |
| --- | --- | --- |
| Actual `.git/hooks/pre-commit` | Exit 0, 5 tests passed, 96% coverage | [Output](installed-hook.txt) |
| `git diff --check` | Exit 0 | [Output](diff-check.txt) |
| `git diff --cached --stat` | Exit 0, no staged changes | [Output](staged.txt) |
| `git rev-parse HEAD` | Exit 0, base recorded above | [Output](head.txt) |

The [fresh coverage JSON](current-coverage.json) was inspected: only
`inventory.py` is measured, branch coverage is enabled, line 81 is missing,
and missing branch pairs are `[59, -45]` (function exit) and `[80, 81]`.
Existing `artifacts/` content was copied into `prior-artifacts/` before the hook
refreshed generated reports; the earlier Markdown report remains untouched.

Git printed sandbox cache/global-ignore warnings but the recorded commands
completed successfully. Earlier negative and stdlib fallback probes remain
historical evidence, not fresh results. No remote validation or human review
occurred; maintainer review remains pending after handoff.
