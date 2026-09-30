---
name: feature-design
description: Clarify consequential requirements, draft or amend an implementable design, or review a design and recheck its findings. Use when these decisions are requested or needed before implementation.
---

# Feature design

Resolve the requested decision with enough reasoning to implement it. Select the operation below; do its substantive work first and finish by making the result easy to read.

| Task | Operation |
|---|---|
| Clarify requirements or investigate a material unknown | [Intake](prompts/intake-feature.md) |
| Write a design or amend an existing decision | [Design](prompts/draft-design.md) |
| Review a design or recheck a finding | [Review](prompts/review-design.md) |

Preserve original requirements and confirmed decisions; separate observations, assumptions and proposals. Use existing source/history references, retaining otherwise unavailable originals once. Follow actual user/repository scope, review and approval requirements, including authorization already given.

Match depth to uncertainty, consequences, reversibility and affected interfaces. A settled local change should take a few minutes; a 30-minute design/review loop is unacceptable. Honor supplied task budgets. Investigate facts that can change the decision; if real uncertainty expands the work, expose that consequence instead of silently expanding the workflow. Stop once the requested decision and any required review are sufficient.

A local extension normally amends its existing note. A separate design needs a distinct decision, lifecycle, owner or substantial independent risk. Design owns choices and consequences; plans own delivery order; code/tests own implementation detail. These responsibilities need not become separate files. An implementation request with sufficient facts does not need an invented design phase; design-only work ends before coding.

Templates are optional aids for the final editing step. Follow useful repository conventions; default artifacts to English. No particular headings, field order or self-check report are required. Resource paths stay inside this bundle.
