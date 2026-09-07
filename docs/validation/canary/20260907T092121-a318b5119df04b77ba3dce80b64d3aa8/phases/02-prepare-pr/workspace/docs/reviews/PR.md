# Add optional coverage to local checks and clarify contributor docs

Contributors now get branch coverage and missing-line output from the normal
`tools/check.py` command and existing commit hook when coverage is available in
the prepared interpreter. Measurement starts before discovery and uses the existing
`.coveragerc`; `quality.ini` still controls the full unittest suite. An absent
coverage package produces an explicit stdlib-only fallback; test failures and empty
discovery still fail the gate.

README now includes output-directory creation in the runnable example and focuses
on the existing CSV/JSON contract. DEVNOTES owns check and hook operations; original
implementation notes and session evidence are retained under `docs/`. Application
behavior, dependencies, hook scheme and version are unchanged.

Validation performed for this draft: the actual installed hook passed all five
tests using CANARY_PYTHON, with 96% displayed application coverage. The generated
JSON was checked for application-only scope and branch measurement. `git diff
--check` passed; the index is unchanged and has no staged changes. See
[fresh validation and input identities](../validation/2026-09-07-prepare-pr-output.txt).
Git emitted sandbox cache/config-access diagnostics despite exiting successfully.

The [prior setup record](../validation/2026-09-07-local-setup.md) and linked output
retain failure, empty-discovery, outside-root and absent-coverage probes; those
probes were not rerun for this draft. Coverage has no percentage threshold, and
fallback runs produce no coverage reports; existing reports can be stale after
failed or fallback runs. No remote CI or external integration was exercised.

Human maintainer review is pending. Next: review the checker’s coverage/fallback
behavior, documentation moves and linked evidence before deciding whether to
approve the setup changes. This is a local draft; no remote PR, commit, push, tag
or release was created.
