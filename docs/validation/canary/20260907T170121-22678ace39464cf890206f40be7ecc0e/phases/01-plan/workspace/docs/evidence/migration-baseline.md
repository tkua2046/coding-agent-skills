# Local baseline evidence — 2026-09-07

Fresh-context inspection and bounded experiments only. No implementation, design
review or plan review performed; no installs, commits or external services used.
Prior design/plan text is retained in those documents.

## Inspected inputs

Read fixture AGENTS, both requested skills and their drafting prompts/templates,
ORIGINAL, prior DESIGN/PLAN, README, DEVNOTES, `settings.py`,
`tests/test_settings.py`, and all three data files.

Reader supports v1 and rejects duplicate IDs before dictionary construction. Normal
fixture has theme `dark` and timeout `30`; duplicate fixture has theme `dark` and
`light`. Selector has format 1 and relative path `settings-v1.json`. No selector
reader or migration implementation exists.

## Actual baseline checks

Prepared runtime, bytecode writes disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v
```

Exit 0:

```text
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok

Ran 2 tests in 0.000s

OK
```

## Bounded compatibility probe

Question: does naive dictionary-to-v2 serialization preserve every input the current
reader accepts? Using the prepared runtime and standard-library
`unittest.mock.patch('builtins.open', mock_open(read_data=raw))`, called actual
`settings.load` on these in-memory inputs; no fixture files changed.

| Raw v1 JSON | Actual reader result |
|---|---|
| `{"version":1,"entries":[{"id":7,"value":"seven"}]}` | `{7: 'seven'}` |
| `{"version":1,"entries":[{"id":"timeout","value":NaN}]}` | `{'timeout': nan}` |
| `{"version":1,"entries":[{"id":"theme","value":"dark","value":"light"}]}` | `{'theme': 'light'}` |

For numeric ID input, `json.loads(json.dumps({'version': 2, 'settings': result}))`
produced `{'version': 2, 'settings': {'7': 'seven'}}`. This observed ID type change
means the old reader alone cannot establish lossless migration. Rejecting these
migration inputs is a proposed policy, pending review.

## Limits

Only baseline tests and compatibility probes ran. No migration, fault injection,
subprocess crash test, filesystem durability experiment or power-loss test was run.
Future acceptance in SPEC is not a completed result. Initial `git status --short`
emitted sandbox warnings about unavailable external cache/ignore paths and no changed
file lines; this is not evidence of migration correctness. All work used this fixture.
