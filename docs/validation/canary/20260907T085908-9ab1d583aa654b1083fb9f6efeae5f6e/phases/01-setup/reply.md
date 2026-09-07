Updated `tools/check.py` to use available coverage, show missing lines, and write `artifacts/coverage.json`. Application-only branch coverage and the no-threshold policy remain unchanged.

Verified:
- All five existing tests pass; coverage reports 96%.
- The installed hook runs the full suite for documentation changes.
- Test failures and empty discovery fail the hook.
- Without coverage, the stdlib gate works and explicitly reports that coverage is unavailable.

README retains user instructions; DEVNOTES owns contributor operations. Historical notes moved to `docs/DEVELOPMENT_HISTORY.md`; verification details are in `docs/reviews/local-workflow-2026-09-07.md`.

Temporary probes were restored. Application code, sample data, existing tests, discovery configuration and hook delegation remain unchanged. No packages were installed or commits created.