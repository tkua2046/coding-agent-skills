# Plan

Next outcome S1: deliver whole-order rejection through both existing APIs, after
independent review of this design and plan. The decisive acceptance is the
[design's mixed batch and rejection prefix](DESIGN.md#decisive-acceptance): rejection
preserves stock, a later exact-fit order succeeds, and results remain ordered.

| Outcome / scope | Dependency and boundary | Acceptance |
|---|---|---|
| S1 — implement whole-order reservation, regression tests, and current behavior/usage documentation | Independent document review first. One coherent local increment; no infrastructure or separate delivery prerequisite. | Both APIs satisfy the design examples and compatibility checks; full test discovery and local hook pass with nonzero tests; independent code review findings are resolved before human handoff. |

Implement the engine's availability check before any per-order deduction. Include
meaningful regression tests and update [SPEC.md](SPEC.md) to describe the new current
contract and [README.md](../README.md) to explain rejected orders and continuation.
Retain [REQUEST.md](REQUEST.md), [ORIGINAL.md](ORIGINAL.md), D1 and completed history.
Do not implement the new behavior in the JSON adapter or expand validation policy.

Execution/review policy: [REQUEST.md](REQUEST.md) and [DEVNOTES.md](../DEVNOTES.md).
Use only the supplied fixture/runtime, no installs or external services. Commands:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

The hook rejects empty discovery. The independent document reviewer follows this
planning phase; an implementer then completes S1 and obtains independent code
review. Agent-only reviews are authorized; human review follows the completed
handoff. Preserve prior review reports and record findings/dispositions without
claiming unperformed reviews. No commit, push, version change or release. Keep
inspection, implementation and necessary reviews within the original 15-minute
whole-task allowance; it is a ceiling shared across phases, not a new allowance.

## Current delivery and evidence

S1 is implemented and the installed gate passes. Independent code review and human
review remain pending; stage acceptance is not complete. Next: the independent
code reviewer reviews the candidate below and records findings/verification before
human acceptance. No commit, push, version change or release was performed.

The [original independent document review](../reviews/design-current.json) has
verdict `ready` and no open findings. Before implementation, all 14 recorded input
SHA-256 hashes matched, including design, plan, source, tests and gate. There is no
unresolved document-review blocker. The exact reviewed
[design](../reviews/s1-evidence/reviewed-DESIGN.md) and
[plan](../reviews/s1-evidence/reviewed-PLAN.md) are retained, as are the original
requirements, review report and S0 history. D2's status annotation now reflects
that review; no design behavior changed. No independent code-review verdict or
human approval is claimed.

Implementation: `inventory.reserve` checks availability before any deduction for
an order. Rejections leave stock intact and processing continues. Adapter and codec
are unchanged. The current spec and README describe rejection and continuation;
README records the Unreleased impact. All 6 existing tests are preserved, with 5
new test methods covering both APIs, the mixed batch and rejection prefix, current
stock versus initial stock, single-item shortages including zero stock, empty
inputs, exact-fit success, ordered boolean results, integer counts, copied stock,
nested input immutability and representative whole-payload JSON validation errors.

Candidate: base `81655edcf4fd63cff672c4830c40a15f45391228` plus the
[captured candidate diff](../reviews/s1-evidence/candidate.patch). This diff captures
all changed tracked files, including this record. Original review and evidence files
are staged alongside it. The reviewer should read [REQUEST.md](REQUEST.md),
[ORIGINAL.md](ORIGINAL.md), current design/plan, actual code/tests and
`hooks/pre-commit`. Source/tests/check configuration were unchanged after the
successful gate. Evidence files are review artifacts, not additional product scope.

Checks on 2026-09-07 used `CANARY_PYTHON` resolving to
`/Users/tk/Documents/coding-agent-skills/.venv/bin/python`, Python 3.12.4
(Clang 15.0.0). No packages were installed or external services used.

| Command / evidence | Actual result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v > reviews/s1-evidence/regression-before.txt 2>&1` | Original engine plus new tests: 11 tests ran, 10 failing subcases. [Original output](../reviews/s1-evidence/regression-before.txt) retained; this is expected regression evidence, not a passing baseline. |
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" hooks/pre-commit > reviews/s1-evidence/gate.txt 2>&1` | Exit 0; all 11 tests passed. [Original output](../reviews/s1-evidence/gate.txt). The installed hook performs full discovery and rejects empty collection, satisfying the suite and gate checks together. |
| `git diff --cached --check` | Exit 2; flags one blank context line in the captured patch and three unittest progress lines in the original failure output. Those evidence bytes are preserved. |
| `git diff --cached --check -- README.md docs inventory.py tests/test_inventory.py` | Exit 0; product, documentation and test changes have no whitespace errors. |

The earlier 6-test passing baseline and observed unconditional-deduction feature gap
remain documented in the preserved planning record and original document review.
The failing regression run above establishes that new tests expose that gap.
No author assertion substitutes for the pending independent code review. Keep
candidate content stable for that reviewer; subsequent fixes require relevant
rechecks and reviewer verification.

## Preserved prior plan and completed work

> # Plan
> S0 complete: in-memory reservation and JSON validation are delivered.
> No pending work before the current change request.

[S0 historical record](history/completed.md) remains unchanged; it is not evidence
that S1 has been delivered.
