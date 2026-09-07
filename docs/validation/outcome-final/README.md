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

Git delivery uses `codex/workflow-canary` and the existing draft PR. The actual commit runs hooks again. Delivery/CI observations are added after those actions occur; their success is not implied by the pre-commit result above. No merge, tag, release or global installation is authorized by this record.
