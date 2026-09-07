Updated the normal check to use available coverage, show missing lines, and write `artifacts/coverage.json`, without a percentage threshold.

Verified five tests pass at 96% coverage. The installed hook runs the full suite for documentation changes; failure and empty-discovery probes correctly fail. The stdlib fallback also works, but cannot produce coverage reports.

README retains user guidance; contributor instructions live in `DEVNOTES.md`, history in `docs/DEVELOPMENT_HISTORY.md`, and verification evidence in `docs/validation/`.

Application, CLI, sample data, existing tests and retained configurations are unchanged. Temporary probes were removed. No packages installed or commits made.