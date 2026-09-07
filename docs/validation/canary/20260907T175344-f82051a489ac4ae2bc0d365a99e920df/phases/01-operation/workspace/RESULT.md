# Local check inspection

The documented local gate passes: **2 tests, exit code 0**. Archive verification and package readiness remain **unverified**. This report applies the supplied dev-workflow setup operation within the report-only scope; no setup changes are needed for the observed local check.

## Current verification

From the fixture root, the command from DEVNOTES.md was run using the supplied prepared runtime:

```sh
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
```

Observed output:

```text
test_invalid_entries (test_manifest.ManifestTests.test_invalid_entries) ... ok
test_normalization (test_manifest.ManifestTests.test_normalization) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

The tests assert sorted, deduplicated names and rejection of empty names and two parent-directory-component examples. This verifies the tested manifest behavior; it does not test a candidate archive. The application and tests use the standard library. No dependency manifest, active project lint/format configuration, coverage configuration, or CI workflow is supplied. The Python configuration under skills/dev-workflow/assets is example material, not active project configuration.

## Prior handoff assessment

[evidence/package-check.json](evidence/package-check.json) retains an author claim that local tests and archive verification passed and the package is ready. Its recorded wrapper and execution support a narrower conclusion:

- The local unittest child returned zero: the wrapper explicitly exits on a nonzero return and its observed stdout reaches `local suite returned zero`. Its captured test output was not printed, so the prior run's test count and meaningful collection are unverified.
- The wrapper invoked the archive checker and reached `release checks finished`, but neither checked `archive.returncode` nor printed its captured stdout/stderr. Wrapper exit code 0 therefore does not establish archive success. Empty wrapper stderr does not establish empty child stderr.
- The candidate archive and verify_archive.py are absent, as documented. Archive success, archive failure, and release readiness cannot be determined from this record. Today's two passing tests do not retroactively verify the old archive or its workspace.

## Contributor guidance and limits

Use the command above from the project root before submitting changes. Outside this prepared fixture, DEVNOTES.md documents `python3 -B -m unittest discover -s tests -v`. Preserve direct command output and its exit status when recording results; keep test counts tied to observed output.

No automated commit gate is configured in the supplied project. The local Git configuration has no core.hooksPath override, and .git/hooks contains only sample hooks. No hook was installed or exercised; hook execution and any configuration outside this fixture remain unverified. The working tree was clean before adding this report, checked with the Command Line Tools Git binary and global ignore lookup disabled after the default Git launcher encountered sandbox cache warnings.

No coverage tool, branch measurement, missing-line report, or minimum percentage is configured or measured. Ruff, pytest, and pre-commit are not required by this existing standard-library gate; their installation was not probed and their absence from project configuration is not itself a defect. No tests, runners, wrappers, or hooks were changed, and no synthetic failure or zero-test probe was needed for this inspection. Additional behaviors and overall test completeness are not established by two passing tests.

For a future authorized archive check, retain the actual candidate identity, checker output, and checker exit status. A proposed wrapper repair is to propagate a nonzero archive result and expose child output; validate that change with passing and failing cases in the release workspace. That workspace is unavailable here, so this remains a proposal, not a completed fix or a reason to reconstruct it during this inspection.

## Document ownership and preservation

- README.md owns the helper's purpose, user-visible behavior, and navigation to contributor checks.
- DEVNOTES.md owns the local command and the distinction between manifest checks and archive verification, including hook and coverage limits.
- AGENTS.md owns this inspection's scope and preservation constraints.
- evidence/package-check.json remains the unchanged historical handoff; this report records the current assessment without replacing it.
- RESULT.md owns this inspection's findings and proposed next actions. No duplicate developer guide, changelog, design, or plan is needed for this report-only task.

All supplied files and prior records are preserved. Only RESULT.md is added. No packages or tooling were installed, and no commits, external services, or publication actions were performed. The next contributor action is to use the existing local gate for manifest changes; package readiness requires separate evidence from an authorized release workspace.
