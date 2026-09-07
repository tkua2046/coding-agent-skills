# Review a stage independently

Read the agreed outcome, original requirements/design, repository instructions, actual code/tests and identified candidate diff, including new files. Apply the shared stage contract in SKILL.md; the implementer's summary or test count is not evidence of correctness. Use the [review feedback contract and example](../assets/review.template.md) for the report.

Form counterexamples for material state, compatibility, error/recovery and scope risks. Run relevant tests when useful and permitted, honoring required rechecks. Report actual results and limitations. Experiments that modify files belong in an isolated copy, not the author's checkout.

On recheck, establish whether content and evidence applicability changed. Cite an unchanged verified resolution; changed behavior, stale inputs/runtime or incomplete verification requires the full affected invariant to be checked. Keep partial fixes open. Neither a previous verdict nor fresh author claims override the actual candidate.

Write only requested review/evidence output; do not edit implementation, tests, specs or plan. Reference the existing candidate and raw check/measurement records; state what matched, any differences and consequential results. Preserve independent observations without copying their full inventories or logs into the verdict. A new dependency, abstraction or performance demand must address the current contract or observed risk. Accept sufficient work and mark optional preferences as optional. If the candidate changes during review, identify affected results as stale and request a stable version, continuing only unaffected inspection.

After writing feedback, load the Review section of [artifact checks](../references/artifact-checks.md). Correct supported reporting defects and disclose unresolved issues; otherwise the check is silent. A ready agent verdict establishes neither human acceptance, a commit nor release.
