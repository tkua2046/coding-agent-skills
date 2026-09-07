# Local workflow verification — 7 September 2026

Outcome: the normal check and existing installed hook pass all five application
tests with coverage. Failure and empty-discovery probes fail as required, both
with coverage and in the stdlib fallback. No application changes were made.

The baseline command using CANARY_PYTHON passed five tests before the workflow
edit. The updated normal command passed five tests, printed missing lines, and
wrote the configured artifacts/.coverage and artifacts/coverage.json. JSON was
checked for branch measurement and inventory.py as its only source. Reported
coverage was 96%; missing line 81 and partial branches remain. No percentage
threshold was introduced.

The local repository root was verified. Its local config has no custom hooks
path. The already installed executable .git/hooks/pre-commit matches the maintained
wrapper byte for byte; it was retained and directly exercised without a commit.
The documentation probe temporarily appended a README comment and invoked the
installed hook with README.md as an argument. This tests unconditional execution;
no commit or staged-index operation was performed.

Fallback probes used the prepared interpreter with -S to hide site packages,
without installing or removing anything. Temporary failing tests, discovery
configuration, README edits, wrapper and probe bytecode were removed/restored in
finally cleanup. Application, sample data, existing application tests, discovery
configuration, coverage settings and both hook copies were verified unchanged.
Reports from the successful normal run were restored byte for byte after probes;
there were no pre-existing artifact reports at initial inspection. The original
historical session record is preserved in [development history](../DEVELOPMENT_HISTORY.md).

Limitations: without coverage the stdlib gate emits a notice and produces no new
coverage reports. No external integration, package installation, feature work or
Git delivery action ran. Git emitted sandbox warnings about its temporary xcrun
cache and user ignore file; local repository inspection still succeeded.

## Probe output

### Installed hook with documentation edit and filename

Exit status: 0

```text
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.011s

OK
Name           Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------
inventory.py      58      1     18      2    96%   59->exit, 81
----------------------------------------------------------
TOTAL             58      1     18      2    96%
```

### Installed hook rejects failing test

Exit status: 1

```text
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok
test_failure (check_workflow_temporary.GateProbe.test_failure) ... FAIL

======================================================================
FAIL: test_failure (check_workflow_temporary.GateProbe.test_failure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-b26de6uv/worker/qa/check_workflow_temporary.py", line 4, in test_failure
    self.fail("temporary gate failure")
AssertionError: temporary gate failure

----------------------------------------------------------------------
Ran 6 tests in 0.010s

FAILED (failures=1)
Name           Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------
inventory.py      58      1     18      2    96%   59->exit, 81
----------------------------------------------------------
TOTAL             58      1     18      2    96%
```

### Installed hook rejects empty discovery

Exit status: 1

```text
Checks failed: no tests discovered
```

### Stdlib fallback hook passes from another directory

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

### Stdlib fallback hook rejects failing test

Exit status: 1

```text
Coverage unavailable: running stdlib unittest gate without coverage reports.
test_cli_success_and_failure_preserve_export (check_inventory.InventoryTests.test_cli_success_and_failure_preserve_export) ... ok
test_header_and_empty_inventory (check_inventory.InventoryTests.test_header_and_empty_inventory) ... ok
test_invalid_rows (check_inventory.InventoryTests.test_invalid_rows) ... ok
test_normalized_rows_and_order (check_inventory.InventoryTests.test_normalized_rows_and_order) ... ok
test_replace_failure_cleans_temporary_and_preserves_destination (check_inventory.InventoryTests.test_replace_failure_cleans_temporary_and_preserves_destination) ... ok
test_failure (check_workflow_temporary.GateProbe.test_failure) ... FAIL

======================================================================
FAIL: test_failure (check_workflow_temporary.GateProbe.test_failure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/canary-b26de6uv/worker/qa/check_workflow_temporary.py", line 4, in test_failure
    self.fail("temporary gate failure")
AssertionError: temporary gate failure

----------------------------------------------------------------------
Ran 6 tests in 0.005s

FAILED (failures=1)
```

### Stdlib fallback hook rejects empty discovery

Exit status: 1

```text
Coverage unavailable: running stdlib unittest gate without coverage reports.
Checks failed: no tests discovered
```
