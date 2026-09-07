# Local PR validation — 7 September 2026

The current setup candidate passed the local checks below. Human review is
pending; these results are execution evidence, not a review approval.

Candidate: working-tree changes against `df6182f` in `tools/check.py`, README,
DEVNOTES, and new `docs/DEVELOPMENT_HISTORY.md`. No staged changes were present.
[SHA-256 identities](candidate-sha256.json) cover these files and the relevant
unchanged application, tests, configuration, and hook. Their contents remained
unchanged through validation. Draft/evidence files were added for this handoff.

| Fresh check | Result | Evidence |
| --- | --- | --- |
| `.git/hooks/pre-commit` from repository root | Exit 0; 5 tests passed | [Hook log](installed-hook.log) |
| `"$CANARY_PYTHON" "$REPO/tools/check.py"` from `qa/` (`REPO` denotes this checkout) | Exit 0; 5 tests passed | [Gate log](normal-from-qa.log) |
| `git diff --check` | Exit 0; no whitespace findings; xcrun cache writes denied by sandbox | [Diff log](diff-check.log) |

[Run metadata](results.json) records exact commands, directories, UTC timestamp,
and interpreter: prepared Python 3.12.4 with coverage 7.16.0. The installed hook
was executable and byte-identical to `hooks/pre-commit`. TMPDIR was set to a new
workspace artifact directory so tests could create local temporary files.
Both suite runs reported 96% combined statement/branch coverage for `inventory.py`,
with missing line 81 and partial branches shown in the logs. There is no required
coverage threshold. No packages were installed.

Before execution, existing `artifacts/.coverage` and `artifacts/coverage.json`
were copied to `prior-*` files in
[the new local archive](../../../artifacts/pr-validation-2026-09-07/).
Per-run coverage outputs are also archived there. These generated files are
Git-ignored; the logs and metadata beside this document are the durable handoff.

Prior setup evidence remains untouched in
[workflow-verification-a44ge9xz](../../../artifacts/workflow-verification-a44ge9xz/summary.txt).
Its logs record successful normal, installed-hook, documentation-hook, and
stdlib-hook runs, plus exit 1 for intentional failure and empty-discovery probes
with and without coverage. Those probes were inspected, not rerun, and their
exact candidate identity was not established in this fresh context. The separate
[earlier normal log](../../../artifacts/workflow-verification-7rrtlk1o/normal.log)
and the [2 September record](../../DEVELOPMENT_HISTORY.md) are also historical.
Ignored artifact links work only in the retained local checkout.

No remote CI, external integration, release checks, or human review occurred.
Next action: maintainer reviews the setup diff and this evidence using
[the local PR draft](../PR.md).
