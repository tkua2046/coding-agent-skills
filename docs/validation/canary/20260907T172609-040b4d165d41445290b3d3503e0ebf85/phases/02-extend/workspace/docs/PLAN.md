# Plan

Next deliverable: load the YAML starting pose and fixed occupancy completely before
movement, then navigate using the retained in-memory index. First resolve the
[open contract questions](SPEC.md#proposed-yaml-contract-and-open-questions) and the
parser/dependency conflict with DEVNOTES. Decisive acceptance is loading
`examples/start.yaml` and processing FFRF to (1, 0, 1) with
[False, False, True, True]; malformed structure, including the last cell in a large
file, must fail before any command is consumed. This extends the existing pending
S1 rather than reopening completed S0.

## Pending outcome

| Outcome / scope | Dependency and boundary | Acceptance evidence |
|---|---|---|
| S1: deliver YAML startup plus optional programmatic occupancy, collision failure and continued commands. Include implementation, meaningful tests, README loading/error usage and DEVNOTES dependency/check instructions together. | Depends on resolving schema/value/duplicate and YAML-feature rules, public loader/error shape, and parser policy. Select and verify a maintained parser only in a later authorized implementation phase. One coherent future change boundary gives a usable file-to-movement path; a loader alone would not meet the request. No partial release is planned. | Preserve the existing regressions and all [spec examples](SPEC.md#acceptance-examples). Verify full validation before command iteration (including a malformed final record), clear syntax/schema/I/O failures and successful corrected-file retry. Verify immutable configuration reuse, mutable caller isolation, one-shot occupied iterables, repeated collision recovery, and independent runs. Exercise a representative 200,000-distinct-cell file: record startup and peak/retained memory, verify repeated membership queries and multiple runs do not reread the file or rebuild the index. Add agreed value/duplicate/YAML-feature cases once settled. |

No resource budget is specified. Scale evidence must show whether the proposed
parser/tree/set startup fits the intended environment; an unacceptable measured
peak would reopen loading strategy before acceptance. Do not invent a numeric
performance gate or claim scale feasibility from the three baseline tests.

Sources: [original](ORIGINAL.md), [occupied request](OCCUPIED_REQUEST.md),
[YAML request](YAML_REQUEST.md), [design](DESIGN.md), [target spec](SPEC.md).

## Execution and review policy

Follow [AGENTS.md](../AGENTS.md) and [DEVNOTES.md](../DEVNOTES.md).
The standard gate is `python3 -m unittest discover -s tests -v`; use the prepared
runtime command recorded below in this fixture. Inspect the eventual diff for
contract, scope and documentation consistency. The fixture specifies no additional
review approval or hook gate. Self-checks are not independent review or human
acceptance. This phase authorizes documents and local evidence only: no
implementation, commits, installation or external actions. S1 checks above are
planned, not performed. Any later dependency-policy change must be explicit in
DEVNOTES and the chosen installation metadata; do not silently bypass its current
standard-library-only constraint.

## Delivery status

- S0 complete: basic translation and turns, accepted as D1. Existing navigation
  tests cover turns and movement. This completed outcome is retained in the
  [historical record](history/completed.md); the [previous plan](history/pre-occupied-documents.md)
  stated no pending stages before this request.
- S1 pending, revised to include YAML startup and in-memory occupancy; no implementation
  has been performed. S1 awaits resolution of the proposed contract and parser policy.
  README continues to describe the implemented API.
- Baseline verified on 2026-09-07 with
  `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`:
  all 3 existing tests passed (exit 0). This is baseline evidence only, not
  occupied-cell acceptance.
- Inspected navigator.py, tests/test_navigator.py, README, DEVNOTES, AGENTS and
  fixture file/check configuration. No additional check configuration was found.
  Read-only Git inspection returned revision
  cab0e6fb96fd7e5731dde0960e61440ae2b0b7a7 and no status entries before edits,
  but emitted sandbox cache/global-ignore warnings; it is not additional test
  evidence.

Original requirements and confirmed request remain unchanged. The
[pre-amendment document capture](history/pre-occupied-documents.md) preserves
the prior specification, accepted design and completed plan text without
relabeling them as acceptance of occupied-cell behavior.

## YAML amendment evidence and review status

- Fresh-context inspection on 2026-09-07 read the fixture guidance, supplied skills,
  requests, example, current documents, navigator.py and its tests. The baseline
  command `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v`
  again passed all 3 tests (exit 0). No YAML parsing or scale measurement was run.
- Initial Git status already contained modified SPEC/DESIGN/PLAN and untracked
  request/example/history files. These prior changes were preserved. Git emitted
  sandbox cache/global-ignore warnings.
- [Pre-YAML document capture](history/pre-yaml-documents.md) retains the preceding
  proposals and full baseline report verbatim. Older historical reports remain unchanged.
- Design and plan author self-checks completed for this amendment. Independent
  design review, plan review, code review and new human acceptance remain pending;
  historical D1 acceptance does not cover occupancy or YAML.
- This phase changed documents only. No dependency installed, implementation
  performed, commit created or external action taken.
