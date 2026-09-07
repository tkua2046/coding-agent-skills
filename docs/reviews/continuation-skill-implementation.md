# Skill implementation — continuation candidate

Implemented the reviewed [continuation scope](../proposals/continuation-repair.md) in the four skill bundles. This is an author implementation record, not independent approval or evidence that the prompts improve behavior. No model trials, commits, pushes or other product changes were performed by this slice.

## What changed

- Design and plan templates now own their substantive artifact contracts and short adaptable examples. Author/reviewer operations reference the same contract. Openings lead with the decision/consequence or next outcome/acceptance, ahead of metadata and history. Original specs remain authoritative.
- Review feedback has the same small contract in each of its three independently usable bundles: identified revision, verdict, actionable finding, original evidence and verified disposition. The two additional owned copies introduce no cross-bundle dependency.
- Four small check resources load after generation, selecting only the relevant section. Supported issues are corrected; unresolved material issues are reported. No self-check report, new agent or recursive review loop is required.
- One existing plan/handoff owns live delivery state; design/spec retain decision/contract status. Relevant snapshots and original records are captured once when needed, then linked. A durable delivery response can record the resulting commit without a self-referential follow-up commit.
- Review/check reuse requires applicable content, requirements, inputs, configuration, runtime and freshness. Required gates and explicit independent rechecks remain mandatory. Resolved findings do not trigger bespoke author verifiers; partial fixes and changed candidates still require the affected invariant to be checked.

Navigator/migration-specific illustrations were replaced with varied display-preference, saved-search, cache-review and notification-handoff examples. Persistent/external-effect failure, activation and safe-retry reasoning remains explicit. Examples establish shape, not mandatory implementation choices.

## Changed paths

All paths below are relative to the named bundle under `skills/`.

| Bundle | Paths |
|---|---|
| feature-design | `SKILL.md`; `prompts/intake-feature.md`, `prompts/draft-design.md`, `prompts/review-design.md`; `assets/design.template.md`, `assets/review.template.md`; new `references/artifact-checks.md` |
| implementation-plan | `SKILL.md`; `prompts/plan-implementation.md`, `prompts/review-implementation.md`; `assets/implementation-plan.template.md`; new `assets/review.template.md`, `references/artifact-checks.md` |
| stage-development | `SKILL.md`; `prompts/execute-stage.md`, `prompts/review-stage.md`; `assets/stage-record.template.md`; new `assets/review.template.md`, `references/artifact-checks.md` |
| dev-workflow | `SKILL.md`; `prompts/prepare-pr.md`, `prompts/setup-dev-workflow.md`, `prompts/release.md`; `references/documents.md`; new `references/delivery-checks.md` |

The four entrypoint names and invocation metadata are unchanged. Six small resources were added while repeated operation prose was removed; total Markdown text remains approximately unchanged. This is a packaging observation, not a readability or speed score.

## Actual static validation

| Command/check | Observed result |
|---|---|
| `.venv/bin/python tools/check.py` | Exit 0: metadata, bundle resources, discovery and documentation links pass |
| `.venv/bin/python -m pytest tests/test_check.py -q --no-cov` | Exit 0: 30 passed in 3.34 seconds, including independent-copy portability and broken-resource controls |
| Skill creator `quick_validate.py` on each of the four bundles | All exit 0: `Skill is valid!` |
| `git diff --check -- skills` | Exit 0 |
| Compare the three owned review templates | Byte-identical feedback semantics |

These checks establish resource integrity and portability only. The primary task owns frozen-candidate smoke/full behavior trials and independent review; Raman owns grader/runtime and intake/V6 case edits. No changes to those areas are included here. Keep this candidate fixed while its behavior is evaluated, and address any supported findings through the coordinated next revision.
