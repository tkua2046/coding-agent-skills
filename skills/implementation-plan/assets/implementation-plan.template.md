# Plan contract and adaptable example

Use this contract for requested or needed planning and its review. Adapt the shape; omit drafting instructions and irrelevant fields from the generated plan. One local outcome may fit in a response or an existing note.

The plan owns deliverable outcomes, order, dependencies, reasons for review/commit boundaries and acceptance evidence. Original requirements and existing design decisions own the contract and rationale; code/tests own implementation details. Update planning decisions without duplicating those details. When live delivery status is needed, keep it here or in an existing handoff; reviews own findings and dispositions.

Lead with the first undelivered stage's usable outcome, prerequisite and decisive acceptance; the opening and ordered stages must agree. Distinguish the overall feature goal when it extends beyond that next delivery. Use one table or short list, not parallel summaries of the same stages. Include meaningful failure/recovery acceptance or link its authoritative example. A stage includes its relevant tests and needed documentation. Split for a genuine dependency, risk or ownership boundary; do not prescribe stage/commit counts. Explain any partial result or ordering constraint that could affect acceptance. Link policy/check commands once after the outcomes; distinguish planned checks from verified results.

## Possible shape

# [Feature delivery]

Next: [first undelivered stage's usable outcome; its prerequisite/open decision and decisive acceptance, consistent with the ordered plan].

| Outcome / scope | Depends on / reason for boundary | Acceptance evidence |
|---|---|---|
| [usable result] | [needed predecessor or none] | [contract example, check or link] |

Sources: [requirements/existing decisions]. Execution/review policy and gate: [applicable requirements/checks]. Current delivery: [existing status or handoff link when needed].

[Add only material dependencies, risks or limitations not explained above. Link completed outcomes and original evidence.]

## Small illustration

Add an optional saved search label while preserving unnamed searches. One increment includes save/load behavior, existing-data compatibility and checks that renaming a label leaves the query unchanged. It has no separately deployable prerequisite; acceptance is save → reload returning the same label/query, including an old unlabeled entry. A later private helper rename leaves this plan unchanged; a new requirement to share labels across users would change its scope and dependencies.
