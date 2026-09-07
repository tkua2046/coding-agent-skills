This is already a fresh reviewer context, separate from the author. You are the
assigned independent reviewer; this role does not require spawning another reviewer.
Independently use the design and implementation-plan review operations in
skills/feature-design and skills/implementation-plan to assess docs/REQUEST.md against
the current proposed design and plan. This is one combined document review authorized
for this task. Decide whether implementation can begin.
Write only the review record and necessary evidence. Write reviews/design-current.json
with {"verdict":"ready"|"needs-changes"|"needs-decision","findings":[...]}; this is the
runner interface, not a demand to find issues. Preserve previous reviews separately.
Identify reviewed content, material findings, and next action in the report. Do not
modify the product or claim implementation/runtime/human approval from this review.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
