# stage-development — specification

**Function:** implement a bounded outcome, run applicable checks, fix substantive findings and hand off; alternatively perform a review-only task.

**Goals:** correct working behavior, trustworthy verification, convergent review and continuation without repeated work.

**Non-goals:** automatic design/planning phases, unrelated refactoring, invented approval, bypassed required reviews or release.

## Expected output

**Runtime prompts revised; production executable rubrics still use the older binary scheme.** Scoped local trials and remaining limits are recorded in [validation](../VALIDATION.md). Complete the requested implementation/review operation, then make its outcome and remaining action easy to read. This final edit does not rerun unchanged checks or create another review. One existing record or the response owns current progress.

| Operation | Result to produce | P1 dimensions to score |
|---|---|---|
| Implement | Working scoped diff, meaningful checks and affected docs; truthful readiness and remaining review. | C1, C2, C4, C5; C3 when review/closure is part of the request. |
| Initial code review | Correct verdict and actionable findings tied to code, trigger, consequence and evidence limits. | C3, C4, C5; C2 only for verification the review was asked to execute. |
| Fix supplied finding | Correct the whole affected behavior, preserve compatibility and verify the actual change. | C1, C2, C4, C5. Author-reported repair is not independent closure. |
| Recheck | Original concern stays open for a partial fix and closes for a verified full fix on the identified revision. | C3, C4, C5; C2 where recheck requires running checks. |
| Resume | Reuse applicable evidence; check changed behavior and continue from actual remaining work. | C2, C4, C5; C1 for new implementation and C3 for requested review. |
| Handoff only | Accurate current outcome, evidence limits, open concerns and next action without replaying history. | C4, C5. No new implementation or gate execution merely to format a handoff. |

Example: “R1 remains open: heading is preserved but blocked movement changes coordinates. Preserve the whole pose and verify a subsequent command.” A later complete fix closes R1 at its new revision.

## Goals and rubrics

Each selected dimension is **P1**; **3 = usable**. Apply [shared scoring/time rules](evaluation.md). A review may correctly reject broken supplied code and still score highly: its task is to detect the defect, not implement the fix.

| ID · priority | 1 / 2 — needs repair | 3 — usable | 4 / 5 — additional benefit within scope |
|---|---|---|---|
| C1 · P1 Behavior | **1:** central behavior absent or destructive. **2:** partial-state mutation, broken compatibility or meaningful required behavior unimplemented. | Scoped behavior and relevant failure/recovery invariants work; tests derive expectations from the contract. | **4:** targeted boundary regression explains and prevents a real defect. **5:** a simpler repair resolves coupled state errors with clear independent behavioral evidence and no extra abstraction. |
| C2 · P1 Checks | **1:** claims success despite demonstrated required-check failure. **2:** missing required execution, zero discovery treated as success or stale candidate evidence. | Required/affected gates actually run or applicable prior evidence is justified; failures and hook edits are inspected and reported accurately. | **4:** checks clearly exercise the consequential failure path. **5:** focused independent verification resolves a subtle propagation/state issue without redundant suite runs. |
| C3 · P1 Review | **1:** wrong approval or invented independent verification. **2:** misses whole-state defect, closes only a partial fix, loses a material finding or blocks over style. | Supported verdict, actionable findings, truthful review mode and revision-bound full-fix dispositions. | **4:** minimal trigger and consequence make the correction easy to verify. **5:** resolves coupled concerns through one coherent correction while retaining the original failed evidence. |
| C4 · P1 Continuation | **1:** handoff directs work from a false state. **2:** pending review presented as complete, open findings lost or next action buried in conflicting records. | Reader quickly sees what works, observed checks, material remaining work and where to resume; complete tasks need no invented next step. | **4:** a new context can continue from precise current evidence links without conversation replay. **5:** resolves an existing stale/contradictory handoff into one concise authoritative state. |
| C5 · P1 Time/context | **1:** extreme avoidable cycles prevent delivery. **2:** repeats unchanged gates/reviews or reloads history without a consequential reason; misses declared target. | Completes within target using required/affected checks and requested reviews, then a short readability edit. | **4:** applicable evidence reuse demonstrably avoids repeated work. **5:** preserves required verification through a complex resumption without costly replay or unnecessary coordination. |

**P2:** a particular review table, exact disposition labels, handoff headings, test-count summaries and optional before/after examples when behavior is already clear. The actual finding state and evidence remain essential; alternate wording is fine. The final readability step may tidy these without another check/review cycle.

## Cases → rubric requirements

| Case / input | Required judgments |
|---|---|
| `counter-stage`: implementation with real gates and pending reviews | C1/C2/C3/C4. Reuse `real-execution`, `pending-review`, `handoff`; add handoff-opening questions. |
| `smoke-review-partial`: incomplete code fix; `v6-execution-handoff`: code review → fix → recheck | C3/C5. Reuse `whole-invariant`, `review-history`, `phase-02-review`, `phase-04-recheck`; verify closure at the actual code revision. V5 is design-only and cannot establish code-review coverage. |
| `smoke-stage-resume` / `smoke-stage-stale`: unchanged versus changed candidate | C2/C3/C4/C5. Reuse `reuse-and-check` / `changed-candidate`; unchanged review may apply, changed behavior needs recheck. |
| `smoke-handoff-opening`: current state buried under policy | C4/C5. Reuse `usable-entry`, `one-truthful-record`; expose next action without duplicate status or excluded implementation. |
| `transfer-transcript-search` / `transfer-packet-import`: complete local feature versus consequential file recovery | C1–C5. Reuse functional and handoff criteria; preserve failure/retry correctness and assess additional work by its purpose. |

Owner feedback: F1/F2/F4/F5/F6/F8/F12. Behavioral mappings exist in case rubrics; the new priorities/anchors are not yet executable. [Validation](../VALIDATION.md) records what actually ran.
