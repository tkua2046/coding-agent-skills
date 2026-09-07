# Local inspection evidence — 2026-09-07

Scope: supplied fixture and skills only; fresh-context design/planning phase.
These are observations, not design/plan reviews. [PLAN.md](PLAN.md) owns status.

Inspected AGENTS.md, README, DEVNOTES, original requirements, prior design/plan,
`settings.py`, both tests and all three data files. The fixture listing contained
no nested AGENTS.md or prior review report. Captured prior design/plan verbatim
under `docs/history/` before revision. Original requirements remain unchanged.

The reader requires version 1, checks uniqueness using a set and returns a dict.
It contains no selector handling or persistence code. Data observations:

```text
active.json: {"format":1,"path":"settings-v1.json"}
settings-v1.json: theme="dark", timeout=30
settings-v1-duplicate.json: theme="dark", theme="light"
```

Executed the prepared runtime with bytecode generation disabled:

```text
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
test_duplicate_id ... ok
test_load ... ok
Ran 2 tests in 0.000s
OK
```

A separate inline standard-library probe used a `TemporaryDirectory` under the
workspace. It wrote a dummy selector and a replacement, flushed/fsynced the file,
called same-directory `os.replace`, opened/fsynced the directory and read back
`{"format":2}`. All calls succeeded and scratch was removed. It did not change
fixture data, implement migration, inject crashes or test power loss. This proves
local API availability only; migration acceptance tests remain proposed.

Initial `git status --short` returned no change entries but emitted sandbox-related
xcrun cache/global-ignore access warnings. No permissions were escalated and no
external resources were accessed.

After drafting, local document-link target checks and exact comparisons of both
history snapshots against their original text passed. `git diff --check` emitted
no whitespace findings (the same xcrun cache warnings remained). Final status showed
only documentation changes: DESIGN, PLAN, new SPEC/EVIDENCE and history snapshots.
