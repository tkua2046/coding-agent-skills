# Integrate optional coverage into local checks and clarify contributor docs

Contributors now get missing-line coverage output and a JSON report from
`tools/check.py` and the existing full-suite commit hook whenever their prepared
interpreter provides coverage. Previously, coverage required separate commands.
The gate retains `quality.ini` discovery and failure/empty-suite rejection; when
coverage is unavailable, it explicitly reports that limit and runs stdlib tests.
Existing application-only branch coverage settings and the no-threshold policy
remain in place.

README now gives users a runnable example including destination-directory creation.
DEVNOTES owns check, coverage and hook instructions, while
[development history](../development-history.md) preserves the implementation notes
and historical session. The exporter CLI and CSV/JSON behavior are unchanged.

Validation during this PR preparation passed through the actual installed hook
using `CANARY_PYTHON`, and through the check command with `-S` to exercise the
coverage-unavailable fallback. `git diff --check` also passed. See
[current validation](PR-validation-20260907.md) for commands, results and candidate
identity. The [prior setup verification](../workflow-verification-20260907.md)
retains earlier failure and empty-discovery probes; those were not rerun here.

Coverage is optional and has no percentage gate. Raw evidence is retained locally
under ignored `artifacts/` and will not accompany a fresh checkout. No remote CI
or external integration was run; these local checks do not establish release
readiness.

**Human review pending.** Next, the maintainer should review the setup diff,
documentation moves and linked validation, then decide whether to accept it.
This is a local draft; no remote PR, commit, push, tag, version bump or release
was performed.
