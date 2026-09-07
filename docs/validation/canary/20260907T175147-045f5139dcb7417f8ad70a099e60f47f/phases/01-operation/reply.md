Repaired `tools/check.py`, retaining unittest and the command path.

Verified before → after exit codes:

- Passing tests: 0 → 0
- Failing tests: 0 → 1
- No tests: 0 → 1

The unchanged application suite still exposes the known defect and now correctly exits 1. Application code, tests, and existing docs were preserved.

Actual evidence and remaining work are recorded in `RESULT.md`.