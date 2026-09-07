# Add optional coverage to local checks and clarify setup docs

Contributors now get branch coverage and missing-line reports from the normal
`tools/check.py` command and existing installed pre-commit hook when coverage is
available in the prepared interpreter. Measurement starts before test discovery,
and paths resolve from the repository root. The existing unittest discovery,
failure gate and empty-suite rejection remain in place; no dependencies are added.

README keeps the CSV/JSON usage contract and puts `mkdir -p artifacts` directly in
the quick-start example. DEVNOTES explains checks, coverage artifacts and hook
restoration. Implementation notes and the original session record are preserved
in [development history](../DEVELOPMENT_HISTORY.md). Application behavior and the
CLI are unchanged.

## Validation and limits

- Current PR preparation: the normal command and actual installed hook passed
  using `CANARY_PYTHON`; the stdlib fallback (`-S`) and `git diff --check` also
  passed. Coverage JSON confirms application-only branch measurement. See
  [current validation and candidate identity](pr-validation-2026-09-07.md).
- Coverage reports 96%, with missing line 81 and partial branches remaining;
  there is no percentage gate. Without coverage, tests still run with an explicit
  notice and no new coverage reports. Existing reports can therefore be stale.
- Failure, empty-discovery and documentation-only hook probes are **prior setup
  results**, retained in [setup evidence](local-workflow-2026-09-07.md). They were
  not rerun during drafting. Prior records and generated reports were preserved.
- Validation was local and offline; no CI or external integration ran.

## Next review action

Maintainer human review is pending. Review the setup/check changes, documentation
placement and linked evidence before deciding whether to accept the changes.
This is a local PR draft; no remote PR, commit, push, tag, version bump or release
was created.
