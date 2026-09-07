Implemented and verified.

- Normal checks now include available coverage: missing lines, `artifacts/coverage.json`, and no percentage threshold.
- Installed hook passed all 5 tests. Disposable failure and empty-discovery probes correctly failed in both coverage and stdlib modes.
- Coverage measured 96%; stdlib fallback explicitly reports unavailable coverage.
- README retains user guidance; DEVNOTES owns contributor instructions; `docs/` preserves history and records verification.
- Application, CLI, sample data, tests, discovery configuration and hook delegation remain unchanged.

Temporary probes were removed. No packages installed or commits created. Sandbox verification required a workspace-local temporary directory.