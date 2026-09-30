# feature-design — specification

**Function:** clarify requirements; draft/amend design decisions; review a design.

**Goals:** correct decisions that a reader can grasp quickly, with proportionate time and context cost.

**Non-goals:** implementing code, delivery sequencing, exhaustive implementation/test inventories or mandatory new documents.

## Operations and expected output

**Runtime prompts revised; production case rubrics still use the older binary scheme.** Four operations have scoped numeric pilot results in [validation](../VALIDATION.md). Do the requested operation, then organize its result for reading and deliver. This final editing step belongs to the task; it is not another review cycle. The questions below describe useful information, not mandatory fields or ordering.

| Operation | Result to produce | P1 dimensions to score |
|---|---|---|
| Intake / investigate | Confirmed behavior and material unknowns; resolve what available evidence settles and expose the owner's remaining choice. | A1, A2, A6; A3 when an investigation must establish a consequential external guarantee. |
| Draft design | An implementable choice with reasons, consequences and examples that distinguish important behavior. | A1, A2, A3, A6. |
| Amend design | Updated affected decisions, preserving unrelated accepted behavior and the original source. | A1, A2, A3, A4, A6. |
| Initial review | Supported verdict and actionable material findings against the actual design. | A5, A2, A6. A5 evaluates A1/A3/A4 in the supplied design; the reviewer need not author it. |
| Recheck | Evidence-bound disposition of the original concern at the new revision; complete fixes close, partial fixes remain open. | A5, A2, A6. |

Example of needed specificity: with the adjacent cell occupied, blocked forward reports failure and preserves the whole pose; later commands follow the agreed continuation policy. “Handle obstacles gracefully” is insufficient.

## Goals and rubrics

Select dimensions from the operation above before execution. All selected rows are **P1**, with a usable threshold of **3**; 4/5 describe benefits, not more required work. Shared [scoring, veto and time rules](evaluation.md) apply. These examples are anchors, not prescribed answers.

| ID · priority | 1 / 2 — needs repair | 3 — usable | 4 / 5 — additional benefit within scope |
|---|---|---|---|
| A1 · P1 Contract | **1:** solves a different contract. **2:** silently chooses between incompatible promises or stalls on already-settled facts. | Preserves confirmed behavior, separates assumptions, and asks only consequential unresolved questions. | **4:** makes the owner's tradeoff directly answerable with a consequence. **5:** resolves an apparent conflict from authoritative supplied facts, avoiding an unnecessary interruption. |
| A2 · P1 Usability | **1:** reader cannot determine the choice/verdict. **2:** must reconstruct it from history or reconcile contradictory summaries. | Reader quickly finds the choice or verdict, its reason and material consequence; examples/detail are accessible where needed. | **4:** concise opening and navigation support both a quick decision and deeper inspection. **5:** explains a subtle consequence immediately through a well-chosen example without extra reading burden. |
| A3 · P1 Adequacy | **1:** chosen mechanism cannot satisfy the request. **2:** omits a consequential failure/retry behavior or relies on an unsupported guarantee. | Choice, reason, tradeoff and decisive behavior are sufficient to implement; evidence limits are clear. | **4:** a counterexample explains why the boundary matters. **5:** resolves interacting constraints with a simpler supported choice while preserving required recovery/compatibility. |
| A4 · P1 Maintenance | **1:** loses accepted behavior or original requirements. **2:** local extension creates contradictory decisions or needless parallel authoritative designs. | Updates affected decisions/examples, retains unrelated accepted work; separate documents have a real ownership/lifecycle/risk need. | **4:** affected and unchanged boundaries are easy to inspect. **5:** removes an existing decision duplication without changing scope or losing provenance. |
| A5 · P1 Review | **1:** approves a known-broken design or fabricates verification. **2:** misses a material concern, blocks over style, or closes only a partial fix. | Correct verdict, actionable finding and revision-bound [closure](evaluation.md#review-closure); accepts sufficient work. | **4:** minimal counterexample and correction make the finding immediately verifiable. **5:** resolves interacting findings with a smaller coherent correction and no unnecessary round. |
| A6 · P1 Time/context | **1:** operation never reaches a usable result or consumes extreme avoidable work. **2:** repeats settled design/research or misses the declared target. | Completes within the operation's target with relevant investigation and one final readability edit; shared time anchors apply. | **4:** reuses applicable decisions/evidence with observable saved work. **5:** handles the task's real uncertainty while avoiding otherwise necessary repeated context reconstruction; no unproved speed claim. |

**P2:** exact headings, paragraph order, optional alternatives lists, preferred example layout and a redundant next-action sentence after a complete answer. The final editing step may improve these; they cannot block an otherwise understandable result. If an absent reason/example prevents understanding a consequential choice, score A2/A3 instead. A different surface form with the same useful content should receive the same core score.

## Cases → rubric requirements

The mappings below identify existing behavioral cases. Their executable rubrics still have the old binary wording; priority/anchor migration is pending in [evaluation contracts](../../evals/CONTRACTS.md). Definitions are separate from actual worker results.

| Case / input | Required judgments |
|---|---|
| `smoke-intake-preserve` / `smoke-intake-conflict`: settled defaults versus incompatible promises | A1/A2/A6. Reuse `resolved-default` / `real-decision`; add role-specific opening and effort judgments. |
| `v1-small-feature` → `v2-scope-extension`: obstacles, then confirmed YAML/large-input scope | A1–A4/A6. Reuse `preserve-intent`, `decisions`, `first-screen-comprehension`, `phase-02-scope`, `phase-02-tradeoffs`; preserve real added scope and assess unnecessary work separately. |
| `smoke-transfer-design`: interruption/retry in a different domain | A2/A3/A4/A6. Extend `proportionate-adequacy` with attributable support for consequential guarantees; retain required recovery detail. |
| `review-ready` / `review-defective`: sufficient versus validation-defective design | A2/A5/A6. Reuse `actionable-static-verdict` and substantive criteria; explicitly judge review opening and whether another round is warranted. |
| `v5-review-recheck`: partial then complete design correction | A5/A6. Reuse `phase-01-incomplete`, `phase-02-corrected`, `review-history`, `review-boundary`; this is design review, not code-review evidence. |

Owner feedback: F1/F2/F4/F5/F6/F11/F12. [Cross-skill tests and coverage](evaluation.md).
