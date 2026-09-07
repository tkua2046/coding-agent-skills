# Plan

Next: deliver caller-supplied fixed occupied cells with per-command failure and
continued command processing. The prerequisite is the confirmed
[request](OCCUPIED_REQUEST.md), captured in [the spec](SPEC.md) and the proposed
[design extension](DESIGN.md). No external dependency or migration is needed.

| Pending outcome and scope | Boundary and dependencies | Acceptance |
|---|---|---|
| S1: extend navigation with optional fixed occupancy, regression and feature tests, and README usage for the new argument and outcomes | One coherent local implementation increment: runtime behavior, tests and caller documentation must agree. Depends on the existing S0 behavior. No separately useful partial delivery is needed. | All design acceptance examples pass; blocked movement preserves the full pose and permits later commands; all headings, snapshot isolation, duplicates, independent runs and omitted/empty occupancy are covered. Existing tests stay green. README shows a blocked move followed by a successful turn and move. |

S1 is a proposed future commit boundary only. This phase writes documents; it
does not implement, commit, install packages, publish or perform remote actions.

## Checks and review policy

Follow [repository scope and ownership](../AGENTS.md) and
[development checks](../DEVNOTES.md). Before any future implementation commit,
run the complete standard-library unittest suite, inspect the local diff for
scope and compatibility, and verify S1 acceptance against the spec and examples.
No hooks or separate review/approval gate are specified by this fixture; this
plan adds none. Any future commit requires authorization outside this document-only
phase. The current author self-check is not independent review or human acceptance.

## Delivery status

- S0 remains complete. Its historical acceptance is retained below and in
  [the completed record](history/completed.md). It is not feature validation.
- S1 is pending; no occupied-cell code or tests have been implemented in this phase.
- Baseline inspection: `navigator.py` always advances on F and appends `True` for
  each valid command. `tests/test_navigator.py` contains three tests for turn/move,
  left wrapping and unknown commands. The fixture supplies no additional check
  configuration; DEVNOTES specifies unittest discovery.
- Actual baseline check on 2026-09-07:
  `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`
  passed all 3 tests. This validates the existing code only. Occupied-cell
  acceptance checks described above remain proposed.

## Preserved completed work

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

The [pre-feature plan](history/plan-before-occupied.md) is preserved verbatim.
