# Actual skill results

**Review candidate; release readiness is blocked.** The four skills were revised, exercised by real agents and independently reviewed. Two targeted repairs have supporting evidence; overall productivity improvement and human usability are unproven. Owner review is pending.

[Use the skills](../../../README.md) · [Goals and cases](../../../evals/GOALS.md) · [Independent final review](../../reviews/outcome-final-review.md) · [Finding dispositions](../../reviews/outcome-dispositions.md)

## Latest results

Each linked status is an original report for the current case and selected skill bytes. `INCONCLUSIVE` means the evaluation did not establish a grade; `DEFERRED` means the final bundle was not rerun. Earlier failures remain in the [complete attempt register](outcome-results.json).

| Development task | Previous skills | Final skills | What the test establishes / limit |
|---|---|---|---|
| `bounded-delivery` v2 | [PASS](20260907T090510-e0640bf3c1ac48fbae25dfec4392a7a6/report.json) | [PASS](20260907T094228-9cae63d40af941b8be555400028d4817/report.json) | Inventory delivery, actual checks/review and accurate final handoff; both pass. |
| `bounded-investigation` v1 | [PASS](20260907T083357-130ffc0a8e31423fbe8c8ab9ded1d958/report.json) | [PASS](20260907T094659-6d7b7192d2a2449db9a83b7544abde58/report.json) | Evidence-based next experiment; both pass. |
| `counter-stage` v1 | [PASS](20260907T090402-1664e48d45bf4fb4b40a06248153eaae/report.json) | [PASS](20260907T090221-d9617806505c41579145df19abada8b9/report.json) | Correct state handling; required human/agent acceptance stays pending. |
| `existing-intake` v1 | [PASS](20260907T090136-e9f9ff66f1594c33b202c5f1e69bbf80/report.json) | [FAIL](20260907T094757-ce99b6e7a1b7402e93107e3d2f08145a/report.json) | Final intake omits explicit error-compatibility clarification; original code preserved. |
| `release-ready` v1 | [INCONCLUSIVE](20260907T091010-8abdb359ca2c44e6a59b742d2318f826/report.json) | [PASS](20260907T095854-155fdbaa011648b1819bac61c9cf4592/report.json) | Synthetic readiness assessment; old scoring quotation is invalid. |
| `release-stale` v1 | [INCONCLUSIVE](20260907T090734-5a79df1e185a46bcad525e9c43c587c4/report.json) | [PASS](20260907T095727-74a08352b2dd44bbb4ea66c867414ca3/report.json) | Synthetic stale-evidence refusal; old scoring quotation is invalid. |
| `review-defective` v1 | [PASS](20260907T084000-a0eb40fca76a46c2bf887c6d5c80b331/report.json) | [PASS](20260907T095057-9357aca7b7fc4ef28d0ae9607ccac1d7/report.json) | Find material contract/dependency and readability defects. |
| `review-ready` v1 | [PASS](20260907T083803-07c4c0591a634ee3afcfa02c7dd171e5/report.json) | [PASS](20260907T095019-40c382652b654e9b9caacd747e731b3f/report.json) | Accept sufficient work without manufactured blockers. |
| `route-local` v1 | [PASS](20260907T092402-902583d3cfff40e1a88c63d6eddaf926/report.json) | [PASS](20260907T095225-753790f4724147848b81bfc711a55bbf/report.json) | Choose a proportionate next step without prescribed workflow. |
| `route-uncertain` v1 | [PASS](20260907T092807-ff5642a36e9c4a34a5a5f7b9b414b010/report.json) | [INCONCLUSIVE](20260907T095332-493e3b8bc66140ac95e4a579b481e4cc/report.json) | Choose bounded work under unmeasured performance uncertainty. |
| `v1-small-feature` v2 | [INCONCLUSIVE](20260907T091520-f558fdf21f704b13899de1b3ced023db/report.json) | [FAIL](20260907T095457-6441a76684304e9dacabed53c78f3084/report.json) | Final first-screen excerpt cuts off the lookup tradeoff; old score remains inconclusive. |
| `v2-scope-extension` v2 | [INCONCLUSIVE](20260907T084545-77792470ee6b483c847a6350fe4c3237/report.json) | [PASS](20260907T093307-869a3e1aa79842b79d2b32ba9949675b/report.json) | Current YAML/scale scope is now recoverable from the opening; targeted OSC01 repair. |
| `v3-maintenance` v2 | [PASS](20260907T095528-b4536438fd5f44019ba79e84ea47c0cc/report.json) | [PASS](20260907T095529-69472bc81f1d4341ab044375f9fce6ca/report.json) | Private change versus public contract; corrected original-file preservation check. |
| `v4-migration-risk` v3 | [FAIL](20260907T091901-572ec8619c5e4a5cbc4d498974adf8f6/report.json) | [FAIL](20260907T094228-a4fb5fdf8c1b492bae4eb21af911f9a2/report.json) | Both fail first-screen recovery comprehension; other five risk criteria pass. |
| `v5-review-recheck` v1 | [PASS](20260907T085347-299c66b0e85c450cabe6663088366c86/report.json) | [PASS](20260907T095550-a96f7005c8524154932e466dcac0d75b/report.json) | Reject incomplete correction; verify complete fix without cosmetic reopen. |
| `v6-execution-handoff` v1 | [FAIL](20260907T090136-e7b5b89b7a6a49568535a0ecf379ecdd/report.json) | DEFERRED | Final bundle not rerun; earlier FAIL is disputed exact commit count (CMR01). |
| `workflow-setup` v2 | [PASS](20260907T092120-d4908cd5b1644a87a7a76c9256532b0a/report.json) | [PASS](20260907T093636-3a4ef47ec46145019ae85aa54bc79a53/report.json) | Existing checks/docs and truthful PR handoff; targeted TRU01 repair passes. |

