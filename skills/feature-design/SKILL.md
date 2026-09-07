---
name: feature-design
description: Clarify uncertain feature requirements and draft or review designs with consequences and acceptance examples. Use for requested design work or consequential choices that need resolution before implementation.
---

# Feature design

Goal: resolve material uncertainty and leave an implementable decision. Select one operation; load its linked contract/example when needed and its self-check after generation.

| Request | Read |
|---|---|
| Understand requirements or identify clarification questions | [Intake](prompts/intake-feature.md) |
| Write or revise the design | [Draft design](prompts/draft-design.md) |
| Review an existing design | [Review design](prompts/review-design.md) |

Choose depth by uncertainty, failure consequences, reversibility and affected interfaces/owners. An explicit design, planning or review request still gets that work. For a direct implementation request with sufficient facts, proceed without inventing design, plan or review documents. A requested local design may combine the decision and next outcome in one note; consequential choices need their reasoning and boundaries. Investigate unknowns that could change the approach, then continue when the evidence is sufficient. Revisit the approach when new evidence changes a decision, rather than scheduling recurring process assessments.

Original specifications and confirmed decisions remain authoritative. Link their existing immutable sources and distinguish assumptions. Honor review and approval requirements established by the user or repository, including prior authorization and human/agent review preferences. Without an established policy, choose review depth on the same grounds as design depth. A design-only request stops before implementation.

Author and reviewer share the artifact contract. Templates are adaptable, not required headings/files. Follow repository conventions; default artifacts to English. Amend local extensions without reopening unrelated decisions; separate designs serve distinct lifecycle, ownership or substantial independent risk. Resource paths resolve within this bundle.
