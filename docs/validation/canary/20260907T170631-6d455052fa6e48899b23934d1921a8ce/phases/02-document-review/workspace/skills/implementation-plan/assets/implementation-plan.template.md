# Plan contract and adaptable example

Use this contract for authoring and review. Adapt the shape; omit drafting instructions and irrelevant fields from the generated plan. One local outcome may be a section of the existing design note.

The plan owns deliverable outcomes, order, dependencies, reasons for review/commit boundaries and acceptance evidence. Original specs/design own requirements and rationale; code/tests own functions, test methods and implementation details. Update planning decisions, not a second implementation inventory. Keep one live delivery state, either here or in a linked handoff; review records own findings and dispositions.

Lead with the next observable outcome, its prerequisite and decisive acceptance. Use one table or short list, not parallel summaries of the same stages. Include meaningful failure/recovery acceptance or link its authoritative example. A stage includes its relevant tests and needed documentation. Split for a genuine dependency, risk or ownership boundary; do not prescribe stage/commit counts. Explain any partial result or ordering constraint that could affect acceptance. Link policy/check commands once after the outcomes; distinguish planned checks from verified results.

## Possible shape

# [Feature delivery]

Next: [observable outcome; prerequisite/open decision; decisive acceptance].

| Outcome / scope | Depends on / reason for boundary | Acceptance evidence |
|---|---|---|
| [usable result] | [needed predecessor or none] | [contract example, check or link] |

Sources: [requirements/design]. Execution/review policy and gate: [link]. Current delivery: [one status block here or handoff link].

[Add only material dependencies, risks or limitations not explained above. Link completed outcomes and original evidence.]

## Small illustration

Add an optional saved search label while preserving unnamed searches. One increment includes save/load behavior, existing-data compatibility and checks that renaming a label leaves the query unchanged. It has no separately deployable prerequisite; acceptance is save → reload returning the same label/query, including an old unlabeled entry. A later private helper rename leaves this plan unchanged; a new requirement to share labels across users would change its scope and dependencies.
