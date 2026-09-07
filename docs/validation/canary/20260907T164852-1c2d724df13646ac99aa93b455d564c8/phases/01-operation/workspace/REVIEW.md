# R1 recheck

Verdict: **needs changes**. Open finding: **R1**. Next action: move the selection update after command validation, then verify that rejected commands preserve both cursor and selection.

## Reviewed scope and version

Independent review of the current supplied candidate against `REQUEST.md`, following `AGENTS.md` and the review operation in `skills/stage-development`. Inspected all of `session.py` and the original review, `reviews/round1.md`.

HEAD: `4979bd84ed8f530eb7c8a66f2d904243aac79064` (`Fixture baseline`). Initial `git status --short` and `git diff` had no output: no dirty/new candidate files or candidate diff. Git emitted sandbox cache/config-access warnings but returned successfully. Candidate `session.py` SHA-256: `a2e28ac4bfc03a0a481453930578a6f659a933ec5663c86cdfdd8a02bf931921`.

## Finding and prior disposition

**R1 — open, partially fixed; required state preservation still fails** (`session.py:6–9`). The original C1 review reported that an unknown command changed both cursor and selection before raising. The author claimed a fix by moving the cursor update after validation. This recheck verifies that cursor preservation is fixed, but selection is still unconditionally assigned `"closed"` at line 6 before validation.

Concrete trigger: `s = Session(); s.apply("unknown")`. It raises `ValueError("unknown command")`, but state changes from `(4, "open")` to `(4, "closed")`. The same failure occurs for the empty-string command. A caller catching the exception therefore receives altered selection despite the explicit requirement to preserve both fields.

Minimal correction: validate the command before either state assignment. Verify rejected commands from a non-closed selection preserve the complete pre-call cursor/selection pair and raise `ValueError`; also check that valid commands still perform their intended updates.

The original review remains unchanged at `reviews/round1.md` (SHA-256 `0648684b49aef0d411c7bdb3329c074a2e5216f498bdefa155f1fbe65e5e4bfa`). This report appends the current disposition without replacing the original concern or evidence.

## Checks and limits

Executed the following local experiment using the prepared runtime, with bytecode writes disabled:

```sh
"$CANARY_PYTHON" -B - <<'PY'
from session import Session
for command in ('unknown', '', 'next', 'previous'):
    s = Session()
    before = (s.cursor, s.selection)
    try:
        s.apply(command)
        outcome = 'returned'
    except ValueError as exc:
        outcome = f'ValueError: {exc}'
    after = (s.cursor, s.selection)
    print(command, before, after, outcome)
PY
```

Observed results:

| Command | Before | After | Outcome |
| --- | --- | --- | --- |
| `"unknown"` | `(4, "open")` | `(4, "closed")` | `ValueError: unknown command` |
| `""` | `(4, "open")` | `(4, "closed")` | `ValueError: unknown command` |
| `"next"` | `(4, "open")` | `(5, "closed")` | Returned |
| `"previous"` | `(4, "open")` | `(3, "closed")` | Returned |

Both rejection probes fail the required preservation invariant. Valid-command probes confirm the adjacent update paths execute. No supplied automated tests were present; this was a focused R1 recheck, not exhaustive input testing. No production files, tests, specs, plans, or prior reports were changed. This verdict does not establish human approval or release readiness.
