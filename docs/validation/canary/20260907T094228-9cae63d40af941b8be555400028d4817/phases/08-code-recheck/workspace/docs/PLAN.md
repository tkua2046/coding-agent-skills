# Plan

Next: independent code review of the S1 candidate recorded below, then resolve
supported findings and hand off for human review. Document review is ready and
implementation checks pass; code review and human review remain pending. Use the
remaining portion of the original 15-minute whole-task allowance, not a new budget
per phase. No commit, push, version change or release is requested.

## Pending outcome

| Stage | Observable outcome and scope | Dependencies and acceptance | Boundary |
| --- | --- | --- | --- |
| S1 — implemented, awaiting review | Whole-order rejection and continued processing through both APIs. Reservation engine, unittest coverage, and README usage updated. | Document review ready; local tests and installed gate pass. Independent code review and subsequent human review pending. Main risk covered: deducting an earlier item before discovering a later shortage. | One coherent implementation/review snapshot covering code, tests and usage; no commit. |

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

These commands were rerun after implementation (evidence below). Tests should establish behavior
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

## S1 current record — 2026-09-07

- Outcome: engine preflights each order before deduction; both APIs preserve their
  signatures and validation boundary. README explains shortage behavior. No added
  dependencies, validation policies, infrastructure or changes to operations.
- Document review: [existing independent report](../reviews/design-current.json)
  has verdict `ready`, no findings. All its recorded SHA-256 values matched at
  implementation intake. The initial working tree already contained DESIGN, PLAN
  and SPEC changes plus that report; those prior artifacts are preserved. Plan
  progress and SPEC implementation status now reflect this candidate; D2 rationale
  and the original requirements remain intact.
- Candidate: [manifest](../reviews/s1-candidate.json) records base commit and file
  hashes; [captured diff](../reviews/s1-candidate.patch) includes the code, tests,
  usage, and prior document changes relative to that base. New report/log contents
  are retained and hashed separately. HEAD alone does not identify this candidate.
- Checks: intake `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`
  passed 6 baseline tests. After implementation, the same command passed 11 tests
  ([raw output](../reviews/s1-tests.txt));
  `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" .git/hooks/pre-commit` passed all 11
  ([raw output](../reviews/s1-installed-gate.txt)). No hook modifications occurred.
  The installed gate is the full local gate; no additional lint/format or release
  checks are specified. Staged whitespace verification and snapshot consistency
  are recorded in the manifest.
- Coverage: both APIs exercise rejection alone with a later insufficient item,
  continuation, exact-stock success, depletion, empty orders/batches, copied stock,
  deep input preservation, and integer quantities/boolean outcomes. Validation
  regressions cover malformed JSON, invalid shapes, duplicate IDs/SKUs, unknown
  SKUs and invalid quantities; a boundary test verifies no engine call before the
  entire payload passes validation. The six original tests remain.
- Open finding IDs: none reported; independent code review has not happened.
  This is an author implementation handoff, not a code-review verdict or stage
  acceptance. Human review remains pending. Prior-phase elapsed time is unavailable;
  no claim is made about the total cross-phase 15-minute allowance.
- Next action: the separately assigned reviewer should read REQUEST, ORIGINAL,
  SPEC, D2, this plan, both APIs and codec, tests, diff and check evidence against
  the manifest. Implementation edits are paused for that review. Address supported
  findings and rerun affected checks before human review. No commit was made and
  none is authorized; no push, version advancement or release occurred.

## Historical plan (preserved)

S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.

See [completed S0 context](history/completed.md); it is not evidence for S1.
