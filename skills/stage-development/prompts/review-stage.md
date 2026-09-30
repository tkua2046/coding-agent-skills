# Review a stage independently

Read the original requirements, confirmed decisions, repository instructions and complete identified candidate, including code/tests, new files and expected generated artifacts. Apply the shared contract in SKILL.md. The author's summary and passing tests alone cannot establish goal fulfillment.

Assess observable behavior, compatibility, state/error/recovery invariants and scope. Form counterexamples for material risks; run relevant tests when useful and permitted, honoring required rechecks. Judge overall complexity and maintenance/review burden by concrete consequences. Expected generated artifacts may serve the goal; evaluate their purpose and result. Accept sufficient work and mark preferences as optional.

On recheck, read the original finding and identify the current affected revision. Verify the whole concern: partial fixes stay open and verified complete fixes close. Cite unchanged applicable reviewer verification rather than reopening it; changed behavior, stale inputs/runtime or incomplete verification requires checking the full affected invariant. Neither a prior verdict nor a fresh author claim overrides the candidate. Preserve original findings/evidence through immutable references, adding the current disposition without recopying history.

Report locatable material findings with their trigger, consequence, correction and verification. Retain finding identity when tracking rounds; distinguish open concerns, author-reported repairs, reviewer-verified fixes, evidence-based refutations and accepted nonblocking limits. State actual review mode, checks and static/runtime limits. Use an independent authorized context when required; disclose missing independence rather than claiming it. Resolve disagreement through evidence or a decision, not cosmetic rounds.

Write only requested review/evidence output; do not edit the deliverable. Experiments that modify files belong in an isolated copy. If the candidate changes during review, mark affected results stale and seek stable content while continuing unaffected inspection. A ready agent verdict establishes neither human acceptance, a commit nor release.

Use the Review section of [final checks](../references/artifact-checks.md), then finish with the supported verdict and any material remaining action before supporting detail. The [feedback example](../assets/review.template.md) is optional. Stop once the requested review is sufficient.
