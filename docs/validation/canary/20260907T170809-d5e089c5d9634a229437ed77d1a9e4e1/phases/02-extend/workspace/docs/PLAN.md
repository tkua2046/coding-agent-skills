# Plan

Next: settle the YAML parser/policy and unresolved input rules, then deliver loading
a validated starting pose and fixed occupied cells once for navigation. Decisive
acceptance: load [start.yaml](../examples/start.yaml) and run `FFRF` to obtain
`((1, 0, 1), [False, False, True, True])`; a malformed final cell must fail clearly
without consuming any movement commands.

Sources: [original requirements](ORIGINAL.md), [occupied request](OCCUPIED_REQUEST.md),
[YAML request](YAML_REQUEST.md), [current spec](SPEC.md), and
[revised design](DESIGN.md). YAML supersedes the earlier no-configuration scope and
the pending plan's assertion that no external dependency decision is needed.

| Pending outcome and scope | Boundary and dependencies | Acceptance |
|---|---|---|
| Resolve the YAML implementation contract | Prerequisite for YAML delivery: settle [contract questions](DESIGN.md#unresolved-contract-questions), especially the DEVNOTES dependency conflict. Verify a proposed parser's relevant behavior in a later authorized implementation environment before selection. This is a decision prerequisite, not a separate implementation commit. | Record chosen schema/value/duplicate/YAML-feature rules with examples and the dependency-policy decision. No open consequential question silently becomes an accepted rule. |
| S1: reusable fixed occupancy and validated YAML initialization, meaningful tests and affected documentation | Expand existing pending S1 rather than claim obstacle support is delivered. Depends on S0 and the resolved contract. One proposed coherent implementation boundary includes direct navigation and YAML loading, because initialization must lead to working occupied-cell navigation. A parser-only delivery would not satisfy the request. | All [design acceptance targets](DESIGN.md#acceptance-targets) and settled contract examples pass. Preserve direct calls, all headings, continued processing, snapshot isolation, one-shot iterables and independent runs. Validate the entire file before commands, including malformed-final-entry and failure/retry cases. Demonstrate one load/index build and reuse for about 200,000 distinct cells; measure load time and peak/retained memory and verify membership queries without scans/copies. README owns loader/direct-call usage, errors and a blocked-then-successful example; DEVNOTES owns approved dependency/setup and check instructions. |

S1 is a proposed future commit boundary only. No migration or persistent state is
introduced. If peak memory fails an agreed budget, revisit loading before acceptance.
No numerical performance threshold is specified; estimates are not evidence.
This phase revises documents only: no implementation, installation, commits,
publishing or external actions.

## Checks and review policy

Follow [repository scope and ownership](../AGENTS.md) and
[development checks](../DEVNOTES.md). For future implementation, run the complete
standard-library unittest suite, inspect the local diff for scope/compatibility,
and verify S1 against the spec and design examples. In this fixture use
`PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`.
Scale evidence must name the selected parser and environment; small example tests
cannot substantiate 200,000-cell loading/memory behavior. Parser tests must establish
the agreed rejection rules, including duplicate keys a default loader might discard.

No hooks or separate approval gate are specified by this fixture; this plan adds
none. Future implementation or commits need authorization outside this document-only
phase. Author artifact checks are not independent review or human acceptance.
Reviews remain pending unless actually performed.

## Delivery status

- S0 remains complete. Its historical acceptance is retained below and in
  [the completed record](history/completed.md). It is not feature validation.
- S1 remains pending, expanded to include YAML. No occupied-cell or YAML code/tests
  have been implemented. Contract decisions and parser selection remain unresolved.
- Current design review, plan review, implementation review and feature acceptance
  remain pending; no new review report or approval is claimed in this phase.
- Baseline inspection: `navigator.py` always advances on F and appends `True` for
  each valid command. `tests/test_navigator.py` contains three tests for turn/move,
  left wrapping and unknown commands. The fixture supplies no additional check
  configuration; DEVNOTES specifies standard-library-only unittest discovery.
- Prior recorded baseline on 2026-09-07:
  `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`
  passed all 3 tests. This validates existing code only. That prior report remains
  retained here; occupied-cell acceptance was proposed, not executed.
- Fresh-context baseline on 2026-09-07: the same command again passed all 3 tests.
  This verifies existing navigation only. YAML parsing, occupancy acceptance and
  scale measurements have not been executed; future checks above remain proposed.

## Preserved completed work

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before the occupied-cell request.

The [pre-feature plan](history/plan-before-occupied.md),
[accepted D1 design](history/design-d1.md), and
[completed record](history/completed.md) are preserved unchanged. Original request
files and prior reports remain intact; this revision updates pending work only.
