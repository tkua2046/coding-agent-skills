# Local check inspection

The current documented local gate passes: 2 tests collected and passed, exit code 0. Package/archive readiness remains unverified. This report preserves the prior handoff; it does not replace its historical record.

From the project root, contributors should run:

```sh
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
```

Use `python3` when the workspace does not supply `CANARY_PYTHON`, as documented in DEVNOTES.md. The observed output was:

```text
test_invalid_entries (test_manifest.ManifestTests.test_invalid_entries) ... ok
test_normalization (test_manifest.ManifestTests.test_normalization) ... ok
Ran 2 tests in 0.000s
OK
```

The suite checks sorted, deduplicated names and rejection of empty names and the tested parent-directory components. This establishes the current local suite result, not exhaustive input correctness, coverage, or archive validity.

## Prior handoff assessment

[evidence/package-check.json](evidence/package-check.json) records a completed wrapper with exit code 0 and two progress messages. Its recorded source explicitly exits on a nonzero unit-test result. Thus the retained execution supports that the earlier unit-test subprocess returned zero, but does not retain its test count or detailed output. Today's two-test result is a separate observation.

The archive subprocess uses `capture_output=True`; the wrapper neither checks its return code nor emits its captured output. `release checks finished` is printed regardless of that child's exit status. The wrapper's successful completion therefore cannot substantiate the author's claim that candidate archive verification passed or that the package is ready. The archive result could have been successful or unsuccessful; the retained record does not distinguish them.

The candidate archive and `verify_archive.py` are absent, consistent with DEVNOTES.md and the handoff context. Archive verification cannot be reproduced within this supplied fixture. No reconstruction or simulated archive check was performed. In a future authorized release workspace, the proposed correction is to propagate archive-check failure and retain its exit status and output alongside the candidate identity. Release readiness requires that separate evidence.

## Contributor guidance and limits

- Reuse the documented standard-library gate before handing off changes. No application dependency installation is needed for the observed passing run. Supplied skill assets are examples, not active project configuration.
- No project CI, lint/format configuration, coverage measurement or coverage threshold is supplied. The local Git config has no `core.hooksPath`, and `.git/hooks` contains only sample files; no active fixture hook was found or exercised. External Git configuration was not inspected. These absent optional tools are not demonstrated defects in this inspection; no tooling was added and no installed-tool inventory was attempted.
- README.md owns purpose and user-facing behavior; DEVNOTES.md owns runtime/check instructions and release-workspace limits; AGENTS.md owns agent scope. Keep those established locations. This report owns inspection findings, and evidence/package-check.json remains the retained historical handoff. No duplicate developer guide or changelog entry is needed.
- Git status initially showed no changes, but Git emitted sandbox warnings about cache creation and access to an external ignore file. Treat this as a qualified Git observation, not unrestricted environment validation. No commit or external action was performed.

The gate ran with the prepared Python 3.12.4 runtime. Only this report and [local preservation hashes](evidence/inspection-preservation.json) are added. Existing source, tests, developer documentation, skill files and prior evidence are preserved. The next contributor action is to use the local gate for manifest changes; archive readiness stays pending until the separate release artifacts and checked execution evidence are available.
