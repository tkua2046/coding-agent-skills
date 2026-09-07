# Plan implementation

Read original requirements, confirmed design, current code and check configuration. A sufficient short note can establish the design; a separately reviewed document is necessary only under the actual policy. Use the shared [plan contract and adaptable example](../assets/implementation-plan.template.md). Surface unresolved consequential choices rather than inventing their answers.

Build coherent increments from observable outcomes and dependencies, preferably with an early runnable path. Implementation, meaningful tests and affected documentation travel together. A deliberately partial stage must leave a usable state and state its limitation. Include PR/release work only when in scope; ordinary commits do not each require a PR or version bump.

Keep one current plan, which may be a section of a local design note. Refresh affected pending outcomes and their acceptance when scope changes. Preserve completed outcomes and source/review history through existing immutable links, capturing an otherwise unavailable reviewed version once. A private rename or new test does not change a planning decision.

Link the established execution/review policy once. If none exists, state the agreed checks/hooks, review and acceptance before commit; do not invent human approval or duplicate the procedure in every stage. Keep run results and current delivery status in one existing handoff/status section; stage rows may link to it.

After drafting or amending, load the Plan section of [artifact checks](../references/artifact-checks.md). Fix supported issues and expose unresolved dependencies; otherwise the check is silent, with no report or extra review round.
