# Use the four skills

These are reusable English instructions. Choose the operation you need; loading a skill does not require running every operation or creating every document.

## Put them in your interview project

From the source repository, copy the four real folders in `skills/` into your project's `.agents/skills/`. The repository's own `.agents/skills/` contains relative discovery links; copying those links alone can break them. From the extracted local package, copy its four actual `.agents/skills/` folders instead. Preserve each folder's contents and keep existing skills. If the agent cannot discover them, ask it to read the relevant `SKILL.md` by path; that works without global installation. Keep personal preparation files out of the submitted diff unless agreed with the interviewer.

Before the call, verify your usual interpreter, test command, formatter/linter and GitHub authentication in a scratch project. Check the actual interview repository's instructions and tools when it becomes available. Follow the invitation: Chrome, screen sharing and editor line numbers.

## Start with the task

Paste the interviewer's requirements, including later clarifications, then choose one request below. Give the agent the time remaining. Explain decisions and inspect its work yourself.

| Need | Example request |
|---|---|
| Clarify | Read `.agents/skills/feature-design/SKILL.md`. Inspect this task and code. Help me identify consequential clarification questions and reasonable defaults. |
| Design | Use feature-design to propose the design for these confirmed requirements. I will review it before implementation. |
| Plan | Read `.agents/skills/implementation-plan/SKILL.md`. Turn the accepted decisions into a delivery plan. I will review it before implementation. |
| Implement | Read `.agents/skills/stage-development/SKILL.md`. Implement the agreed outcome and run the applicable checks. Leave the result ready for my review. |
| Review | Use the relevant skill's review operation on this exact candidate and the original requirements. Report material findings and the evidence boundary. |
| Handoff | Use stage-development to update the current handoff from existing evidence. Keep pending checks and my acceptance visible. This request is status-only. |
| Setup | Read `.agents/skills/dev-workflow/SKILL.md`. Inspect the existing checks and repair this specific gap: [gap]. |

Use a separate context for independent review; a same-context review is self-review. Keep original findings available for rechecks. For a follow-up, supply the changed requirement and existing work; the skills should update affected decisions and pending outcomes.

## Finish

Inspect the final diff, actual test results and any remaining issue. Commit and push to the requested repository when the interviewer asks. A PR, version bump, changelog or release is needed only when the task or repository requires it.

Validation and limitations are recorded in [VALIDATION.md](VALIDATION.md), alongside this guide in the repository or local package. The skills guide behavior; they do not guarantee timing or replace your judgment.
