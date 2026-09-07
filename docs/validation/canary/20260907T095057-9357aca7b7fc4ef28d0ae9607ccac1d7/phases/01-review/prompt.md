Use the review operations in skills/feature-design and skills/implementation-plan
for one combined review of docs/DESIGN.md (D1) and docs/PLAN.md (P1) against
docs/ORIGINAL.md, the existing application and check configuration.

This is a routine local feature task. Decide whether the proposed next increment
is usable as written; report consequential issues with locations, examples and
minimal corrections. Assess whether a developer can quickly understand the
behavior and next action. Treat optional preferences as optional and conclude
when the evidence supports a verdict.

Write one concise report at docs/reviews/REPORT.md with the verdict, reviewed
scope/version, findings and next action. This is a static document review: inspect
files, but do not run application commands or tests or claim runtime verification.
Do not edit requirements, design, plan, code or configuration. No implementation,
commits, tags, pushes, external actions or additional human/agent approval rounds
are part of this task. The review itself is already authorized.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
