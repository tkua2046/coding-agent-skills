# Gate disposition

The first final local `pre-commit run --all-files` exited 1 even though all 250 tests and other checks passed. During its pytest hook, the coordinating author updated docs/VALIDATION.md with the completed independent packet-repair result. Pre-commit detected that concurrent tracked-file change and reported “files were modified by this hook.” The only unstaged tracked change was that author-written validation paragraph; the test output itself contains no failed test.

The original log remains final-gate.log. Freeze the final documentation before running the complete gate again; no hook is bypassed and this invocation is not called a passing gate. The eventual source commit's hook and remote exact-commit CI establish delivery checks separately from this archived attempt.
