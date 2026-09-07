# Workflow regression safeguards: independent delta review

Verdict: **ready** at proposal level.
Open finding IDs: **none**.
Next action: the owner may decide whether to authorize the proposed implementation. This review authorizes no implementation or release and does not establish that the safeguards work.

## Scope and input identity

One bounded independent review of the v2-to-v3 delta, focused on the user's new requirements: retain standardized important behavior cases, grading and results as future regression safeguards; defer heavy tests until release rather than require them for every small change. Unchanged design choices and the v2 verdict were not re-reviewed.

Binding input: [v3 manifest](evidence/workflow-v3/manifest.json), baseline `6573f8f422cb6528981ff43bc0d20c656096e7dc`. Manifest SHA-256: `3d33fd85b888772d03d65fc11d5ec80540a1c2257a9f687dac6b0ac51637bd5b`.

| Reviewed file | SHA-256, verified against both current file and v3 archive |
|---|---|
| `workflow-proposal.md` | `7efa5c1a9ab87cfed701e17770a048bc77cecdf98d072d7f78ba745606efb14e` |
| `workflow-validation.md` | `65ddae4dca221acb19956c78ac513ff9fb2e7656b37a7c1f561e061698f5944a` |

The supplied [delta](evidence/workflow-v3/proposal-delta.patch.txt) exactly matches a generated comparison of the archived v2 and v3 documents; its SHA-256 is `958823dfd92d4855dbae39e2b17cb235598d7bb4756d7ac985225d088595159d`. Archive reads served identity verification, not renewed review of unchanged content.

Read repository `AGENTS.md` and the feature-design skill's entrypoint, review operation and review template. Performed static inspection and input hash/diff verification only.

## Findings and dispositions

No material delta problems found. The following concerns are covered by explicit proposal requirements, rather than assumed future behavior:

- **Cadence — covered.** Proposal “Implementation boundaries and evidence” and validation “Regression policy for future prompt changes” distinguish fast commit/PR checks from heavy release coverage. The initial canary increment requires fast controls, not completion of expensive baseline trials before prompt editing. Normal PRs may record heavy coverage as pending; targeted early runs require concrete uncertainty. This fits the requested cadence.
- **Durable regression detection — covered.** Validation “Standardized cases and grading” requires versioned cases, task-derived criteria, evaluator-owned deterministic assertions, separately calibrated semantic judgments and retained attempts/results. Missing or inconclusive required criteria cannot pass; baseline failures cannot excuse candidate failures. Existing historical runs cannot silently become new-grader evidence. These requirements establish a reusable safeguard without treating worker-written tests or test counts as sufficient evidence.
- **Rubric isolation — covered at specification level.** The new standardized-case section separates worker inputs from grader-only criteria, examples and historical conclusions. The trial-design contract explicitly keeps evaluator expectations outside accessible worker inputs. Thus copying grader material into a readable worker fixture would violate this proposal; merely using separate folders would not satisfy it. Semantic grading also excludes the author's desired verdict and baseline/candidate labels.
- **Evidence freshness and proportionality — covered.** The release gate must bind results to candidate, fixture, grader and settings; dependency changes invalidate reused evidence. A post-fix release can reuse unaffected cases only with verified unchanged inputs/dependencies and aggregate coverage of the final artifact. Grading changes require compatible reassessment of both sides. Negative and positive controls cover stale identities, incomplete release coverage and honest PR deferral. Reusing the existing hook runner and disposable local fixtures keeps the proposed machinery bounded.

## Limitations

This is approval of the delta's specification, not runtime validation, human acceptance or endorsement of unchanged v2 choices. No runner, isolation boundary, grader calibration or release gate was exercised. Concrete case budgets, mappings and enforcement remain future implementation work; their correctness cannot be inferred from this review. No source research, private Rover inspection, tests, installations, commits or external actions were performed. Local-link checking and unchanged-tracked-file verification remain with the main author as requested.
