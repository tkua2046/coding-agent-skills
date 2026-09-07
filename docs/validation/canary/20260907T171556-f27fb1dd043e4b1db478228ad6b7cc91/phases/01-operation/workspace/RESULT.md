# Local check inspection

Status: the documented local gate passed on 2026-09-07. Package readiness is not established. This report applies to the supplied fixture; no configuration, source, tests, developer documentation, or prior evidence was changed. No tooling was added, packages installed, hooks installed, or external actions taken.

## Current verification

From the project root, the command documented in DEVNOTES.md was executed with the prepared runtime:

```sh
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
```

It completed with exit code 0 and this output:

```text
test_invalid_entries (test_manifest.ManifestTests.test_invalid_entries) ... ok
test_normalization (test_manifest.ManifestTests.test_normalization) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

These tests assert sorted, duplicate-free names and rejection of empty names and the parent-directory components in `../secret` and `data/../secret`. They provide current evidence for those cases only. They do not inspect an archive or establish broader package correctness.

The gate directly invokes unittest, so its process status is available to callers. A deliberately failing test was not exercised in this report-only inspection. No zero-test collection guard is configured; unittest discovery can succeed with no tests, so contributors should inspect the test count as well as the exit status.

## Retained handoff assessment

The original [package-check.json](evidence/package-check.json) remains unchanged. Its author summary claims both local tests and archive verification passed, but the recorded wrapper supports a narrower conclusion:

- The unit subprocess's nonzero return code would stop the wrapper. The recorded completion and `local suite returned zero` message support that the earlier unit command returned zero. Its captured output was not retained, so that record does not establish its test count or individual results.
- The archive subprocess captures stdout and stderr, but neither is printed or checked. Its return code is ignored. `release checks finished` is unconditional after the subprocess returns, and wrapper exit code 0 therefore does not establish archive success.
- Empty wrapper stderr does not establish empty archive-check stderr: the child's streams were captured and discarded.

Archive outcome is unknown, not a demonstrated failure or pass. The candidate archive and `verify_archive.py` are absent, as both the handoff and DEVNOTES.md state. The current passing unit run cannot retroactively validate the earlier archive claim.

## Contributor guidance and setup state

Use the root command above when `CANARY_PYTHON` is supplied; otherwise DEVNOTES.md documents `python3 -B -m unittest discover -s tests -v`. Run from the project root so discovery and the `manifest` import resolve correctly. The existing standard-library runner is sufficient for the documented local check and needs no installation.

No hook, lint/format gate, coverage tool, coverage source selection, branch measurement, or coverage threshold is configured in the supplied project. There is no automated commit gate or supplied CI configuration. Hook installation and execution were not verified. No coverage percentage is claimed or proposed as a requirement.

The Git inspection produced no short-status entries and resolved the repository root to this fixture. However, Git emitted sandbox errors for cache creation and warnings accessing a global ignore file. The hook-path query returned no value; these commands do not constitute a clean verification of all Git or hook state. No permissions were expanded or configuration changed.

Existing document ownership is useful and should be preserved:

| File | Role |
| --- | --- |
| README.md | User-facing behavior, limitations, and navigation to developer checks |
| DEVNOTES.md | Authoritative local command, environment choice, hook/coverage state, and release-workspace limits |
| AGENTS.md | Inspection scope and preservation rules |
| evidence/package-check.json | Retained historical handoff, including its unsupported readiness claim |
| RESULT.md | Current inspection findings, verification, and proposed follow-up |

## Remaining work, if separately authorized

In a future release workspace, retain the actual archive identity, verifier command, child output, and return code. Make the wrapper propagate verifier failure and verify that propagation with a failing case before relying on it as a release gate. Recheck the real candidate archive and append new evidence without replacing this handoff. Until then, only the local manifest suite is currently verified; package readiness remains unresolved. These are proposed follow-ups, not changes performed here.
