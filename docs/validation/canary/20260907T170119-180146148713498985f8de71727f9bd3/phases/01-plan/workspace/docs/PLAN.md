# Occupied-cell delivery plan

Next: implement caller-supplied fixed occupied cells in a later authorized task,
using the [proposed D1 amendment](DESIGN.md) and its explicit input policies.
The decisive acceptance is `FFRF` from `(0,0,0)` with `{(0,1)}` returning
`((1,0,1), [False,False,True,True])`: failures preserve pose, then commands
continue successfully. This phase prepares documents only.

| Outcome / scope | Dependency and boundary | Acceptance evidence to produce |
|---|---|---|
| Deliver optional occupied-cell input with fixed per-run membership, blocked-command outcomes and unchanged existing calls; include meaningful regression tests and README usage/examples. | Later implementation authorization; resolve any changes arising from pending document reviews. One coherent increment keeps the API, behavior, tests and usage documentation usable together; no separately useful partial delivery is needed. | All [addendum examples](SPEC_OCCUPIED.md), iterable/snapshot semantics, unchanged caller inputs and isolation across runs. Existing tests and added occupied-cell checks pass using the standard suite. |

Sources: [original requirements](ORIGINAL.md), [baseline spec](SPEC.md),
[confirmed request](OCCUPIED_REQUEST.md), [addendum](SPEC_OCCUPIED.md),
[design](DESIGN.md). The design owns rationale; this plan owns delivery status.

## Checks and review policy

Follow [repository instructions](../AGENTS.md) and [development checks](../DEVNOTES.md).
The configured check is `python3 -m unittest discover -s tests -v`. In this
fixture use `"$CANARY_PYTHON" -B -m unittest discover -s tests -v` with the prepared
runtime. No dependency installation, commits or external actions are authorized
in this phase. Design and plan reviews remain pending until actually performed;
author self-checks do not constitute either review or acceptance. No additional
approval procedure is prescribed by the repository.

During implementation, run the standard suite with new meaningful coverage and
check README examples against the callable interface. README owns usage; change
DEVNOTES only if operations change, which this design does not require. Record
actual implementation check/review results here when they exist.

## Current delivery status

- D1 movement and turns: complete, historically accepted; see the unchanged
  [completed record](history/completed.md), [accepted design](history/design-d1.md)
  and [previous plan](history/plan-before-occupied.md), captured before amendment.
- Occupied-cell design amendment, specification addendum and implementation plan:
  drafted; implementation and new feature tests not started.
- Requested design review: pending, not performed. Requested plan review: pending,
  not performed. No new acceptance or implementation review is claimed.
- Baseline check performed on 2026-09-07 with
  `"$CANARY_PYTHON" -B -m unittest discover -s tests -v`: exit 0, all three tests
  passed (`test_turn_and_forward`, `test_left_wraps`, `test_unknown_command`).
  This verifies existing behavior only; occupied-cell acceptance remains untested.
- Inspected `navigator.py`, `tests/test_navigator.py`, README and DEVNOTES:
  one two-argument run function, three unittest cases, standard-library-only
  checks, no other check configuration in this fixture.
