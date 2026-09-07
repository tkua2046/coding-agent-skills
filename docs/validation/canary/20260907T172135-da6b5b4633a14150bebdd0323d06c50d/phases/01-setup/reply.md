Updated the local gate to use available coverage, show missing lines and write `artifacts/coverage.json`, without a percentage threshold.

Verified five passing tests, 96% coverage, and the installed hook running with only README staged. Both coverage and stdlib paths reject test failures and empty discovery. Without coverage, tests still run and reports are not refreshed.

README retains user guidance; DEVNOTES owns contributor instructions; `docs/DESIGN.md` and `docs/DEVELOPMENT_HISTORY.md` preserve implementation and historical detail. Verification is recorded in `docs/reviews/2026-09-07-local-workflow.md`.

Application, samples, existing tests and configurations remain unchanged. Temporary probes were restored. No installations, commits or external actions occurred.