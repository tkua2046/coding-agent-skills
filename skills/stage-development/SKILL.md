---
name: stage-development
description: Implement a bounded change with appropriate validation and required review, or independently review code. Use for direct implementation requests, planned stages and focused code reviews.
---

# Stage development

| Operation | Read |
|---|---|
| Implement, fix findings, or finish a stage | [Execute stage](prompts/execute-stage.md) |
| Review stage code and tests | [Review stage](prompts/review-stage.md) |

Goal: deliver a correct, reviewable outcome with effective checks and a usable handoff. Read the request, relevant original requirements and existing decisions, repository instructions and acceptance. Sufficient facts in the request can support direct implementation without design, plan or review documents. Load only the selected operation and its relevant resources.

Both executor and reviewer assess the deliverable against the original goal and agreed stage scope, including observable behavior, compatibility, relevant state/error/recovery invariants and maintainability. An intentionally partial stage must leave a usable state and disclose the remaining outcome. Choose investigation, validation and review depth from uncertainty, consequences, reversibility and affected interfaces/owners. Use meaningful checks with independently derived expectations; new tests or abstractions need a current behavior or risk. Run the project's required gates; failed or empty test collection is not success.

Reuse evidence only while relevant content, requirements, inputs, check configuration, runtime conditions and freshness requirements still match. A changed input/runtime can invalidate a result without a code edit. Verify applicability at that scope, not through a new whole-workspace inventory. Mandatory gates and explicitly required independent rechecks still run.

Honor established user/repository review and approval requirements, including human plus agent review when requested and prior authorization. Without an established policy, a local understood reversible change can use focused verification and self-review; seek independent or human review when consequential uncertainty or affected boundaries warrant it. Perform explicitly requested review, keep author and reviewer roles distinct, and disclose actual independence. Missing required review stays pending. A stage request does not authorize release or unrelated refactoring.

When durable delivery status is useful or required, keep it in one existing record; a completion response can suffice for a local change. Design/spec own decisions/contracts. Operations provide adaptable record/feedback examples and silent checks. Default artifacts to English; resolve resources within this bundle.
