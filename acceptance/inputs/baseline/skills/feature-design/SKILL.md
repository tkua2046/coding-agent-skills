---
name: feature-design
description: Clarify feature requirements, inspect relevant existing code, and draft or review a concise design with consequences and acceptance examples. Use before planning a feature or when reviewing its design.
---

# Feature design

Goal: resolve material uncertainty and leave an implementable decision. Select one operation; load its linked contract/example when needed and its self-check after generation.

| Request | Read |
|---|---|
| Understand requirements or identify clarification questions | [Intake](prompts/intake-feature.md) |
| Write or revise the design | [Draft design](prompts/draft-design.md) |
| Review an existing design | [Review design](prompts/review-design.md) |

Choose depth by uncertainty, failure consequences/reversibility and affected interfaces/owners, not a difficulty score. A local understood change may combine design and next implementation outcome in one note and one authorized document review. Consequential choices need relevant reasoning and boundaries; separate artifacts only when they help assessment. An unknown needs bounded inspection/experiment before elaborating a design around it. No classification document is needed.

Original specifications and confirmed decisions remain authoritative. Preserve their source text, distinguish assumptions and inspect relevant code. Existing task/repository review requirements take precedence; combined document review does not replace required code review or human acceptance. Design alone does not authorize implementation.

Author and reviewer share the artifact contract. Templates are adaptable, not required headings/files. Follow repository conventions; default artifacts to English. Amend local extensions without reopening unrelated decisions; separate designs serve distinct lifecycle, ownership or substantial independent risk. Resource paths resolve within this bundle.
