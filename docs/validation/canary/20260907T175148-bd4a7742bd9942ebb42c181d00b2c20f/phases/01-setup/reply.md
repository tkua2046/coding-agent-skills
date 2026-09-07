Implemented and verified.

- Normal checks now use available coverage: missing lines displayed, JSON at `artifacts/coverage.json`, no percentage threshold.
- Normal command and installed hook passed all 5 tests; coverage was 96%.
- Hook failure and zero-discovery probes exited 1, including with the stdlib fallback. Hook remains unconditional for documentation changes.
- README retains user guidance; DEVNOTES owns contributor operations; `docs/development-history.md` preserves historical details.
- Application, CLI, samples, existing tests, discovery configuration and hook delegation remain unchanged. Temporary probes were restored.

Sandbox checks required a local `TMPDIR`. Without coverage, tests still gate successfully but reports are unavailable. No packages installed or external actions taken.