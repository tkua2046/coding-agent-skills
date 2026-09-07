# What these tests must establish

Status: revised contract for the outcome-driven iteration. [Run instructions](README.md) · [Decision and iteration rules](../docs/proposals/outcome-workflow.md) · [Results](../docs/validation/canary/INDEX.md).

**Success means usable decisions and correct delivery with proportionate effort.** File counts, headings, coverage percentages and passing packaging tests do not establish that outcome. Each goal below has required case-specific criteria; quality acceptance and observed improvement are reported separately.

| Goal | User-visible success | Cases / decisive failure |
|---|---|---|
| FD1 — Understand the task | Existing code and original requirements inform clarification; evidence resolves material uncertainty | `existing-intake`, `bounded-investigation`, `route-uncertain`: fails on invented scope, unsupported performance claims, or architecture before investigation |
| FD2 — Make design understandable and adequate | A new reader finds the behavior, choice, consequence and next action; relevant risks remain explicit | `v1-small-feature`, `v2-scope-extension`, `v4-migration-risk`, `bounded-delivery`: restricted reader cannot recover the decision, or design omits the relevant invariant/recovery |
| IP1 — Make work executable | An implementer can select the next coherent outcome and understand dependencies and acceptance | The same four planning cases: function/test inventory obscures delivery, a dependency is missing, or the reader cannot find the next outcome |
| IP2 — Keep the plan maintainable | Internal edits stay with code/tests; changed behavior updates the affected decisions and pending work | `v3-maintenance`: rewrites completed work, duplicates a new test in the plan, or leaves contradictory public contracts |
| SD1 — Deliver correct checked behavior | Real implementation meets independently derived behavior checks and uses effective existing gates | `counter-stage`, `v6-execution-handoff`, `bounded-delivery`: partial state mutation, missing test assertions, bypassed/false check result, or premature acceptance |
| SD2 — Review usefully and converge | Review catches material issues, accepts sufficient work, verifies complete fixes and enables continuation | `review-ready`, `review-defective`, `v5-review-recheck`, `bounded-delivery`, `v6-execution-handoff`: invented blocker, missed contract/reading issue, partial-fix closure, or repeated cosmetic cycle |
| SD3 — Resume without repeating finished work | A fresh context identifies current work, open issues, evidence and actual acceptance state | `v6-execution-handoff`, `bounded-delivery`: stale claims, forgotten blocker, reopened completed stage or fabricated human assent |
| DW1 — Adapt a useful development environment | Existing tools remain useful; actual gate failures propagate; users and contributors can find their own instructions | `workflow-setup`: broken/ineffective hook, unnecessary stack replacement, polluted README, lost useful documentation or unsupported setup claim |
| DW2 — Make delivery reviewable and truthful | Local PR text explains the actual impact/checks; release readiness matches current evidence and authorization | `workflow-setup`, `release-stale`, `release-ready`: PR is a log dump, evidence is stale, scope/version churn is invented, or ready/not-ready is assessed incorrectly |
| ALL — Spend effort where it matters | Local understood changes use a short path; uncertainty prompts investigation; serious consequences receive adequate analysis | `route-local`, `route-uncertain`, `bounded-delivery`, `bounded-investigation`, `v4-migration-risk`, `review-ready`: unnecessary workflow machinery, premature architecture, missing safety reasoning, or failure of an explicit task-local budget |

## How evidence is obtained

- **Runtime correctness:** evaluator-owned executable behavior checks, separate from the worker's tests. Existing isolated hook trials additionally exercise copied tooling; they are not LLM skill results.
- **Decisions, maintenance and review:** independent scoring of each case's actual outputs/transcripts against predeclared criteria, with literal supporting evidence. Known outputs separately test the scoring prompt, including acceptable work that must not be rejected.
- **Quick comprehension:** a separate reader sees the actual first 30 lines, capped at 2,000 characters, of each named document and questions without answers. Its answer must be supported by those excerpts. This fixed exposure is a reproducible proxy; human scan time and satisfaction await owner review. Full-document navigability and correctness are also assessed.
- **Effort:** record executed/skipped phases and worker elapsed time; compare repeated review findings and document changes. Exclude reader/scorer work from development time and report evaluation overhead separately. The local delivery's 900-second allowance and investigation's 300-second allowance are fixture user constraints, not general speed standards.

## Interpretation and safeguards

For each goal, report quality as pass/fail/inconclusive and benefit against the frozen prior version as improved/unchanged/tradeoff/unresolved. A faster incorrect result fails. All-green but equally burdensome work is unchanged. A good machine-reader result does not claim human approval. One paired run is not a statistical productivity benchmark. The originally planned local-delivery variability repeat was explicitly deferred at the [reviewed scope checkpoint](../docs/reviews/outcome-scope-checkpoint.md); no complete additional pair could be reserved within the experiment ceiling. Comparing changed candidates is not that repeat.

Task-local budgets and semantic failures stay visible. Correcting evaluation infrastructure never counts as improving a skill. Every attempted run is retained; a failure gets a disposition and a justified affected rerun. Case/grading changes require compatible baseline/candidate evaluation. See the proposal for cumulative iteration limits and independent global checkpoints.

Coverage limits: these are bounded synthetic repositories, not full production deployments, all language ecosystems, or a model benchmark. Explicit supplied paths test skill execution; they do not establish automatic discovery. The local-delivery case uses inventory allocation, outside the navigation examples embedded in the skills, to check transfer. No external push/tag/release is performed.

The two neutral planning probes were added after independent global review found that execution cases substantially prescribed their desired route. They reuse existing applications and leave the next commitment open; see the [reviewed contract](../docs/reviews/outcome-routing-review.md). Corrected handoff and migration-reader cases retain their original disputed results in the [dispositions](../docs/reviews/outcome-dispositions.md).
