---
name: feature-design
description: Clarify feature requirements, inspect relevant existing code, and draft or review a concise design with consequences and acceptance examples. Use before planning a feature or when reviewing its design.
---

# Feature design

Goal: resolve material uncertainty and leave a decision another developer can understand and implement. Choose the requested operation; do not automatically perform all three.

Select depth from uncertainty, failure consequences/reversibility and affected interfaces or owners. Explain the choice in one sentence when useful; no classification document is needed.

- A local understood change can use one short note covering design, implementation outcome and acceptance, with one combined document review when authorized. Preserve any existing entrypoints/history.
- A feature with consequential choices needs explicit design reasoning and delivery boundaries. Separate their documents/reviews when that helps independent assessment.
- High-consequence changes need the relevant compatibility, recovery or coordination analysis. Expand the risky parts, not every template section.
- For a material unknown, first answer a bounded question through relevant inspection or a small authorized experiment. Record the evidence and limits, then reconsider depth. Do not elaborate a design around an untested premise.

Existing user/repository review requirements take precedence. Combined document review does not replace the agreed code review or human acceptance.

| Request | Read |
|---|---|
| Understand requirements or identify clarification questions | [Intake](prompts/intake-feature.md) |
| Write or revise the design | [Draft design](prompts/draft-design.md) |
| Review an existing design | [Review design](prompts/review-design.md) |

Use the user's original specifications and decisions as authority. Retain source text and distinguish confirmed requirements from assumptions. Inspect relevant existing code before proposing replacements. A design request does not authorize implementation.

Write engineering artifacts in English unless the user requests otherwise. Put the outcome, material decisions, consequences, and next step first. Scale detail to risk and available time; retain the same review criteria for a short document. Link long evidence and examples rather than duplicating them.

For a follow-up, amend affected decisions and acceptance in the existing design. Create a separate design only when it has a distinct lifecycle, audience, or substantial independent risk. Preserve accepted history and avoid expanding the workflow merely because another feature was requested.

For a fresh artifact, adapt the [spec addendum](assets/spec-addendum.template.md), [design](assets/design.template.md), or [review](assets/review.template.md). Existing repository document conventions take precedence over these defaults. Resolve these resources relative to this skill folder, not the target repository.
