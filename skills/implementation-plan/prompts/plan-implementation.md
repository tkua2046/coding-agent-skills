# Plan implementation

Read specs, clarifications, reviewed design, current code, and existing checks. Surface unresolved design blockers rather than filling them with invented requirements.

Build ordered increments from observable outcomes and dependencies. Prefer an early runnable path where feasible. Each increment includes the implementation, relevant tests, and necessary documentation. A partial first stage is acceptable when its limitation is explicit and the committed state remains coherent.

Give each stage:

- Outcome and scope/files.
- Requirements/design decisions addressed.
- Dependencies and significant risks.
- Acceptance examples and specific checks; distinguish existing from proposed commands.
- Done condition and proposed commit message.

Use the repository's complete commit gate when specified. A stage commonly maps to one commit, but split a large change into coherent commits when that improves review. Avoid unrelated files, placeholders that pretend to work, and an artificial documentation commit that hides bug fixes.

Make the execution loop explicit: implementation and tests → checks/hooks → fixed review snapshot → human and authorized independent-agent review → fixes and necessary rechecks/review → final commit gate → commit → next stage. A new code change invalidates affected checks. Record human-review status; lack of response is not approval.

Show a compact stage table first and detailed cards below. Do not duplicate the entire spec, design, or test catalog. Include release/PR work only if it is part of the requested delivery. Ordinary implementation commits do not each require a PR or version bump. Mark all unexecuted work as planned.
