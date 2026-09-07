# Reviewed candidate and delivery checks

The four skills are a review candidate. **Release readiness fails; owner approval is pending.** Start with the [skill results](../canary/INDEX.md) and [independent final review](../../reviews/outcome-final-review.md).

| Check | Actual outcome | Original record |
|---|---|---|
| Final skill cases | 12 pass, 3 fail, 1 inconclusive, 1 deferred at current inputs | [Case records and previous versions](../canary/outcome-results.json) |
| Complete local pre-commit gate | Passed; 187 mechanical tests, tools coverage 92%, all hooks passed | [Original command/output and staged tree](pre-commit.json) |
| Behavior release gate | Exit 1; nine matched acceptable comparisons, eight missing | [Original command/output](release-gate.json) |
| Independent skill / result review | Static scope and bounded claims reviewed; owner review remains pending | [Review and follow-ups](../../reviews/outcome-final-review.md) |
| Experiment limit | 208 recorded fresh CLI calls + 2 outside-catalog smokes + 1 conservative abort reserve = 211 / 220 | [Definition and execution paths](cli-call-ledger.json) |

The mechanical suite checks bundle/document integrity and evaluator/runtime safeguards; it is not 187 skill-quality tests. The CLI ledger excludes independent reviewer agents and is not token/cost/total-model accounting.

The final candidate is retained in [its original snapshot](../outcome-contract/candidate-v2-final/manifest.json). Original unsuccessful runs, intermediate candidates and case corrections remain available. The snapshot ZIP retains incidental ignored metadata; actual worker-input identities are in individual run reports.

The reviewed skill commit is `e017ce09592e41fcdf523df922d1a51d5081fac7` on `codex/workflow-canary`. Its [actual commit hooks](commit.json) passed; its [push](push.json) updated only that branch and verified main remained `d384cddd080c881a56bc9d9ba378c4e69a1d31d3`. The [PR snapshot](pr.json) records the existing [draft PR #1](https://github.com/tkua2046/coding-agent-skills/pull/1).

Both candidate CI runs passed: [observed statuses](ci-e017ce0.json), [original PR-job log](ci-e017ce0.log.txt), [GitHub run](https://github.com/tkua2046/coding-agent-skills/actions/runs/34114568720). A subsequent documentation-only commit records these observations and has its own commit/CI checks visible through the PR; it does not change the tested skills, cases or engine. No merge, tag, release or global installation occurred.

The [staged-blob audit](staged-evidence.json) verified every report-declared original against Git, including 123 paths initially omitted by ignore rules. The [diff preflight](diff-preflight.json) retains the unfiltered whitespace result and the scoped pass: original output/fixture whitespace is preserved under the established formatting exclusions. [Display-attribute checks](diff-attributes.json) establish local matching, not complete web-diff rendering.
