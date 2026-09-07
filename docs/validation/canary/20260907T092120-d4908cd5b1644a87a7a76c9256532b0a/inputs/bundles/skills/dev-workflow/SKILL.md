---
name: dev-workflow
description: Set up or adapt development checks and document ownership, prepare a feature for PR review, or perform an authorized versioned release. Use for repository maintenance and delivery, not feature design or routine code review.
---

# Development workflow

Select the requested operation and inspect the target repository's existing conventions first.

| Request | Read |
|---|---|
| Configure or repair environment, hooks, coverage and document layout | [Setup](prompts/setup-dev-workflow.md) |
| Prepare or revise a feature PR | [Prepare PR](prompts/prepare-pr.md) |
| Prepare/version/tag/publish a release, within requested scope | [Release](prompts/release.md) |

For document creation or reorganization, use [document ownership](references/documents.md). Root templates live in `assets/`; the Python checks example is in `assets/python/`. Templates are defaults to adapt, not instructions to overwrite established configuration or create every document for every task.

Operate within existing task authorization. Do not treat a release procedure as permission to publish. Conversely, do not repeatedly request approval for actions already authorized. Ordinary implementation commits do not automatically create PRs, bump versions or publish releases.

Keep source requirements and reviewed versions traceable. Report planned, configured, installed and actually verified as separate facts. Default engineering artifacts to English. Each resource path is relative to this skill folder.
