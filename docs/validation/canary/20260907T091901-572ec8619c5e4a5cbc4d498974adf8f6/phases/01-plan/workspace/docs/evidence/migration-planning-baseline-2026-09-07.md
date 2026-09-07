# Migration planning baseline — 2026-09-07

Fresh fixture inspection; no implementation or design/plan review performed.

Command: `$CANARY_PYTHON -B -m unittest discover -s tests -v`

Runtime: 3.12.4
Exit status: 0

```text
test_duplicate_id (test_settings.SettingsTests.test_duplicate_id) ... ok
test_load (test_settings.SettingsTests.test_load) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

## Inspected source fingerprints (SHA-256)

- `AGENTS.md`: `34ec1a63df56f4eccf184db32eab791c8cf34c7c89a949eb59cb64ef257b1344`
- `docs/ORIGINAL.md`: `473d6378896b5cfaaf2ee3af5c4384e9e5180d87b1509fe858f2de57536eca6b`
- `settings.py`: `e944c9d67c106e539cffb7c9786c544a313e3bbff56cd81340b599f072a62be7`
- `tests/test_settings.py`: `b39a8b82abea78907c78c366b6d6756d702fafa6a06c1d698ee34a7bb9455f01`
- `data/active.json`: `ba10dad8fd3fa186f11e15f0f887e8ebcdc99dec6a0d73c07b0aebb1dcdbce16`
- `data/settings-v1.json`: `c08c91c016051713d882e6d5abbc67960d01cba94889eebae4abf46d0affc2e1`
- `data/settings-v1-duplicate.json`: `773a6797ad0fd6dcfc0a04154993e5f9b513a0ade4d780cb4ebe9e6a833c9341`

Only existing v1 behavior was tested; migration and crash acceptance remain proposed.
