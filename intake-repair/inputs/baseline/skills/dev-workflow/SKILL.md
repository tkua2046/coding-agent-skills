---
name: dev-workflow
description: Set up or adapt development checks and document ownership, prepare a feature for PR review, or perform an authorized versioned release. Use for repository maintenance and delivery, not feature design or routine code review.
---

# Development workflow

Goal: effective checks, useful document ownership and accurate delivery evidence. Inspect existing conventions and reuse working setup. Select one operation and its relevant resources; load its silent check after generation.

| Request | Read |
|---|---|
| Configure/repair environment, hooks, coverage or document layout | [Setup](prompts/setup-dev-workflow.md) |
| Prepare/revise a feature PR | [Prepare PR](prompts/prepare-pr.md) |
| Prepare/version/tag/publish a release within scope | [Release](prompts/release.md) |

For document creation/reorganization, read [document ownership](references/documents.md). Root and Python assets are adaptable examples, not reasons to overwrite working configuration or create every document.

Existing authorization persists; do not repeat approval questions or infer publication permission from a procedure. Ordinary commits do not trigger PRs, version bumps or releases. Preserve source requirements and reviewed versions. Distinguish configured, installed and actually verified states. Default artifacts to English; resolve resources within this bundle.
