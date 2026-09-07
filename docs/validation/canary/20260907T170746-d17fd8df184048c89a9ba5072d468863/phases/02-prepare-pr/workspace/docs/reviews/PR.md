# Add optional coverage to local checks and clarify contributor docs

The normal check previously required separate coverage commands, and README
mixed user instructions with development records. `tools/check.py` now measures
application coverage when available in the prepared interpreter, prints missing
lines and writes the configured reports. For example, running the existing
installed pre-commit hook now runs all five tests and produces coverage in one
step. Without coverage, it explicitly reports the limitation and runs the same
stdlib suite. Test failures and empty discovery remain failing gates.

README now includes output-directory creation in its runnable example and links
to contributor operations in DEVNOTES. Original implementation notes and session
history are preserved in [development history](../DEVELOPMENT_HISTORY.md).
The CLI and CSV/JSON contract, custom test discovery, coverage configuration and
existing hook delegation are unchanged; no dependencies were added.

Validation for this local working-tree snapshot over `e39e359` (7 September 2026):

- Ran the actual installed `.git/hooks/pre-commit` with `CANARY_PYTHON`
  (Python 3.12.4, coverage 7.16.0) and repository-local `TMPDIR`: exit 0,
  all five tests passed. Application coverage displayed 96%: 57/58 statements
  and 16/18 branches covered. The installed wrapper matches the maintained copy.
- Current command, output, coverage snapshot and input hashes are in
  [local validation evidence](../../artifacts/pr-draft-verification/results.json)
  and [hook output](../../artifacts/pr-draft-verification/installed-hook.log).
- Earlier failure, empty-discovery, documentation-only staging and simulated
  coverage-absence probes are retained in [setup verification](../LOCAL_CHECK_VERIFICATION.md);
  these were inspected, not rerun during this handoff.

Limits: coverage targets only the application and has no percentage threshold.
The fallback can leave stale reports; earlier empty-discovery probes also showed
coverage errors after the no-tests diagnostic. Detailed evidence directories are
ignored and local to this checkout. No remote CI or external integration ran.

Next action: maintainer human review of the setup diff, documentation and linked
evidence is pending after this handoff. This is a local PR draft; no remote PR,
commit, push, tag, version bump or release was performed.
