---
name: stage-development
description: Implement a bounded change with appropriate validation and required review, independently review code, or prepare a status-only handoff. Use for direct implementation, planned stages, focused code reviews and delivery status.
---

# Stage development

Deliver the requested working change or review, then make the result easy to use. Read only the selected operation and relevant context; sufficient requirements can support direct implementation without a new design, plan or stage record.

| Task | Operation |
|---|---|
| Implement, fix a finding, or resume work with checks or review still to perform | [Execute stage](prompts/execute-stage.md) |
| Review code or recheck a finding | [Review stage](prompts/review-stage.md) |
| Summarize or reconcile existing delivery evidence only | [Hand off](prompts/handoff-stage.md) |

Read the original requirements, confirmed decisions, repository instructions and acceptance relevant to this outcome. Preserve unrelated work and prior authorization. A stage request does not authorize release or unrelated refactoring. Match depth to uncertainty, consequences, reversibility and affected interfaces; investigate facts that could change the result. Honor supplied task budgets without dropping substantive requirements.

When implementing or verifying behavior, judge it against the contract, including compatibility and relevant state, failure and recovery invariants. Tests need meaningful expectations derived independently of the implementation. Run required gates and explicitly required rechecks; a failed command or empty test collection is not success. For any operation, reuse evidence only while relevant content, requirements, inputs, check configuration, runtime and freshness requirements still match. Check applicability at the affected scope, not through a new whole-workspace inventory.

Honor actual review and approval requirements, including human plus agent review when requested; do not ask again for authorization already given. For an understood local reversible change without such a policy, focused verification and self-review can suffice. Seek additional review when consequential uncertainty or affected boundaries warrant it. Keep author repair, reviewer verification and human acceptance distinct; missing required review remains pending.

Finish by checking substance and editing for readability within the same task. Templates are optional aids, not required fields, headings or new artifacts. One existing record can own durable status when useful or required; otherwise the completion response suffices. Design/spec own decisions and contracts, reviews own findings. Default artifacts to English; resource paths stay within this bundle.
