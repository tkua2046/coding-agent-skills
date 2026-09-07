# Review a stage independently

Read the requested outcome, original requirements and existing decisions, repository instructions and complete identified deliverable, including code/tests, new files and expected generated artifacts. Apply the shared stage contract in SKILL.md and the [review feedback contract](../assets/review.template.md). Judge whether the result achieves the goal with justified complexity and a usable review path; the implementer's summary or passing tests alone cannot establish that.

Form counterexamples for material state, compatibility, error/recovery and scope risks. Run relevant tests when useful and permitted, honoring required rechecks. Report actual results and limitations. Experiments that modify files belong in an isolated copy, not the author's checkout.

On recheck, establish whether content and evidence applicability changed. Cite an unchanged verified resolution; changed behavior, stale inputs/runtime or incomplete verification requires the full affected invariant to be checked. Keep partial fixes open. Neither a previous verdict nor fresh author claims override the actual candidate.

Write only requested review/evidence output; do not edit the deliverable. Reference the existing candidate and check records, reporting consequential differences and independent observations. Expected generated artifacts may be part of the goal; assess their purpose and result. Block unnecessary overall complexity when its maintenance or review burden has a concrete consequence, even if component checks pass. Accept sufficient work and mark preferences as optional. If the candidate changes during review, identify affected results as stale and seek a stable version, continuing unaffected inspection.

After writing feedback, load the Review section of [artifact checks](../references/artifact-checks.md). Correct supported reporting defects and disclose unresolved issues; otherwise the check is silent. A ready agent verdict establishes neither human acceptance, a commit nor release.
