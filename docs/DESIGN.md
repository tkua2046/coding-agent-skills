# Design: useful workflow skills with proportionate process

Decision: retain four independently copyable skills. Choose workflow depth from the decisions and risks in the task; do not make every task traverse every operation. Keep original evidence retrievable outside the maintained source diff. [Plan](IMPLEMENTATION_PLAN.md) owns execution state.

## Decisions and consequences

| Decision | Reason | Consequence and example |
|---|---|---|
| Choose needed operations, not a fixed pipeline | A known local change has fewer decisions than a migration | Implement a clear filter fix with relevant tests; investigate an uncertain compatibility issue before planning |
| Explicit user and repository gates remain authoritative | Simplification cannot manufacture approval or skip real constraints | A project requiring independent review still gets it, even for a small patch |
| Design owns choices; plan owns outcomes | Prose should not mirror implementation | Adding a regression assertion leaves the design and completed stages alone unless the contract changes |
| Review the whole deliverable | Individually valid files can form an unusable PR | Reject unrelated generated snapshots in the source diff even when hooks pass |
| Store evidence separately and reference immutable originals | Source preservation does not require repeated copies in every report | A calibration run is referenced by identity; source PRs contain a result index, not its repeated workspaces |
| Load one operation and its relevant references | Installing a skill should not burden unrelated work | Design drafting loads decision guidance; release instructions stay unloaded |

## Boundaries

The four skills cover feature design, implementation planning, stage execution/review, and development setup/delivery. They are guidance, not an orchestrator or approval service. Each folder is portable; short shared review principles may be repeated between folders so installation has no cross-folder dependency. Within a folder, author and reviewer use the same substantive artifact contract.

Existing specifications and confirmed decisions stay authoritative. A local extension updates affected decisions and pending outcomes. A separate design is useful for independent ownership/lifecycle or consequential choices, not merely because another request arrived. Document templates are adaptable examples; a direct implementation request with sufficient context does not need a document prerequisite.

One existing record owns live delivery state. Git revisions, review records and actual check output establish evidence; otherwise unavailable originals are captured once. Fixed findings require applicable verification, and an unchanged verified finding does not trigger a new review cycle. Missing evidence stays unknown, not success or an invented defect.

## Evidence and verification

Historical raw trials and review rounds remain pinned in the [evidence archive](EVIDENCE.md). New model runs use ignored local storage, then a separate immutable evidence tree for delivered results. Shared calibration references must fail closed on missing or changed dependencies. Every retained attempt remains discoverable so an older pass cannot conceal a newer failure.

Mechanical tests check packaging and runner behavior. Focused LLM tasks check operation decisions; complete tasks check useful outcomes and interaction costs. Compare identical requests/settings against the pre-repair skill revision and retain failures. Broader release checks remain distinct from normal PR verification. See [test goals](../evals/GOALS.md) and [actual results](VALIDATION.md).

A passing suite is insufficient acceptance. The final reviewer inspects the aggregate source diff, clean-checkout use, original-evidence retrieval and actual task output. Report quality and effort separately: less work is useful only when the required behavior and safeguards remain intact. A handful of trials cannot establish general productivity or human satisfaction.
