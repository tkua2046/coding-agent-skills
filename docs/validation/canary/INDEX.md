# Actual skill results

**Revised candidate for owner review; release acceptance remains pending.** The four skills now share author/reviewer artifact contracts, adaptable templates and silent after-generation checks. Small LLM tests exercise individual responsibilities. Passing a scorer is not by itself proof of useful work or a productivity gain.

Current-input automatic results: smoke — 16 pass; heavy — 1 inconclusive, 11 not-run-current, 5 pass. Not-run-current includes unrun cases and older tested bundles; the tables below keep them distinct from matching passes.

[Use the skills](../../../README.md#artifact-guides) · [Goals](../../../evals/GOALS.md) · [Findings and corrections](../../reviews/continuation-dispositions.md) · [Original attempt register](continuation-results.json)

Read actual generated artifacts: [local design](20260907T172024-7082e5a00d93484ab19c02eac5db047e/phases/01-plan/workspace/docs/DESIGN.md), [delivery plan](20260907T172024-7082e5a00d93484ab19c02eac5db047e/phases/01-plan/workspace/docs/PLAN.md), and [review that keeps a partial fix open](20260907T175554-99cefee4409b4731a8172dfa0f312680/phases/01-operation/workspace/REVIEW.md). These are original worker outputs, not polished replacements.

## Small operation tests

Each case uses one fresh worker and a separate blind scorer. These statuses match the current case and selected skill bytes. Earlier failed or inconclusive attempts remain in the register; they are not overwritten.

| Responsibility test | Previous skills | Current skills |
|---|---|---|
| Make a row-limit decision usable ahead of accepted history | [PASS](20260907T164442-ad99c0bc9c914adeb5847181c8203cac/report.json) | [PASS](20260907T164440-e93ba43deedd44ac88e3fe67bd08c8a5/report.json) |
| Expose current handoff state before retained policy and history | [PASS](20260907T180818-6c87c8a499ea469b8c018a47b8f052d3/report.json) | [PASS](20260907T180819-02a11cfd69c64c7ea3d6883356ab140f/report.json) |
| Identify an actual Unicode compatibility conflict | [PASS](20260907T164442-2c839831035840ff9bc4c7ed7b1ece64/report.json) | [PASS](20260907T164440-3ee6ec2a13bc4123be0aac2b23e3d9e6/report.json) |
| Resolve prefix API scope without reconfirming compatibility | [PASS](20260907T164628-6b4cf51ed8c44138bfebb43a9538f36a/report.json) | [PASS](20260907T164636-edf95d48bd634588ba60a199e9d50b8f/report.json) |
| Plan a compatibility transition around useful delivery boundaries | [PASS](20260907T164647-ed30f95675d2465ea3f6c1d8583b0887/report.json) | [PASS](20260907T171953-2907b948c86c47f79ca532f832bbdcbc/report.json) |
| Leave accepted planning decisions stable during an internal edit | [PASS](20260907T164833-5d0a3f93934d4abb9b9d75dfe92bea1e/report.json) | [PASS](20260907T171953-dc8b73049678497eaf7a164c7cd8b891/report.json) |
| Plan a read-only CSV preview before confirmed import | [PASS](20260907T171332-0bfe08cafd5d475c8738228c57196250/report.json) | [PASS](20260907T172143-8c9b74d886584557a7eae0d8f231093c/report.json) |
| Keep a partly repaired state-preservation finding open | [PASS](20260907T164852-1c2d724df13646ac99aa93b455d564c8/report.json) | [PASS](20260907T181012-6d7518debee5464fa793ced6a8c6ef54/report.json) |
| Accept sufficient design and plan with a useful short verdict | [PASS](20260907T170446-01cae268fe144a2aad7277952940a706/report.json) | [PASS](20260907T172110-927d1892cd894df0a5baf3e417b54979/report.json) |
| Repair a gate without hiding its failing application baseline | [PASS](20260907T175146-5e08334b206745a28544b1b9f692ca0c/report.json) | [PASS](20260907T175147-045f5139dcb7417f8ad70a099e60f47f/report.json) |
| Report partial verification from an archived package-check wrapper | [FAIL](20260907T171556-f27fb1dd043e4b1db478228ad6b7cc91/report.json) | [PASS](20260907T175344-f82051a489ac4ae2bc0d365a99e920df/report.json) |
| Distinguish listed tests from an executed development gate | [PASS](20260907T170642-2080e258e5c14f18b7a2d508c1562869/report.json) | [PASS](20260907T175147-bf23befcbe834cc7a34bf008b06bee7a/report.json) |
| Resume a verified fix and perform only the remaining gate | [PASS](20260907T165201-f622e8000b2449d0913c958e33d139e6/report.json) | [PASS](20260907T180819-4f56dd989c2447a6a9bc7c4ede07efa8/report.json) |
| Do not reuse a ready review after the candidate has changed | [PASS](20260907T165329-75a6b578042b48acaebf891bdca80a40/report.json) | [PASS](20260907T181002-bc6b3afc34a647a896fdc1519fe5308e/report.json) |
| Configuration replacement remains recoverable after interruption | [PASS](20260907T165404-dbff5d00e40a4d57b9b19dd41a01b302/report.json) | [PASS](20260907T165438-4ff826056f6046df83cd015bd25051a1/report.json) |
| A changed current check cannot inherit a previous green result | [PASS](20260907T170944-2c13f189f45c4563ae9d79f7006201aa/report.json) | [PASS](20260907T175412-a5316abda8354044ac3d2d6f18a50012/report.json) |

## Complete workflow evidence

These affected scenarios test interactions, actual code/checks and document reading. “Not run for current inputs” is explicit: a preceding version is not silently treated as the final version.

| Scenario | Previous skills | Current skills |
|---|---|---|
| Inventory rejection from decisions to reviewed working code | [PASS](20260907T172136-f66fbdc7c5944eb6aecaeefe9c073c9a/report.json) | [INCONCLUSIVE](20260907T180820-90405caa55224fc4b13a3a0c261a7b02/report.json) |
| Existing-project intake with a failing legacy expectation | [FAIL](20260907T170551-87988855585e4dd6b614c24e4e6d42f6/report.json) | [PASS](20260907T170531-f8a717d31c264946b578c1e0ef183854/report.json) |
| V1: Plan occupied cells in an existing navigator | [PASS](20260907T172025-e2e577943056454981c1c297c502f682/report.json) | [PASS](20260907T172024-7082e5a00d93484ab19c02eac5db047e/report.json) |
| V2: Confirm YAML pose and large obstacle input | [PASS](20260907T172438-948c8aa567514f5a98bfa53f6454767a/report.json) | [PASS](20260907T172609-040b4d165d41445290b3d3503e0ebf85/report.json) |
| V3: Separate private maintenance from a public contract change | [PASS](20260907T171804-446cb9f7078f46529b87a71e47151bd8/report.json) | Not run for current inputs |
| V4: Design crash-safe settings migration | [FAIL](20260907T170121-22678ace39464cf890206f40be7ecc0e/report.json) | [PASS](20260907T172024-c7f03e138c6e4f7bb5f1b9f0cd49cbd4/report.json) |
| V6: Execute, independently recheck, resume and deliver locally | [FAIL](20260907T171355-605d353e8e0e4dbb8c3b9799aaefeb7a/report.json) | Not run for current inputs |
| Adapt inventory workflow, then prepare its local PR draft | [PASS](20260907T170747-ce482cf4869d44709e3fd4f8025da87b/report.json) | [PASS](20260907T175148-bd4a7742bd9942ebb42c181d00b2c20f/report.json) |

The other complete cases were not rerun for this continuation. Their historical results and all remaining current-input gaps are listed in the [machine-readable index](continuation-results.json) and [previous delivery](HISTORY-before-continuation.md). The final release suite is still required before tagging/publication.

Preceding selected bundles also have a [V3 maintenance PASS](20260907T175555-2f7be4b14beb46d690af28c19f444339/report.json) and a [V6 execution/handoff INCONCLUSIVE](20260907T175340-5d38fd21597f4a18a889bfeacfdf923b/report.json). V6 completed all workers/checks but its scorer timed out; independent [result inspection](../../reviews/continuation-global-review.md) verifies the specific duplication repair without substituting a formal PASS. Both predate the final handoff-opening change and are not exact-final release evidence. They were not repeated solely to refresh the bundle identity; the changed opening behavior is exercised in the current bounded follow-up.

## What the evidence means

- Migration originally failed because the opening called the whole migration next while the first stage only delivered reading support. The corrected plan and restricted-reader answer pass; opening, order and acceptance identify the same first pending outcome.
- Setup reporting exposed unsupported positive and negative claims, including a false gap inside an automatic PASS and a later unsupported pre-edit baseline. The corrected complete setup now passes; [independent original-evidence inspection](../../reviews/workflow-setup-evidence-review.md) verifies its own before/after observations. Earlier erroneous claims and malformed grades remain intact.
- Handoff tests exposed two different problems: repeated unchanged candidate text, then correct state buried below policy/history. Independent review verifies the respective operational and opening corrections in actual complete outputs. The final reader recovers completion and next owner action; this is bounded evidence, not universal productivity or human-usability proof.
- Missing review prerequisites and history-directory equality were case defects. Their reviewed, versioned corrections preserve original failures and original-file protection. A changed grade from those corrections is not a skill improvement.
- First-wave smoke worker medians were 75.74 seconds for the candidate and 76.79 for the baseline; total worker times were 952.14 and 936.49 seconds. Scoring added 572.46 and 547.53 seconds respectively. Concurrent, single-pair timings do not establish a stable speedup.
- Current scoring uses qualified Astra/medium after nineteen calibration controls; interrupted, timeout and unqualified alternative-model attempts remain retained. Calibration tests the scorer, not the skills, and later malformed/incorrect grades still occurred.
- Complete reading probes expose only the first 30 lines, capped at 2,000 characters. They measure supported machine comprehension, not human reading time or owner acceptance.

Frozen versions: [candidate-1](../continuation-contract/candidate-1/manifest.json), [candidate-2](../continuation-contract/candidate-2/manifest.json), [candidate-3](../continuation-contract/candidate-3/manifest.json), [candidate-4](../continuation-contract/candidate-4/manifest.json), [candidate-5](../continuation-contract/candidate-5/manifest.json), [candidate-6](../continuation-contract/candidate-6/manifest.json), [candidate-7](../continuation-contract/candidate-7/manifest.json). Each original run includes its own complete inputs, execution, artifacts and evidence identity. The [independent final assessment](../../reviews/continuation-global-review.md#current-assessment) verifies specific observed repairs; final local gates and staged-original verification are linked below when recorded.

## Local delivery verification

The [staged-original check](../continuation-checks/staged-evidence-20260907T182835Z.json) verifies 30,687 declared evidence/report files from 151 completed reports against their recorded SHA-256 values and actual staged Git blobs. It force-stages those originals where fixture ignore rules would otherwise omit them; no original report is rewritten. This is evidence preservation, not a skill-quality grade.

The [fast mechanical run](../continuation-checks/fast-20260907T175220Z.json) passes 218 tests plus Ruff and case validation. The earlier [staged hook attempt](../continuation-checks/pre-commit-20260907T180043Z.json) ran all tests successfully but failed because a reviewer appended a tracked report during the hook. Its outcome is retained. The [serialized final hook gate](../continuation-checks/pre-commit-20260907T182959Z.json) passed after all writers finished: all hooks and 218 mechanical tests pass, with 94% coverage for tooling code. This is separate from LLM behavior grades.
