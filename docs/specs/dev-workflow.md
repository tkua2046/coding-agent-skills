# dev-workflow — specification

**Function:** adapt setup/document ownership; prepare a PR; prepare or perform an authorized release. Select the requested operation.

**Goals:** working development checks, reader-specific docs and reviewable delivery with accurate evidence and proportionate cost.

**Non-goals:** mandatory scaffolding/tool replacement, invented coverage floors, feature redesign, PR/version per commit or implicit publication permission.

## Expected output

**Runtime prompts revised; most existing executable rubrics retain the older binary scheme.** The prepared-metadata neighbor uses the priority contract. Scoped local trials and remaining limits are recorded in [validation](../VALIDATION.md). Finish the selected operation, then organize the result for its reader. Readability/formatting is the final part of this task; it does not create another review or justify repeating working checks.

| Operation | Result to produce | P1 dimensions to score |
|---|---|---|
| Inspect checks | Supported diagnosis of the observed setup and material gaps; preserve working tools and leave unrequested repairs alone. | D1 inspection, D6. Apply D2/D3 to the accuracy of an in-scope coverage/docs diagnosis, not to demand repair of supplied defects. |
| Repair checks | Repair the requested gap and verify the changed path while preserving effective tools. | D1 repair, D6. D2/D3 only when coverage/docs are affected. |
| Installed hook | Actual installation and delegation in the intended repository, including relevant failure/empty paths. | D1, D6. |
| Coverage | Current application measurement with meaningful source/branch/missing-line reporting and unchanged applicable gate policy. | D2, D6; D1 when runner/hook behavior changes. |
| Document ownership | Users find usage in README, contributors find operations in DEVNOTES, completed impact goes to CHANGELOG, agent rules go to AGENTS; respect useful existing conventions. | D3, D6. |
| PR preparation | Reviewable whole diff and description of final behavior, observed validation and readiness. | D4, D6; D5 for lifecycle actions in scope. |
| Version / notes | Authoritative version and completed impact selected under actual compatibility/repo policy. | D5 preparation, D6. No tag/publication implied. |
| Release readiness | Honest readiness of the exact candidate with remaining evidence/approval conditions. | D5 readiness, D6. No release execution implied. |
| Release execution | Authorized, verified association between candidate, version, tag, artifact and observed publication. | D5 execution, D6. |
| Retry decision | Distinguish matching completion, conflicting identity and unknown state; take only justified authorized action. | D5 retry, D6. Supplied observations do not prove live acquisition. |

## Goals and rubrics

Selected dimensions are **P1**, with **3 = usable**. D1 distinguishes inspection from repair; D5 is scoped to the selected lifecycle responsibility. An accurate report of a broken supplied setup can fully satisfy inspection. Judge the agent's diagnosis and evidence, not whether it fixed that system. The same distinction applies when inspecting coverage/doc ownership. Shared [veto, evidence and time rules](evaluation.md) apply; readiness-only tasks do not need execution evidence for actions they were not asked to perform.

