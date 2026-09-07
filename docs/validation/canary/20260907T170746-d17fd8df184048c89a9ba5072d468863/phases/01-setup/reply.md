Implemented optional coverage in `tools/check.py`: missing-line output and `artifacts/coverage.json`, preserving application-only branch settings and no percentage threshold.

Verified five tests pass through the normal command and installed hook, including documentation-only staging. Test failures and empty discovery fail the gate. The stdlib fallback also works; without coverage, reports are unavailable. Empty discovery additionally emits a coverage no-data error.

README retains user guidance. Contributor instructions are in `DEVNOTES.md`; history and verification evidence are under `docs/`.

Application, CLI, sample data, existing tests and hook delegation remain unchanged. Temporary probes were restored. No packages installed or commits created.