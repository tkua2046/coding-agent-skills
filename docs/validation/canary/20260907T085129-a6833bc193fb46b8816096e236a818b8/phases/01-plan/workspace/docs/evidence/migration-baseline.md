# Migration baseline evidence

Date: 2026-09-07. Scope: supplied fixture only, fresh design/planning phase.

Read `AGENTS.md`, both requested skills and their drafting/planning prompts and templates, `docs/ORIGINAL.md`, existing design/plan, README, DEVNOTES, `settings.py`, `tests/test_settings.py`, and all three data files. No other implementation or review reports appeared in the fixture inventory. Original requirements and prior design/plan text are retained.

Observed reader: `json.load`, version-1 check, duplicate-ID check, then dictionary construction. No v2 reader, selector integration, persistence code or recovery tests exist. Active selector is format 1 pointing to `settings-v1.json`; normal entries are theme=`dark`, timeout=`30` (JSON number). Duplicate fixture repeats theme with dark/light.

Actual check:

```text
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok
Ran 2 tests in 0.000s
OK
```

Exit code: 0. This verifies existing v1 behavior only. All migration acceptance, durability and interruption checks in the design/plan remain proposed. No packages installed, external services used, commits created or implementation files edited.

Initial `git status --short` emitted sandbox warnings about unavailable developer-tool cache and user ignore configuration, with no status entries. That command is not evidence of migration correctness. No denied-path inspection or permission escalation was attempted.
