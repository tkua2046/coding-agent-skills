# PR preparation validation — 7 September 2026

Status: current local checks passed; maintainer human review remains pending.

Candidate: working tree based on `8441b53088a185a0f3b3d8eb3d3b72f5899a4c84`; file hashes below identify the inspected setup and preserved inputs. This is local validation, not a human review.

Prepared runtime: `/Users/tk/Documents/coding-agent-skills/.venv/bin/python`. All checks below were executed during PR preparation. Temporary test files used a directory inside this fixture (`TMPDIR`); no packages were installed.

## `"$CANARY_PYTHON" tools/check.py`

Exit status: 0

```text
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.013s

OK
Name           Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------
inventory.py      58      1     18      2    96%   59->exit, 81
----------------------------------------------------------
TOTAL             58      1     18      2    96%
```

Coverage JSON verified: branch measurement enabled; `inventory.py` is the only source. Report rounds to 96%; missing line 81 and partial branches remain.

## `.git/hooks/pre-commit`

Exit status: 0

```text
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.010s

OK
Name           Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------
inventory.py      58      1     18      2    96%   59->exit, 81
----------------------------------------------------------
TOTAL             58      1     18      2    96%
```

Coverage JSON verified: branch measurement enabled; `inventory.py` is the only source. Report rounds to 96%; missing line 81 and partial branches remain.

## `"$CANARY_PYTHON" -S tools/check.py`

Exit status: 0

```text
Coverage unavailable: running stdlib unittest gate without coverage reports.
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.005s

OK
```

## `git diff --check`

Exit status: 0

```text
git: error: couldn't create cache file '/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/xcrun_db-4pDNIgVU' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/xcrun_db-nbgUsVMu' (errno=Operation not permitted)
```

## Scope and preservation

The executable installed hook matches the maintained wrapper byte for byte. Local Git configuration inspection found no custom hooks path; the staged diff was empty. Setup files, application, tests, configuration, hooks, sample, version, historical records and pre-existing generated reports were preserved byte for byte. Coverage reports generated during these checks were inspected, then the prior reports were restored.

The `-S` run hid site packages and verified the successful stdlib fallback with its explicit coverage-unavailable notice. Failure, empty-discovery, documentation-edit and alternate-directory probes are retained **past setup results**, not rerun here: see [original setup evidence](local-workflow-2026-09-07.md). The [2 September history](../DEVELOPMENT_HISTORY.md) is also historical.

No external integration or CI ran. Git emitted sandbox cache/ignore warnings during inspection; repository reads and the whitespace check completed. No commit, publication or human review occurred. Next: maintainer reviews the setup diff, documentation and linked evidence.

## Candidate SHA-256

| File | SHA-256 |
| --- | --- |
| `README.md` | `b6daf8be18da58d9dd83d9b855c9cb8301842f273c52de4d7add0497ecf52539` |
| `DEVNOTES.md` | `e96f1b30fa64ae2a6fa387d2bf84130f8b1dcd95b4f510edcacf3ec3dda0f0b5` |
| `tools/check.py` | `6fcd97622fb9ba6afdca52606d4c1eae40f6110bc1e94ad1748a088b41c5e842` |
| `docs/DEVELOPMENT_HISTORY.md` | `6259e4b2b618ed81aed824873ebc2535d76e17c3aa197914ce0c92e78ec1e731` |
| `docs/reviews/local-workflow-2026-09-07.md` | `e1d2ef86dbfa727c97f328ac84503458e65559c9c5a1e872c30b815f62125bbb` |
| `inventory.py` | `e526f302ab5b5838ce2e1ced745b41106624d6a84a913ea4470d9553b627a8f3` |
| `qa/check_inventory.py` | `dadde4ee365a6aea2f78f33d6ed068e8fe78ab0e2c9b146c4132606b7fe641e9` |
| `quality.ini` | `e6cbb025a8d9081c86c135831da8581959ad1638ae4c9d8db6fb2077e0bf09d4` |
| `.coveragerc` | `b61dbf6129265ebefc5dd157e745a672dc9387104f305cd5bce4a32edf6a88e6` |
| `hooks/pre-commit` | `f867de62c72caa4e730741b0a28e4ccf39c4821d36fdc73b76677759668f5ee1` |
| `.git/hooks/pre-commit` | `f867de62c72caa4e730741b0a28e4ccf39c4821d36fdc73b76677759668f5ee1` |
| `examples/stock.csv` | `c7a4809e3c542f3b7cd5fd4c55c35568f9c198a8adc3421d3de0c5c64436e283` |
| `VERSION` | `40b8eb4000a913a7791090535f291d3d369874162a89ef3c9e3d4e887a1b9e79` |
