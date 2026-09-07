Updated the gate and documentation using `skills/dev-workflow`.

- Normal checks now use available coverage: missing lines, configured JSON output, application-only branch measurement, no percentage threshold.
- All five tests passed through both the normal command and existing installed hook; coverage was 96%.
- Isolated probes verified documentation-change execution, test-failure rejection, empty-discovery rejection, and stdlib fallback.
- README retains user guidance; DEVNOTES owns contributor instructions; `docs/DEVELOPMENT_HISTORY.md` preserves historical detail.
- Application, CLI, sample data, tests, discovery configuration and hook delegation remain unchanged.

Without coverage, tests still gate successfully but generate no coverage reports. Evidence remains under `artifacts/workflow-verification-*`; temporary fixtures were removed and earlier evidence preserved. No packages installed or commits created.