# Optional plan shape

Use a short list, table or existing note. Include only information useful to deliver the requested outcome; do not copy drafting instructions into the result.

The plan owns outcomes, order, dependencies, useful delivery/commit boundaries and acceptance. Link requirements and design reasoning rather than repeating them. Code and tests own their implementation details; a private rename or added test should not require plan maintenance. Keep live delivery status here or in an existing handoff, not both.

## Example shape

Next: [first undelivered outcome, any prerequisite and decisive acceptance].

| Outcome | Dependency / useful boundary | Acceptance |
|---|---|---|
| [usable increment, including relevant tests/docs] | [needed predecessor or reason for splitting] | [success/failure example, check or authoritative link] |

Sources and gate: [existing requirements, decisions and execution/review policy].

[Add a material limitation or later outcome only if the next increment is a partial delivery. Link existing completed history and status where relevant.]

## Small illustration

Add an optional saved-search label while preserving unnamed searches. One increment includes save/load behavior, compatibility and relevant checks. Accept when save → reload retains the same label/query and an old unlabeled entry still loads. There is no independent prerequisite requiring a separate stage. A helper rename leaves this plan unchanged; sharing labels across users would change scope and dependencies.
