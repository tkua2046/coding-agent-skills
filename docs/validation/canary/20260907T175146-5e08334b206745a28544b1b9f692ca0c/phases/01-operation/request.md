Use the setup operation in skills/dev-workflow to repair tools/check.py: the
normal check must succeed when collected tests pass, fail when any test fails,
and fail when no tests are collected. Retain unittest and this command path.
Demonstrate the problem and resulting behavior, and write RESULT.md with actual
before/after evidence and remaining work. The application defect described in
DEVNOTES is outside this task: preserve application code, tests and existing docs.
Do not add tooling, install packages, configure hooks, commit or publish.
