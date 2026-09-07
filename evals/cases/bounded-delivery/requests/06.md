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
