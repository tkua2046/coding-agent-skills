# Plan implementation

Read original requirements, existing decisions, current code and check configuration. The request or a short note can establish sufficient decisions; a separate design or document review is needed only when requested, required by policy or useful to resolve consequential uncertainty. Use the shared [plan contract and adaptable example](../assets/implementation-plan.template.md). Investigate an unresolved fact that could change the plan; surface choices that need the user's decision.

Build coherent increments from observable outcomes and dependencies, preferably with an early runnable path. Implementation, meaningful tests and affected documentation travel together. A deliberately partial stage must leave a usable state and state its limitation. Include PR/release work only when in scope; ordinary commits do not each require a PR or version bump.

Keep one current plan, which may be a section of a local design note. Refresh affected pending outcomes and their acceptance when scope changes. Preserve completed outcomes and source/review history through existing immutable links, capturing an otherwise unavailable reviewed version once. A private rename or new test does not change a planning decision.

Link established execution/review policy once, including applicable user requirements. Without one, choose checks and review proportionate to uncertainty, consequences, reversibility and affected boundaries. Identify an actual approval dependency where it affects delivery. Keep run results and current delivery status in one place when needed; stage rows may link to it.

After drafting or amending, load the Plan section of [artifact checks](../references/artifact-checks.md). Fix supported issues and expose unresolved dependencies; otherwise the check is silent, with no report or extra review round.
