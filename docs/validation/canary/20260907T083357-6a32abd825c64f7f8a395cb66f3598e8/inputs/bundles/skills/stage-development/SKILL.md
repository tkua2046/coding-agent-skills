---
name: stage-development
description: Execute a bounded implementation stage with tests, review, fixes and a commit gate, or independently review a stage's code. Use when working from a stage plan or requesting a focused code review.
---

# Stage development

| Operation | Read |
|---|---|
| Implement, fix findings, or finish a stage | [Execute stage](prompts/execute-stage.md) |
| Review stage code and tests | [Review stage](prompts/review-stage.md) |

Operate on the current agreed stage. Read its requirements, design, repository instructions, baseline and acceptance criteria. Keep implementation and review roles distinct; the executing agent owns edits and the reviewer owns findings.

Human plus agent review is the default collaboration policy. Honor an explicitly requested autonomous/agent-only policy without fabricating human approval. Existing task authorization persists; do not add repeated confirmation checkpoints. When an actual required review is missing, report it as pending and do not declare the stage accepted.

Use [the stage record](assets/stage-record.template.md) to capture state and evidence. Keep the main record short and link raw outputs. Default artifacts to English and resolve resources relative to this folder. A stage request alone does not authorize release or unrelated refactoring.
