Repaired `tools/check.py`, retaining unittest and the existing command path.

Verified before → after exit statuses:

- Passing tests: 0 → 0
- Failing tests: 0 → 1
- No tests: 0 → 1

`RESULT.md` contains actual transcripts and reproduction instructions. Application code, tests, and existing docs are unchanged. The known application defect remains and correctly causes the normal check to fail.