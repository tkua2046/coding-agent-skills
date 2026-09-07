# Local evidence — 2026-09-07

Run from the fixture root using the supplied `CANARY_PYTHON`, with temporary files
inside the workspace. No packages or remote services were used.

```sh
mkdir -p docs/investigation-evidence .investigation-tmp
TMPDIR="$PWD/.investigation-tmp" PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v > docs/investigation-evidence/baseline.txt 2>&1
TMPDIR="$PWD/.investigation-tmp" PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" docs/investigation-evidence/probe.py > docs/investigation-evidence/results.txt 2>&1
```

Both Python commands exited 0. The baseline ran two tests successfully; the probe
passed all assertions. `results.txt` includes interpreter/platform, source/test
SHA256 hashes, all timing samples, loader counts, profiles and compatibility results.
Timings exclude synthetic input construction and output-equality assertions.
The call-count wrapper is used separately from timings and profiling.
Temporary catalogs are removed automatically on probe completion.

Initial `git status --short` returned 0 with no changes listed, but printed sandbox
warnings about Git's external cache/config locations. Final verification uses a
workspace temporary directory and disables external Git configuration. Git's
launcher still printed external cache warnings; status listed only `?? docs/`,
and the source/test/input diff printed no changes. An independent Python SHA256
comparison against the hashes in `results.txt` exited 0 and printed
`Production/test hashes unchanged`. No commit was created.
