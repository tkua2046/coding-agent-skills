# Intake a feature

Read original requirements, known decisions, repository instructions and relevant entry points, interfaces and checks. Identify the intended change and compatibility obligations. Infer routine reversible defaults; ask only when an answer materially changes behavior, compatibility, scope or architecture. If observed behavior makes stated requirements incompatible, expose the concrete tradeoff and leave consequential precedence or scope unresolved unless the owner supplied that decision; an inferred exception is a proposal, not a confirmed requirement. Keep confirmed answers distinct from proposals, with an example explaining a consequential question.

When an unknown could change the approach, obtain the smallest useful evidence: inspect a caller, reproduce behavior or run an authorized experiment. Reuse applicable baseline evidence; run checks when they resolve uncertainty or establish a needed comparison. Report actual commands, outcomes and limits, distinguishing pre-existing failures. Once the question is answered, continue within scope. Investigation responds to a concrete unknown; it is not a recurring requirement to reassess the process after each change.

Return the useful findings and remaining decisions in the response or an existing note. Adapt the [spec addendum](../assets/spec-addendum.template.md) when durable clarification is useful or requested. Link original requirements and relevant raw evidence through existing immutable references; capture otherwise unavailable source text once rather than replacing it with a summary. Requirement IDs are useful when they connect acceptance to later stages.

An intake-only request stops before design or implementation. When implementation is also requested and the facts are sufficient, proceed without an additional intake artifact. If an essential answer is pending, continue independent work but leave the dependent decision open.

After writing the note, load the Intake section of [artifact checks](../references/artifact-checks.md). Correct supported issues; expose unresolved material decisions. Otherwise the check is silent, without an additional report or review round.
