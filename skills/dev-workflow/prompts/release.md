# Prepare and execute an authorized release

Identify the requested operation: version/notes preparation, tagging, or publishing. Read repository release rules and existing authorization. Continue already authorized actions; a general reference to this procedure does not itself authorize publishing.

1. Identify the single authoritative version source and the public compatibility contract. Choose the version based on actual changes; account for prerelease/0.x policy rather than blindly mapping every feature to a bump.
2. Keep significant completed changes under Unreleased until release preparation. Move the chosen notes to the actual version/date, retain a new Unreleased section, and review version metadata and notes together. Never list planned features as delivered.
3. Complete the required PR/review process. Run the project's release gate, including deferred expensive suites and required baseline comparisons. Bind evidence to the final candidate and relevant inputs/runtime; where agent evaluations apply, also bind their fixture, grader and settings. Missing, stale, failed or inconclusive required evidence leaves release pending. Reuse results only while their scope and freshness remain applicable, without skipping mandatory gates. Rerun affected checks after fixes and retain failed attempts/dispositions. Verify the final merged commit, including conflict-resolution changes and relevant CI, rather than assuming the old feature-branch result still applies.
4. Tag the exact verified release commit within the requested scope. Inspect an existing tag/release before retrying; do not move or replace one implicitly. Build and validate any distributable from that tagged content.
5. Smoke-test the actual artifact where applicable, then publish when authorized. Preserve the association among source commit, version, tag and artifact. If publication status is uncertain, inspect remote state before retrying.

Report the exact version, commit/tag, artifact/check results and published URL or remaining step. Version edits, successful local checks, a push, a tag and a published release are different facts. Do not claim a release from local simulation.

After drafting the report, load [delivery checks](../references/delivery-checks.md). Correct supported issues and expose unresolved conditions; otherwise keep the check silent, without another report or round.
