# Add optional coverage to local checks and clarify project guidance

Contributors now get branch coverage, missing-line output and JSON reports from
the existing `tools/check.py` command and installed commit hook whenever coverage
is available. Previously, coverage required separate manual commands. The gate
retains configured unittest discovery and rejects failures and empty suites;
without coverage, it runs the same tests with an explicit notice.

README now puts directory creation directly in the runnable export example and
keeps the CSV/JSON usage contract easy to find. DEVNOTES owns check, coverage and
hook operations; detailed implementation and session notes are preserved in
[development history](../development-history.md). Application behavior, tests,
discovery configuration and the existing hook wrapper remain unchanged.

Validation during this handoff: the prepared runtime passed the normal command,
the actual installed hook invoked with `README.md`, and the stdlib fallback.
Coverage-enabled runs reported 96% for `inventory.py`. See
[current validation](PR-validation.md) for commands, counts, input fingerprints and
local report snapshots. The earlier setup's failure and empty-discovery probes
are documented in [setup verification](../workflow-verification.md); those probes
were not rerun during this handoff.

Coverage is optional and has no percentage threshold. The fallback produces no
new coverage reports; existing reports can therefore be stale. Raw evidence is
ignored and local to this checkout. Validation was offline; no CI, external
integration or release validation was performed.

Status: local draft prepared; maintainer human review is pending. Next, the
maintainer should review the complete setup diff, including the new history and
verification documents, and the linked evidence before approving. No remote PR,
commit, push, tag, version bump or release was made.
