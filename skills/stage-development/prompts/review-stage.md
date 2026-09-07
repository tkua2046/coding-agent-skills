# Review a stage independently

Read the stage's scope and acceptance examples, original requirements/confirmed design, repository instructions, relevant implementation, tests, and the exact candidate diff. Establish the reviewed version including dirty/new files. Do not rely solely on the implementer's summary or test-count claim.

Inspect state invariants, interfaces, error recovery, compatibility, scope creep, and whether tests would detect incorrect behavior. Form concrete counterexamples. Run relevant tests if permitted; report the actual commands and results, including known baseline failures. Experiments that modify files belong in an isolated copy, not the author's live checkout.

The human focuses on intent, usability and explainability; the agent focuses on code-level counterexamples and blind spots. These roles complement each other, but neither establishes the other's approval.

Report:

- Verdict: ready / needs changes / needs decision.
- Exact reviewed scope/version and review mode (independent or self-review).
- Checks run, observed results and untested limitations.
- Prioritized findings with location, trigger/example, consequence, minimal correction and verification.
- Current open finding IDs and next action first; append dispositions of prior findings with stable IDs and the new reviewed version. Distinguish an author's fix claim from reviewer verification, retaining the original concern and each round's evidence.

Do not change production files, tests, specs or plans during review. A separately requested review report may be written. Avoid speculative blockers or cosmetic preferences presented as correctness problems. Preserve material findings even if only the top few fit the first screen.

A ready code-review verdict does not mean a stage was committed, human-reviewed or approved for release. If the candidate changes during review, identify the affected results as stale and ask the executor for a stable version; continue only unaffected inspection.
