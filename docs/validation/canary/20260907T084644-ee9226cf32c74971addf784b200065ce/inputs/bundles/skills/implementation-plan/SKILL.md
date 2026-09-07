---
name: implementation-plan
description: Turn a feature design into reviewable stage and commit boundaries, or review that plan for dependencies, acceptance criteria, and feasibility. Use for implementation planning rather than executing code changes.
---

# Implementation plan

For writing or revising a plan, read [Plan implementation](prompts/plan-implementation.md). For reviewing it, read [Review implementation plan](prompts/review-implementation.md). Use only the requested operation.

Ground the plan in original requirements, confirmed design decisions, and the current repository. A stage should deliver an observable result with its relevant tests. Do not replace behavior acceptance with a fixed count of tests or functions.

The plan owns delivery order, dependencies, review/commit boundaries and acceptance. Code and tests own implementation detail. Update the plan when these planning decisions change; adding a test or renaming a private helper does not itself require a plan edit. Preserve completed stages when revising pending work.

Keep the first screen usable for selecting the next stage. Put detailed cases behind links; preserve the requirements and design as their own authorities. Engineering artifacts default to English. Adapt [the plan template](assets/implementation-plan.template.md) to the repository and task size.

Planning does not execute stages or create commits. Record proposed versus verified status accurately. Resolve bundled resources relative to this skill folder.
