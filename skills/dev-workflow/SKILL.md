---
name: dev-workflow
description: Set up or adapt development checks and document ownership, prepare a feature for PR review, or perform an authorized versioned release. Use for repository maintenance and delivery, not feature design or routine code review.
---

# Development workflow

Goal: a useful, reviewable deliverable with effective checks and accurate evidence. Inspect existing conventions and reuse working setup. Match depth to uncertainty, consequences, reversibility and affected boundaries while honoring established user/repository review and gates. Select one operation and its relevant resources; load its silent check after generation.

| Request | Read |
|---|---|
| Configure/repair environment, hooks, coverage or document layout | [Setup](prompts/setup-dev-workflow.md) |
| Prepare/revise a feature PR | [Prepare PR](prompts/prepare-pr.md) |
| Prepare/version/tag/publish a release within scope | [Release](prompts/release.md) |

For document creation/reorganization, read [document ownership](references/documents.md). Root and Python assets are adaptable examples, not reasons to overwrite working configuration or create every document.

Existing authorization persists; a procedure does not itself grant publication permission. Ordinary commits do not trigger PRs, version bumps or releases. Preserve original requirements and reviewed evidence through existing immutable references, capturing relevant otherwise unavailable content once. This does not require a repository-wide archive. Distinguish configured, installed and actually verified states. Default artifacts to English; resolve resources within this bundle.
