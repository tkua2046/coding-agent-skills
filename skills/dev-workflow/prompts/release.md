# Prepare and execute an authorized release

Identify the requested operation: version/notes preparation, tagging, or publishing. Read repository release rules and existing authorization. Continue already authorized actions; a general reference to this procedure does not itself authorize publishing.

1. Identify the single authoritative version source and the public compatibility contract. Choose the version based on actual changes; account for prerelease/0.x policy rather than blindly mapping every feature to a bump.
2. Keep significant completed changes under Unreleased until release preparation. Move the chosen notes to the actual version/date, retain a new Unreleased section, and review version metadata and notes together. Never list planned features as delivered.
3. Complete the required PR/review process. Verify the final merged commit, including conflict-resolution changes and relevant CI, rather than assuming the old feature-branch result still applies.
4. Tag the exact verified release commit within the requested scope. Inspect an existing tag/release before retrying; do not move or replace one implicitly. Build and validate any distributable from that tagged content.
5. Smoke-test the actual artifact where applicable, then publish when authorized. Preserve the association among source commit, version, tag and artifact. If publication status is uncertain, inspect remote state before retrying.

Report the exact version, commit/tag, artifact/check results and published URL or remaining step. Version edits, successful local checks, a push, a tag and a published release are different facts. Do not claim a release from local simulation.
