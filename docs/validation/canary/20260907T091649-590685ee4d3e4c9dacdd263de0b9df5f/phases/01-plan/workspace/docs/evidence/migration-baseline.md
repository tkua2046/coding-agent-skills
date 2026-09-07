# Local migration evidence — 2026-09-07

Scope: fresh-context inspection and bounded filesystem experiment, using only the
fixture and supplied skills. This is evidence, not a design or plan review.

Read AGENTS.md, ORIGINAL.md, existing DESIGN.md/PLAN.md, README.md, DEVNOTES.md,
settings.py, both tests and all three supplied data files. Original requirements
and the historical design/plan statements are preserved. No prior review reports
were present in the fixture file inventory.

## Verified baseline

Command: `"$CANARY_PYTHON" -m unittest discover -s tests -v`

```text
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok
Ran 2 tests in 0.000s
OK
```

The reader rejects non-v1 versions and duplicate IDs, then constructs a Python
dictionary. It does not inspect the marker or write files. Python dictionary keys
can include non-string IDs; plain JSON parsing can discard duplicate object names.
Neither behavior establishes a safe v2 migration contract. Supplied data uses
unique string IDs except the deliberate duplicate-ID negative fixture.

## Bounded question: are the proposed local filesystem primitives available?

Using the prepared Python runtime and standard library, created a temporary
directory under `docs/evidence/`, wrote a v1 marker and a temporary v2 marker,
flushed and `os.fsync`ed the temporary file, closed it, used `os.replace` over the
marker, then opened the directory read-only and `os.fsync`ed that descriptor.
Read back the marker, closed handles and removed the temporary directory.

```text
Local probe: file fsync, same-directory replace, directory fsync succeeded; active = {"format": 2}
```

This verifies callable primitives on the local fixture filesystem only. It does
not test a migration, termination during an operation, atomic observation by a
reader, power failure, or other operating systems/filesystems. No production
reader, test or fixture data was modified by the probe. Migration failure and
recovery tests remain proposed work.

`git status --short` emitted sandbox warnings about system cache/global-ignore
access; no permissions were expanded. No commits, installs or external actions
were performed.
