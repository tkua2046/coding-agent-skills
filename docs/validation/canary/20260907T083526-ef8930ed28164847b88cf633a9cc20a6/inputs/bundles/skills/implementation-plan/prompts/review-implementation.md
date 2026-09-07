# Review the implementation plan

Read requirements, confirmed design, the plan version, relevant code, and actual check configuration. Do not change the plan or implementation during review.

Assess whether:

- Stages satisfy required behavior without inventing scope or leaving a dependency to a later stage.
- Each boundary is coherent, reviewable, and verifiable; its limitations are explicit.
- Relevant tests arrive with code, cover meaningful errors, and use independent expected results.
- Existing behavior and interfaces remain protected in an existing repository.
- Check commands exist or are explicitly planned; zero tests are not counted as success.
- Runtime cost and stage scope fit the available time; a fixed test count is not the acceptance criterion.
- The human/agent review loop, version being reviewed, fix loop, and final delivery are unambiguous.
- The plan owns delivery decisions rather than duplicating code/tests; routine implementation edits will not require synchronizing a second inventory.
- Detail is proportional to risk: local extensions preserve accepted history, while migration or failure-recovery dependencies remain explicit.

Accept a sufficient short combined note or single coherent increment; separate files, extra stages and fixed test counts are not prerequisites. Block only for a concrete contract, dependency, feasibility or usability consequence. State optional improvements as optional.

Report a short verdict, scope/version, actual inspection/checks, and prioritized findings. Each finding states a location, concrete consequence/example, minimal correction, and verification. Include reading-cost issues when they prevent the plan from being used quickly. Additional material findings may live in an appendix.

Stop when blockers are resolved and remaining suggestions have explicit dispositions. Do not require endless rounds or treat agent preferences as mandatory changes. State whether this was self-review or a genuinely separate reviewer. Historical review results remain bound to their reviewed version.

For a recheck, show current verdict/version, open stable finding IDs and next action first. Preserve prior findings and append what changed and what was verified. “Author fixed” is not “reviewer verified”; recheck the affected contract, including previously omitted parts. Do not reopen unrelated completed decisions without a concrete consequence. When successive rounds repeat the same disagreement without new evidence, identify a resolving experiment/decision or the remaining limitation; do not keep rewriting for stylistic agreement. A deadline does not convert unresolved issues into approval.
