# Add optional coverage to local checks and clarify contributor docs

Contributors now get branch coverage and missing-line output from `tools/check.py`
and the existing commit hook when coverage is available in their interpreter.
The command uses the established `.coveragerc` and `quality.ini`; without coverage,
it explicitly reports the limitation and still runs the full unittest gate.
Test failures and empty discovery remain failures, with no coverage percentage gate
or new dependency requirement.

README now includes directory creation in the runnable example and focuses on the
CSV/JSON utility's usage. DEVNOTES owns check, coverage and hook operations; the
original implementation notes and dated session record are preserved in
[development history](../development-history.md). The application contract,
test discovery convention and hook delegation remain intact.

Validation during this handoff passed for the normal check command, actual installed
hook and stdlib fallback using `CANARY_PYTHON`. Coverage reports were produced by
the first two runs. See [current validation](PR-validation.md) for commands,
results, candidate fingerprints and separately identified prior setup evidence.

Limits: coverage measures `inventory.py`, not the check runner; missing coverage
support leaves any existing reports stale. Failure/empty-discovery probes are
retained prior results, not newly rerun checks. Validation is local only; no CI or
external integration ran. Detailed artifacts are ignored local files and must
accompany this draft if it is moved to another checkout.

Maintainer human review is pending. Next: review the complete setup diff against
the baseline, including the new history file, and assess the optional-coverage
behavior and documentation preservation using the linked evidence. This is a
local draft; no remote PR, commit, push, tag, version bump or release was performed.