Counts for final current inputs: **1 deferred**, **3 fail**, **1 inconclusive**, **12 pass**. These are case outcomes, not numbers of AIs or packaging checks.

## What changed usefully

| Skill goal | Observed benefit and remaining limit |
|---|---|
| Understandable design and maintainable plans | OSC01: the older candidate foregrounded the old amendment; the repaired opening exposes the current startup/validation/scale decision and next outcome. Actual reader answers support this local repair. A matched old-baseline grade is inconclusive; small-feature and migration reading still fail. |
| Correct development and useful reviews | Both versions complete the inventory task and distinguish sufficient, defective and incompletely fixed work. No broad review-efficiency improvement is established. |
| Useful setup and truthful delivery | TRU01: the earlier candidate falsely claimed an original baseline check had run; the repaired handoff supports its current checks without that claim. This does not prove that every attempted shell check executes correctly. |
| Proportionate process across skills | Neutral local/uncertain probes test choices without supplying the desired route. A combined note can be useful, but fewer files or a passing grade does not prove less effort or better human readability. |

Inspect actual generated examples: [local next-step note](20260907T095225-753790f4724147848b81bfc711a55bbf/phases/01-plan/workspace/docs/NEXT.md), [extended design](20260907T093307-869a3e1aa79842b79d2b32ba9949675b/phases/02-extend/workspace/docs/DESIGN.md), [extended plan](20260907T093307-869a3e1aa79842b79d2b32ba9949675b/phases/02-extend/workspace/docs/PLAN.md), [completed inventory handoff](20260907T094228-9cae63d40af941b8be555400028d4817/phases/09-handoff/workspace/docs/PLAN.md).

## Method and limits

- Same `gpt-6-astra`, medium effort, 600-second per-call limit, isolated synthetic repositories and frozen baseline `b9087c5`. Case versions, exact prompts, original documents, execution records and scoring evidence are retained with each report. There is no no-skill control or cross-model conclusion.
- A separate reader gets only each selected document's first 30 lines, capped at 2,000 characters, plus questions. This measures supported machine comprehension, not human scan time. Full-document quality is also assessed.
- Inventory worker time was 704.783 seconds for baseline and 619.238 for final skills. The earlier candidate took 566.835. Concurrency and service/tool waits varied; the predeclared same-candidate variability repeat was deferred within the reviewed 220-call ceiling. These observations do not establish a stable speedup. Reader/scorer time is excluded from worker time.
- [Twelve known-output checks](20260907T082604-813e3ca009e44d6cbd680a50b29f49a7/report.json) passed for the scoring prompt. They test the evaluator, not the skills. Invalid literal quotations and one scoring timeout still occurred in actual trials and remain inconclusive.
- Handoff opportunity, migration-reader wording, setup evidence boundaries and history preservation received independently reviewed case corrections. Their changed grades are measurement repairs, not skill improvements. Original outcomes are preserved.
- CMR01, missing compatible old grades, intake and both small-feature/migration reading failures prevent release acceptance. The final snapshot is a reviewed candidate, not an all-green release. No tag, release, global installation or human approval is implied.

Fast checks and the actual release-gate command are recorded separately in the [delivery evidence](../outcome-final/). Fast tests verify packaging/runtime mechanics, not skill quality.

[Historical workflow status, before these real runs](HISTORY-before-outcome.md) · [Raw iteration waves](../outcome-waves/) · [Frozen final skills](../outcome-contract/candidate-v2-final/manifest.json)
