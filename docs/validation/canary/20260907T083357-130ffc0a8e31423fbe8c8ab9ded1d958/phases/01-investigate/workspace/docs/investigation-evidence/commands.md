# Reproduction record

Run from the fixture root using the supplied `CANARY_PYTHON`. No packages or external services were used. Fixture data is generated deterministically in workspace-local temporary files and removed by the probe.

```sh
mkdir -p docs/investigation-evidence scratch/order-report-investigation
TMPDIR="$PWD/scratch/order-report-investigation" PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v > docs/investigation-evidence/baseline.txt 2>&1
TMPDIR="$PWD/scratch/order-report-investigation" PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" scratch/order-report-investigation/probe.py > docs/investigation-evidence/probe.txt 2>&1
```

Baseline: exit 0, two tests passed; stdout/stderr in `baseline.txt`. Probe: exit 0, stdout/stderr in `probe.txt`; contains individual timings, profiles, call counts, correctness checks and source/test fingerprints. Timing uses `time.perf_counter`; profiling and mocked call counting are separate from timing. The candidate is only in the scratch probe, with no production edits.

An initial `git status --short` emitted sandbox warnings about the default xcrun temporary cache and user git ignore file. These were repository-inspection warnings, not test failures. Final inspection used a workspace-local TMPDIR and disabled optional git locking; xcrun cache warnings persisted, but both commands exited 0. Status listed only untracked `docs/` and `scratch/`; the production/test/input diff was empty:

```sh
TMPDIR="$PWD/scratch/order-report-investigation" GIT_OPTIONAL_LOCKS=0 git -c core.excludesFile=/dev/null status --short
TMPDIR="$PWD/scratch/order-report-investigation" GIT_OPTIONAL_LOCKS=0 git diff -- report.py tests README.md DEVNOTES.md AGENTS.md
```
