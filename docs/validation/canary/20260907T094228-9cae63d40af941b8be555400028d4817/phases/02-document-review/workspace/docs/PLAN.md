# Plan

Next: independent combined review of [DESIGN.md](DESIGN.md) and this plan against
[REQUEST.md](REQUEST.md) and [SPEC.md](SPEC.md), then implement S1. Planning only is
complete; document review, implementation and code review are pending. Use the
remaining portion of the original 15-minute whole-task allowance, not a new budget
per phase. No commit, push, version change or release is requested.

## Pending outcome

| Stage | Observable outcome and scope | Dependencies and acceptance | Boundary |
| --- | --- | --- | --- |
| S1 — planned | Whole-order rejection and continued processing through both APIs. Update the reservation engine, relevant unittest coverage, and README usage to explain shortage rejection. | Independent document review of D2; validated-input assumptions retained. Pass the decisive examples and validation regressions in SPEC.md plus the complete local gate below. Main risk: deducting an earlier item before discovering a later shortage. | One coherent implementation/review snapshot covering code, tests and usage; no commit. |

Done means the requested behavior is implemented, tests and the installed hook pass
with nonempty discovery, independent code review findings are resolved, and the
result is ready for human review. Preserve S0 and all prior reports. Record actual
checks, review scope/snapshot and findings in a new S1 record or an appended section;
do not mark proposed acceptance as verified. README owns usage; DEVNOTES owns
operations; SPEC owns target behavior; DESIGN owns rationale.

## Verification and review handoff

Follow [DEVNOTES.md](../DEVNOTES.md) and the request's agent-only review authorization:
independent document review → implement with regression tests → full tests and hook
→ independent code snapshot review → fixes and affected checks/review → human-review
handoff. Human review happens afterward and must not be claimed here. There is no
additional approval ceremony or commit step.

Use the supplied runtime, without installing anything:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" .git/hooks/pre-commit
```

These commands must be rerun after implementation. Tests should establish behavior
from SPEC's expected values, including unchanged inputs, rather than mirror private
implementation details. Add missing meaningful cases within the existing unittest
suite; no new framework is needed.

### Verified planning baseline — 2026-09-07

- Inspected engine, JSON adapter/codec, all existing tests, usage/operations docs,
  and both hook copies. The installed `.git/hooks/pre-commit` matches
  `hooks/pre-commit` and rejects empty test discovery.
- `"$CANARY_PYTHON" -m unittest discover -s tests -v`: all 6 existing tests passed.
- `"$CANARY_PYTHON" hooks/pre-commit` and
  `"$CANARY_PYTHON" .git/hooks/pre-commit`: all 6 existing tests passed in each run.
- Read-only engine probe with stock `{"a":4,"b":1}` and orders `reject`, `later`,
  `empty` from SPEC returned `{"a":-3,"b":-2}` with all three accepted. Caller
  stock stayed unchanged. This confirms the requested rejection is absent despite
  the green baseline; no implementation or test changes were made in this phase.

## Historical plan (preserved)

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See [completed S0 context](history/completed.md); it is not evidence for S1.
