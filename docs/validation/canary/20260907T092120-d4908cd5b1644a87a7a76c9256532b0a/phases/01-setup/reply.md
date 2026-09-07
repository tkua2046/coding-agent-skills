Updated the check command to use available coverage, show missing lines, and write `artifacts/coverage.json`, retaining application-only branch coverage and no percentage threshold.

Verified all five tests through the normal command and installed hook. Isolated probes confirmed failure and zero-test rejection, including the stdlib fallback. Without coverage, tests still gate successfully but generate no reports.

README now serves users; DEVNOTES owns contributor instructions; `docs/development-history.md` preserves historical detail. Results are documented in `docs/workflow-verification.md`.

Application, tests, sample data, discovery settings and hook delegation remain unchanged. Temporary probes were removed. No packages installed or commits made.