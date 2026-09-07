# Plan implementation

Read specs, clarifications, reviewed design, current code, and existing checks. Surface unresolved design blockers rather than filling them with invented requirements.

Build ordered increments from observable outcomes and dependencies. Prefer an early runnable path where feasible. Each increment includes the implementation, relevant tests, and necessary documentation. A partial first stage is acceptable when its limitation is explicit and the committed state remains coherent.

For each stage, capture the planning decisions a reader needs:

- Observable outcome and bounded scope; name files only when they clarify ownership.
- Requirements/design decisions addressed.
- Dependencies and significant risks.
- Decisive acceptance/risk checks or links to their authoritative contract; distinguish existing from proposed commands.
- Done condition and intended commit boundary; a suggested message is optional.

Use the repository's complete commit gate when specified. A stage commonly maps to one commit, but split a large change into coherent commits when that improves review. Avoid unrelated files, placeholders that pretend to work, and an artificial documentation commit that hides bug fixes.

Link the repository's execution/review policy once; if none exists, briefly establish implement/test → agreed checks/hooks → snapshot review → fixes/recheck → commit, including the actual human/agent review policy. Do not repeat this procedure in each stage. Keep run results, reviewed identities and findings in a stage/review record. A new code change invalidates affected checks, not every unrelated design decision.

Choose one compact table or short list; add detail only for a dependency, risk, or boundary the overview cannot explain. Do not restate every function, test method, test count, or code edit in prose. Keep decisive acceptance examples, especially failure/recovery behavior; these are not an exhaustive test inventory.

For a small occupied-cell feature, one coherent increment may suffice: lookup + blocked-move contract + verification together. For a persisted-data migration, order work around preserving the source, validating the new representation before activation, and safe interrupted retry. Stage boundaries need reasons, not a prescribed count or a stage for every component.

Amend affected pending stages when confirmed scope changes; preserve completed outcomes and their evidence. A new regression test or private rename alone belongs with code/tests. A public behavior change updates the affected requirement/design acceptance and pending stage. Do not rewrite the whole plan or add global rules for a local correction.

Include release/PR work only within requested delivery scope. Ordinary implementation commits do not each require a PR or version bump. Mark all unexecuted work as planned.
