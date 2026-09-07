# Integrate optional coverage into the local check gate and clarify contributor docs

Contributors now get branch coverage and missing-line reports from `tools/check.py`
and the existing commit hook when their interpreter provides coverage. Measurement
starts before test discovery and uses the existing `.coveragerc`; invocation from
another directory resolves paths consistently. The configured `qa/check_*.py`
suite and failure/zero-test gates remain in place. Without coverage, the gate
explicitly reports the limitation and runs unittest without installing dependencies.

README now includes output-directory creation in the quick start. Contributor
operations live in DEVNOTES, and implementation notes and the historical session
record are preserved in [development history](../DEVELOPMENT_HISTORY.md).
The application CLI and CSV/JSON contract are unchanged.

- **Current validation:** the actual installed hook and the normal gate invoked
  from `qa/` passed using `CANARY_PYTHON`; both reported 96% application coverage.
  `git diff --check` returned zero, with sandbox cache warnings. See
  [validation evidence](validation-2026-09-07/README.md) for commands, logs,
  candidate hashes, and the distinction between current and retained setup results.
- **Limits:** coverage is optional, has no enforced percentage, and is incomplete.
  Failure/empty-discovery and stdlib-fallback probes are retained prior evidence,
  not fresh runs. No remote CI or external integration ran. Ignored raw setup
  artifacts are available in this checkout only.
- **Next action:** maintainer human review is pending. Review the check-runner diff,
  documentation move, and linked evidence against baseline `df6182f`, then decide
  whether to accept the setup/adaptation changes. This is a local draft; no remote
  PR, commit, push, tag, version change, or release was performed.
