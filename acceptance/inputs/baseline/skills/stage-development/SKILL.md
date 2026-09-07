---
name: stage-development
description: Execute a bounded implementation stage with tests, review, fixes and a commit gate, or independently review a stage's code. Use when working from a stage plan or requesting a focused code review.
---

# Stage development

| Operation | Read |
|---|---|
| Implement, fix findings, or finish a stage | [Execute stage](prompts/execute-stage.md) |
| Review stage code and tests | [Review stage](prompts/review-stage.md) |

Goal: deliver a correct, reviewable outcome with effective checks and a usable handoff. Read the current scope, original requirements/design, repository instructions and acceptance. A sufficient short combined note is valid input; do not restart planning to create template files. Load only the selected operation and its relevant resources.

Both executor and reviewer assess the same stage contract: observable behavior and compatibility, state/error/recovery invariants, meaningful tests with independently derived expectations, and actual checks on the relevant candidate. New tests or abstractions need a current behavior/risk, not a count or speculative feature. A complete gate includes the project's required checks; failed or empty test collection is not success.

Reuse evidence only while relevant content, requirements, inputs, check configuration, runtime conditions and freshness requirements still match. A changed input/runtime can invalidate a result without a code edit. Verify applicability at that scope, not through a new whole-workspace inventory. Mandatory gates and explicitly required independent rechecks still run.

Keep implementation and review roles distinct. Human plus agent review is the default; honor a recorded autonomous policy without fabricating human approval or repeated confirmation checkpoints. Missing required review stays pending. A stage request does not authorize release or unrelated refactoring.

One existing record owns live delivery status; design/spec own decisions/contracts. Operations provide adaptable record/feedback examples and after-generation checks, not mandatory additional documents or agents. Default artifacts to English; resolve resources within this bundle.
