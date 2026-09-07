This is already a fresh reviewer context, separate from the author. You are the
assigned independent reviewer; this role does not require spawning another reviewer.
Independently use skills/stage-development's review operation to assess this
feature implementation against docs/REQUEST.md and the existing application behavior.
Inspect the actual code and tests; run relevant checks when useful. Decide whether
it is ready for the owner to review.
Write only review/evidence files. Write reviews/code-current.json with
{"verdict":"ready"|"needs-changes"|"needs-decision","findings":[...]}. Identify the
reviewed content, consequential findings and actual checks. Preserve previous reports.
Do not modify code or tests. Human acceptance remains pending; no commit is requested.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
