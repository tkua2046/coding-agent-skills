# Reproduction record

Executed from the fixture root with the supplied `CANARY_PYTHON` runtime. Directory creation preceded execution. Both commands exited 0; captured stdout/stderr is linked below. The probe creates and removes its synthetic catalog beneath this evidence directory. It does not edit production code or tests.

```sh
mkdir -p docs/evidence/order-report-20260907-0835/tmp
TMPDIR="$PWD/docs/evidence/order-report-20260907-0835/tmp" PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v > docs/evidence/order-report-20260907-0835/baseline.txt 2>&1
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" docs/evidence/order-report-20260907-0835/probe.py > docs/evidence/order-report-20260907-0835/results.txt 2>&1
```

- Baseline: exit 0, [output](baseline.txt).
- Probe: exit 0, [output](results.txt); Python 3.12.4 on macOS ARM64.
- SHA256 before/after for `report.py` and `tests/test_report.py` match in the probe output.

Initial `git status --short` returned no change entries, but emitted sandbox warnings about inaccessible external Git configuration and xcrun temporary cache creation. File hashes and the limited edits provide the preservation evidence; Git warnings are not treated as a test failure or a clean-check guarantee.
