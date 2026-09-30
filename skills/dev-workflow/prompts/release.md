# Prepare or execute a release

Identify the requested operation: readiness assessment, version/notes preparation, tagging, publication or retry decision. Read project release rules and existing authorization, then perform only that operation and its necessary authorized prerequisites. Readiness-only work does not imply version edits or publication; continue actions already authorized without asking again.

## Version and candidate

For version/notes preparation, establish the last released version, completed changes since it, and the project's compatibility and prerelease/0.x policy. Determine whether the authoritative version source still names that baseline or already contains a prepared target; derive or verify the target accordingly. Its current value alone is not the target decision, and an already prepared candidate needs no second bump. Move only the selected Unreleased notes under that version/date, leave prior releases intact, and retain an Unreleased section. Review metadata and notes together; planned features are not delivered changes.

For readiness or execution, apply required PR/review and release gates, including deferred expensive suites and required baseline comparisons. Evidence must apply to the final candidate, relevant inputs/runtime and configuration; agent evaluations also depend on fixtures, graders and settings. Missing, stale, failed or inconclusive required evidence leaves release pending. Reuse applicable results without skipping mandatory gates. After fixes, rerun affected checks and retain failed attempts/dispositions. Verify the final merged commit, including conflict resolution and relevant CI, rather than assuming feature-branch evidence transfers unchanged.

## Tag and artifact

Within scope, tag the exact verified release commit, then build and validate the distributable from that tagged content. Smoke-test the actual artifact where applicable before authorized publication. Preserve the source commit, version, tag and artifact identity association. Inspect existing tags/releases before retrying; never implicitly move or replace them.

## Uncertain external writes

After an ambiguous publish or other external-write response, inspect authoritative status and compare source/tag/artifact identity before retrying. Matching confirmed completion needs no duplicate write. Conflicting identity must be preserved and resolved before proceeding. Unknown status remains unknown: stop the mutation path until reliable state or a service-supported idempotent retry can establish safety. Reuse the same operation identity where supported; a fresh key, rebuild or new tag does not resolve an uncertain prior write. Do not infer failure from a timeout or success from a matching local tag. Bound status checks to useful new evidence rather than looping indefinitely.

When the task supplies frozen observations or asks only for advice, assess those inputs and state their limits; do not claim live verification or perform additional writes. Report the supported identity comparison and next action.

Finish with the operation's actual outcome and material remaining conditions. Make the relevant version, commit/tag, artifact/check results and observed publication URL easy to find when available. Version edits, local checks, pushes, tags and publication are distinct facts; local simulation is not a published release. No separate report is required unless requested or maintained by the project.
