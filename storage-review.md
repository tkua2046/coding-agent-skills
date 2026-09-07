# Storage and packaging review

Current verdict: **ready for the reviewed storage/packaging scope**. Open findings: none. SR1 is reviewer-verified resolved. Next: main's remaining delivery checks and required acceptance. The original finding and assessment below are retained; the recheck follows them.

Independent review of storage/packaging changes from `a24b140ddda594bec61ae42ac272d3225892cfb5`: `tools/canary.py`, `tools/check.py`, changed tests, and `evals/graders/nested-output-provenance.json` with its retained fixture. No review of my own skill edits. Reviewed code SHA-256: canary `d8a07cfe623a4515e43b5e092ac69b44c80dc3c190148d4afb0bc6b9b7eb6b70`; checker `65353d4fcdd8a676497b02394e9808496a65de9770e8f06ca4f30645d828614d`.

## SR1 — [P2] Noncanonical explicit filenames bypass collection discovery

Location: `tools/canary.py:1251–1263`, specifically the filename filter at line 1255.

The gate accepts and verifies arbitrary explicit report filenames, but includes their sibling attempts only when the supplied basename is `report.json`. In a complete relocated evidence tree outside the canonical locations, copies named `selected.json` in the same run directories therefore exclude a retained newer failure from consideration. No report bytes, hashes, identities or calibration records need modification. The gate can return pass despite the newer failure for the same candidate/settings/environment.

Executed one isolated offline counterexample using the existing synthetic runtime helpers: generate passing calibration, comparable baseline and passing candidate, then a newer genuine synthetic candidate failure; move the complete collection; call the gate with the older standard report paths; copy those two reports byte-for-byte to `selected.json` alongside their originals and call again. Observed:

```text
canonical_report_paths: fail
aliased_identical_report_paths: pass
aliased_errors: []
newer_failure_still_present: true
```

Correction: either reject noncanonical explicit report filenames before acceptance, or include their collections consistently. Verify that aliases cannot bypass newer failed or unfinished sibling attempts. This needs a focused regression, not broader discovery of scratch trees. Disposition: open.

## Remaining assessment and limits

- Standard report paths include immediate sibling reports and unfinished attempts in explicit, current and legacy collections. Nested captured workspaces and unrelated backups remain outside discovery. Existing changed tests cover those boundaries; I did not rerun the suite.
- Complete-tree relocation preserves relative calibration references. Report hashes, required control evidence, execution completion and recomputed calibration judgments reject missing/tampered dependencies. Legacy inline calibration still uses its retained evidence; changed engine identity prevents historical evidence from becoming current acceptance. No further material defect found by inspection.
- Ordinary offline checks use maintained source/fixtures, not the removed execution archive. The 54,681-byte retained fixture exactly matches its Git object at `a24b140`; its SHA-256 matches provenance, and both selected original stdout events match the calibration excerpts. These were direct byte comparisons, not model evaluations.
- Shared calibration plus a legacy reader and shallow collection discovery is proportionate to the storage change. The retained regression input has a concrete offline consumer; I found no additional unnecessary mechanism requiring rejection.

Only the focused counterexample and read-only provenance comparisons were executed. Temporary probe files were removed automatically. No product files, skills or tests were changed; this report is the sole review output. No claim of full-suite success or human acceptance.

## SR1 recheck — reviewer verified

Reviewed `tools/canary.py` SHA-256 `e21cbaef4a8b488187525739a55c7625a077b392150bec760b8b02b86bc81ab1` and the corresponding alias regression changes in `tests/test_canary.py` (`d1425a3de9d6945192580f801a66b8cc248ca51441411670d1afdd7311bcde0b`). The checker remains at its original reviewed hash.

Lines 1252–1257 now add a blocking error for every explicit basename other than `report.json`, before collection expansion. That error survives successful record verification and forces the final verdict to fail. Standard collection discovery is unchanged, so rejecting aliases does not broaden scanning into unrelated scratch.

Repeated only the original retained [probe](storage-alias-probe.py), unchanged SHA-256 `2a8383644ed56755fd23f22589f74ca69ef38386e54fe870b6abed4f935ff1da`, from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B - < artifacts/repair/storage-alias-probe.py
```

Observed: `canonical_report_paths: fail`, `aliased_identical_report_paths: fail`, and `newer_failure_still_present: true`. Both aliases produced the explicit error “use report.json in its complete evidence collection; renamed report aliases cannot establish release acceptance.” The original pass-through defect is closed on the reviewed code.

Inspected the test update: both relocated failure and unfinished-attempt variants now submit byte-identical aliases and require failure with the alias diagnostic. Main's [focused regression log](alias-regression.log) reports `3 passed, 164 deselected in 4.77s`; I read that result and did not repeat those tests. This recheck changed only this report. The original finding, original observation and retained probe remain available. No additional material finding; no full-suite or human-acceptance claim.