| ID · priority | 1 / 2 — needs repair | 3 — usable | 4 / 5 — additional benefit within scope |
|---|---|---|---|
| D1 · P1 Setup | **1:** inspection falsely calls a demonstrably broken gate working; or a requested repair cannot run/suppresses failures. **2:** diagnosis overlooks a material gap or infers installation from YAML; repair misses relevant failing/empty propagation or needlessly replaces an effective stack. | **Inspection:** supported state/gap diagnosis, with configured/installed/executed facts distinct; no repair required. **Repair/install:** changed path works in the actual environment, relevant failures propagate and commands are accessible. | **4:** evidence clearly locates a subtle wrapper/hook boundary. **5:** inspection explains interacting symptoms through their common evidenced cause; repair resolves that cause with less machinery while preserving policy. |
| D2 · P1 Coverage | **1:** wrong application measured or results invented. **2:** misses executed application initialization/subprocess paths, hides consequential gaps or changes threshold without justification. | Measures requested application execution, preserves real gate policy and exposes usable coverage/gap evidence; no inference of quality from percentage alone. | **4:** explains the consequential uncovered behavior with independent evidence. **5:** reveals a misleading measurement boundary and makes it accurately observable without metric gaming or extra machinery. |
| D3 · P1 Documents | **1:** essential usage is lost. **2:** instructions conflict or readers must sift through development logs to run the product. | Each audience quickly finds accurate instructions with one maintained owner; useful history and links survive moves. | **4:** a practical example and concise navigation make first use easy. **5:** removes existing cross-document contradictions while reducing maintenance and preserving needed detail. |
| D4 · P1 PR | **1:** description/diff represents the wrong work. **2:** stale readiness, unrelated files or raw archives make the actual change hard to review. | Whole diff serves the task; reader quickly sees actual behavior, meaningful checks and remaining conditions; evidence remains retrievable. | **4:** a concrete trigger/result makes the consequence clear. **5:** makes a complex authorized change readily assessable through concise scope/risk explanation, without dumping history. |
| D5 · P1 Lifecycle | **1:** wrong candidate/artifact or fabricated publication. **2:** preparation notes/version disagree, readiness uses stale evidence, or retry treats unknown state as success. | **Preparation:** policy-based version/completed notes. **Readiness:** exact candidate with honest gaps. **Execution:** verified tag/build/artifact and authorized observed state. **Retry:** inspect identity/status and preserve conflicts. Score only the requested part. | **4:** makes the relevant compatibility or retry consequence immediately clear. **5:** resolves a real cross-step ambiguity using existing evidence/state while avoiding duplicate publication or ceremony. |
| D6 · P1 Time/context | **1:** extreme avoidable setup/release loops prevent delivery. **2:** rebuilds effective tools or reruns unaffected costly suites; misses declared target. | Meets target with actual required/affected checks, reuses adequate setup and finishes with a useful readable report. | **4:** existing commands/evidence remove demonstrated setup work. **5:** resolves the actual environment/lifecycle uncertainty without rebuilding or replaying unrelated history. |

**P2:** exact README section names, report field order, repeating an accessible DEVNOTES command in the final reply, and optional numeric summaries when linked results already make the outcome clear. A missing usable command, materially misleading measurement or hidden release blocker remains P1. Explicit task-required machine formats are assessed as functional requirements, not cosmetic preferences.

## Cases → rubric requirements

These are existing behavioral contrasts; priority/anchor migration of executable cases is pending. P0 scope violations (for example, an unrequested push/tag/publication) remain separate from ordinary lifecycle quality.

| Case / input | Required judgments |
|---|---|
| `workflow-setup`: existing Python gate and mixed docs | D1/D2/D3/D6. Reuse `effective-existing-gate`, `coverage-and-scope`, `document-audiences`; add setup-opening and effort judgments. |
| `smoke-setup-evidence` / `smoke-setup-child-evidence` | D1/D6. Actual current execution, not file listing or unsupported child-result claims; preserve useful tooling. |
| `smoke-transfer-pr` / `smoke-pr-scope`: stale checks; required CSV plus unrelated preview | D4/D5/D6. Reuse `freshness-and-truth`, `reviewable-pr`, `whole-deliverable`, `evidence-and-boundaries`; explicitly assess PR opening/readiness. |
| `release-ready` / `release-stale`: current versus stale candidate evidence | D5/D6. Reuse `candidate-identity`, `readiness`, `evidence-limits`, `scope`; recognize sufficient readiness without inventing extra gates or publication. |
| `local-release-execution`: prepare version/notes, tag/build, then inspect retry/conflict variants | D5/D6. [Defined inputs and evidence](evaluation.md#release-execution); exercise permitted local actions and simulated publication state. Existing readiness-only cases retain their no-tag/no-metadata-change scope. |

Owner feedback: F1/F2/F6/F7/F8/F11/F12. Repository-maintainer testing/research duties live in the [evaluation specification](evaluation.md), not every downstream setup task.
