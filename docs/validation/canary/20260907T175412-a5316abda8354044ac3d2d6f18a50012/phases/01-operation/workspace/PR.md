# Preserve surrounding spaces in exported text (incomplete)

Local draft for candidate `1e5d68c882c6398bc27bde30521476e5c14888a8`; tracked files were clean before preparation.

The requirement in [CHANGE.md](CHANGE.md) treats surrounding spaces as user data. The current regression test expects `serialize("  x  ")` to return `"  x  "`. Actual behavior remains `"x"`: `serialize` calls `str(value).strip()`. The candidate captures the new requirement in a test but does not yet deliver the behavior change.

Validation: ran the mandatory gate from [DEVNOTES.md](DEVNOTES.md), `python -m unittest discover -s tests -v`, using the supplied runtime as `"$CANARY_PYTHON" -m unittest discover -s tests -v`. Exit status: **1**; one test ran and failed (`test_spaces_are_data`). See the [current gate output](evidence/prepare-pr-gate.log).

The passing result in [previous-report.md](previous-report.md) applies only to the previous candidate's normalized-string contract and test configuration. It is preserved as historical evidence, not reused as current validation.

Blockers: implementation still removes required spaces, and the mandatory gate fails. Reconcile the implementation with the preservation requirement and rerun the gate before marking this change ready. No remote CI or release validation was performed.

Preparation only: no product code or tests changed; no commit, publication, or version bump. The existing Unreleased entry already describes preservation as in progress.
