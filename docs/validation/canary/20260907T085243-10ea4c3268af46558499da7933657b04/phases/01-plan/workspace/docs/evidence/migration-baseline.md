# Local baseline evidence

Fresh design/planning phase, 2026-09-07. Inspected only fixture files and supplied
skills. No implementation, reviews, installs, commits or external actions.

Inspected `settings.py`, both tests, all three data files, README, DEVNOTES,
AGENTS, ORIGINAL and prior DESIGN/PLAN. The reader supports only v1 and rejects
duplicate IDs; there is no selector reader or migration. No prior review files
were found in the fixture file inventory. Historical design/plan text is retained.

## Actual checks

`"$CANARY_PYTHON" -m unittest discover -s tests -v`:

```text
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok
Ran 2 tests in 0.000s
OK
```

A standard-library inline probe used an automatically removed workspace-local
temporary directory. It read a numeric v1 ID, inspected JSON conversion/parsing,
flushed/fsynced a temporary selector, replaced it in the same directory, and
fsynced the directory. Results:

```text
JSON numeric object key round trip: {'7': 'value'}
Default JSON duplicate object key: {'settings': {'theme': 'light'}}
Current numeric ID load: {7: 'value'}
Same-directory replace: {'format': 2, 'path': 'target.json'}
Directory fsync: succeeded
Source unchanged: {"version":1,"entries":[{"id":7,"value":"value"}]}
```

This checks primitive availability, not migration correctness: the dummy selector
had no real v2 target. No crash was injected. The results do not establish
atomicity or durability under process/host/power crashes on supported platforms.

Baseline `git status --short` printed no changed paths but emitted sandbox
warnings about xcrun cache creation and global ignore access. No permission
changes or escalation were attempted.

## Not verified

V2 reading, strict validation, activation, collision handling, interruption and
retry checks remain proposed in SPEC/PLAN. Both document reviews remain pending.
README and DEVNOTES continue to describe current functionality; their future
changes belong with the planned implementation stages.
