Updated the check command to use available coverage, show missing lines, and write `artifacts/coverage.json`. Application-only branch settings and no percentage threshold remain unchanged.

Verified all 5 tests pass through the normal command and installed hook. Failure and empty-discovery probes correctly failed, including with coverage unavailable. The stdlib fallback works but cannot generate coverage reports.

README retains user guidance; DEVNOTES owns contributor operations; `docs/development-history.md` preserves historical detail.

Evidence: `artifacts/workflow-verification-20260907-020113/`.

Temporary fixtures were removed. Application, CLI, sample data, and existing tests remain unchanged. No packages or external actions were used.