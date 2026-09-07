# Migration planning evidence — 2026-09-07

Scope: fresh-context fixture inspection and bounded standard-library experiments.
This is evidence for proposals, not a design review, plan review, or migration run.

Read `AGENTS.md`, both requested skills and their drafting/planning prompts and
templates; inspected `settings.py`, `tests/test_settings.py`, all three data files,
README, DEVNOTES, ORIGINAL, DESIGN and PLAN. No other reports appeared in the
fixture file listing. Original requirements and historical design/plan text retained.

## Actual checks

`"$CANARY_PYTHON" -B -m unittest discover -s tests -v` exited 0:

```text
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok
Ran 2 tests in 0.000s
OK
```

Prepared-runtime JSON probe (no file writes):

```text
json.dumps({"version": 2, "settings": {1: "a"}})
=> {"version": 2, "settings": {"1": "a"}}
json.dumps({1: "a", "1": "b"})
=> {"1": "a", "1": "b"}
json.loads('{"settings":{"theme":"dark","theme":"light"}}')
=> {'settings': {'theme': 'light'}}
```

This verifies that naive conversion/parsing can change ID identity and silently
drop entries. The supplied normal fixture contains only string IDs; it does not
establish that every previously readable v1 file has string IDs.

Filesystem probe: used `tempfile.TemporaryDirectory(dir=".")`, wrote a disposable
old selector and a new temporary file, flushed/fsynced the new file, called
`os.replace` in that directory, then `os.fsync` on an open directory descriptor.
Exit 0; observed selected contents `new`. The probe directory was automatically
removed. No fixture data was modified. This demonstrates syscall availability in
this workspace, not crash/power-loss behavior or support on other filesystems.

`git status --short` produced no changed-path output before document edits, but
printed sandbox warnings about xcrun cache creation and global ignore access.
No access escalation was requested; this is not evidence of an unrestricted Git
environment. No commits, installs or external actions occurred.

## Not verified

No migration implementation, crash/retry tests, v2 reader tests or design/plan
reviews have been performed. All acceptance examples and stage checks beyond the
two baseline tests are proposed. Deployment filesystem durability and caller
compatibility remain review inputs.
