# Add optional coverage to local checks and clarify contributor docs

The existing check command now automatically reports application coverage when
the selected Python interpreter provides `coverage`. Contributors get test and
coverage results from the same command and installed pre-commit hook, using the
existing `.coveragerc`; no dependency installation is required. Without coverage,
the command reports its absence and runs the standard-library unittest gate.
The established `qa/check_*.py` discovery and empty-suite failure remain intact.

README now includes directory creation in the runnable export example and keeps
the user-facing CSV/JSON contract. DEVNOTES explains checks, hook invocation,
optional coverage and the local temporary-directory workaround. Implementation
notes and the historical session are preserved in
[development history](../development-history.md). The exporter, CLI, tests and
hook wrapper are unchanged.

Validation on this uncommitted candidate over `e1bb8fd` (7 September 2026):

- Invoked the actual installed `.git/hooks/pre-commit` with `CANARY_PYTHON`
  (Python 3.12.4) and a repository-local `TMPDIR`: exit 0, all 5 tests passed.
- Application coverage with branch measurement reported 96%, with gaps at `59->exit`
  and line 81. There is no required coverage percentage.
- See [hook output](evidence/prepare-pr-hook.txt),
  [current coverage](evidence/prepare-pr-coverage.json) and
  [runtime, command and candidate hashes](evidence/prepare-pr-validation.json).
  Prior `artifacts/.coverage` and `artifacts/coverage.json` were preserved byte
  for byte; those retained artifacts and the 2 September session are past
  evidence, not checks performed for this draft.

Limits: this run exercised coverage being available; the no-coverage fallback
and empty-suite failure were inspected but not exercised in this handoff.
Coverage measures `inventory.py`, not the check runner. No remote CI or external
integration was run.

Next action: maintainer human review of the setup diff and linked evidence is
pending. This is a local PR draft only; no remote PR, commit, push, tag, version
change or release was performed.
