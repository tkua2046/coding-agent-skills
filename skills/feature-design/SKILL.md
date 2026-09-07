---
name: feature-design
description: Clarify feature requirements, inspect relevant existing code, and draft or review a concise design with consequences and acceptance examples. Use before planning a feature or when reviewing its design.
---

# Feature design

Choose the requested operation; do not automatically perform all three.

| Request | Read |
|---|---|
| Understand requirements or identify clarification questions | [Intake](prompts/intake-feature.md) |
| Write or revise the design | [Draft design](prompts/draft-design.md) |
| Review an existing design | [Review design](prompts/review-design.md) |

Use the user's original specifications and decisions as authority. Retain source text and distinguish confirmed requirements from assumptions. Inspect relevant existing code before proposing replacements. A design request does not authorize implementation.

Write engineering artifacts in English unless the user requests otherwise. Put the outcome, material decisions, consequences, and next step first. Scale detail to risk and available time; retain the same review criteria for a short document. Link long evidence and examples rather than duplicating them.

For a follow-up, amend affected decisions and acceptance in the existing design. Create a separate design only when it has a distinct lifecycle, audience, or substantial independent risk. Preserve accepted history and avoid expanding the workflow merely because another feature was requested.

For a fresh artifact, adapt the [spec addendum](assets/spec-addendum.template.md), [design](assets/design.template.md), or [review](assets/review.template.md). Existing repository document conventions take precedence over these defaults. Resolve these resources relative to this skill folder, not the target repository.
