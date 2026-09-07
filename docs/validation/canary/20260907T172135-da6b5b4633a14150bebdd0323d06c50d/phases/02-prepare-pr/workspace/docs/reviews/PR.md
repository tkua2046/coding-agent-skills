# Add optional coverage to local checks and clarify contributor docs

The normal `tools/check.py` command now measures coverage when the selected
interpreter already provides it, so contributors get branch coverage, missing
lines and JSON reports through the existing installed pre-commit hook. Discovery
still follows `quality.ini`; failed tests and empty discovery fail the gate.
Without coverage, the standard-library tests still run with an explicit notice.

README now creates the output directory in its runnable example and focuses on
CSV/JSON usage. DEVNOTES owns check, hook and troubleshooting instructions;
[implementation notes](../DESIGN.md) and [development history](../DEVELOPMENT_HISTORY.md)
preserve the moved material. The application, CLI and CSV/JSON contract are unchanged.

Validation on this uncommitted setup candidate (base `1b6e3bf2cffed987854592f3f6e65982d0022e43`):

- Invoked the actual installed `.git/hooks/pre-commit` with `CANARY_PYTHON`
  (Python 3.12.4, coverage 7.16.0) and a workspace-local `TMPDIR`: all 5 tests
  passed, exit 0. Coverage reported 96%; JSON measures only `inventory.py` with
  branches enabled. The installed hook is executable and matches the maintained wrapper.
- `git diff --check` passed; the index was empty. See the
  [current validation record](pr-validation-2026-09-07/README.md) for logs,
  runtime details and candidate hashes.
- The [retained setup report](2026-09-07-local-workflow.md) records earlier
  documentation-only staging, failing-test, empty-discovery and no-coverage
  probes. Those probes were not rerun for this draft.

There is no coverage threshold. Without coverage, reports are not refreshed and
existing reports may be stale. Missing line 81 and uncovered branches remain;
no remote CI or external integration was run. This is a local PR draft only.

Maintainer human review is pending. Next: review the setup diff and linked
evidence, especially the optional-coverage behavior and preservation of moved
documentation, before accepting the changes.
