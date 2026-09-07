# Local workflow verification, 2026-09-07

Outcome: the normal command and installed hook pass all five existing tests with
coverage. Assertion failures and empty discovery fail the hook, including when
coverage is unavailable. No application code, sample data or existing tests changed.

## Executed checks

The prepared CANARY_PYTHON interpreter provided coverage. The original stdlib
baseline passed five tests. After the change, `"${CANARY_PYTHON:-python3}"
tools/check.py` passed five tests and displayed missing lines. The report measured
only inventory.py with branches: 96% displayed, missing line 81 and partial branch
59->exit. No percentage threshold was added. `artifacts/coverage.json` was parsed
and checked for application-only scope and branch measurement.

The existing executable `.git/hooks/pre-commit` already matched hooks/pre-commit;
no reinstall was necessary. Its direct invocation with README.md ran all five
tests. The wrapper has no filename or staged-diff filtering, so documentation
changes use the same full-suite gate. No commit was made and the index was unchanged.

[Detailed command output](2026-09-07-local-setup-output.txt) records seven cases:
installed hook success; copied hook success from outside the repository; injected
assertion failure; empty discovery via the configured pattern; stdlib fallback
success; fallback assertion failure; fallback empty discovery. Expected exits were
0 for passing suites and 1 for failures/empty discovery.

Failure probes used disposable copies of the installed hook, checker, configuration
and application suite under .tmp. The absent-coverage case used the same prepared
interpreter with `-S` to disable site packages. It emitted the limitation message,
passed five tests and generated no coverage artifacts. These copies and the
verification driver were removed. Byte comparisons confirmed unchanged application,
existing tests, sample, discovery/coverage configurations, hook wrappers and index.

## Limits and retained evidence

Without coverage, only the stdlib test gate is available; no coverage report is
produced. No packages, environments or toolchains were installed or replaced.
No external integration or Git commit lifecycle was exercised. Direct hook
execution verified the local gate. Prior historical material remains preserved in
[development history](../DEVELOPMENT_HISTORY.md); current operations belong in
[DEVNOTES](../../DEVNOTES.md). Detailed output is retained separately from disposable
coverage artifacts. No pre-existing coverage reports were present before this run.

## Verified checker identity

`tools/check.py` SHA-256: `d49d57861b1f2fcc43957479db04e0d77c5de2d1910f6b926a6e3e7b7fae872b`
