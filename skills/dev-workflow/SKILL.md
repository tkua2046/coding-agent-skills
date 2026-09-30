---
name: dev-workflow
description: Set up or adapt development checks and document ownership, prepare a feature for PR review, or perform an authorized versioned release. Use for repository maintenance and delivery, not feature design or routine code review.
---

# Development workflow

Complete the requested setup, delivery or release operation with effective checks and accurate evidence. Select the relevant operation; do its substantive work, check the result, then make it easy to read as the final part of the same task.

| Task | Operation |
|---|---|
| Inspect or repair environment, checks, hooks, coverage or document ownership | [Setup](prompts/setup-dev-workflow.md) |
| Prepare or revise a feature PR | [Prepare PR](prompts/prepare-pr.md) |
| Assess readiness, prepare version/notes, tag, publish or resolve a release retry | [Release](prompts/release.md) |

Reuse working project tools and applicable evidence. Match depth to uncertainty, consequences, reversibility and affected boundaries; honor task budgets and actual required gates/review. A small implementation does not need workflow infrastructure added along the way. Inspection diagnoses the supplied state; it does not imply permission or a need to repair it.

Preserve original requirements, confirmed decisions and review findings through existing immutable references; retain otherwise unavailable relevant originals once. Existing authorization persists, but this procedure grants no additional scope. Ordinary commits do not trigger PRs, version bumps or releases. Distinguish author fixes, reviewer verification and human acceptance; a passing gate does not establish all three.

Use [document ownership](references/documents.md) when changing document responsibilities. Root templates and Python assets are optional examples: preserve useful conventions, filenames and working configuration. No particular headings, fields, new artifacts or self-check reports are required unless the task itself requires them. Default artifacts to English; resource paths stay inside this bundle.

Before delivery, use the shared [final checks](references/delivery-checks.md) to catch material omissions. Correct supported issues and finish; this is not an automatic review loop or reason to rerun adequate checks.
