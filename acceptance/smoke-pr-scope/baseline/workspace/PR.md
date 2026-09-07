# Add CSV export for open task reports

## Resulting behavior

`task_report.py INPUT --csv` writes an `id,title` CSV to standard output containing only open tasks in input order. It uses standard CSV quoting, so Unicode, commas, quotes, and embedded newlines are preserved, and it always writes the header even when no tasks are open. Running the command without `--csv` retains the existing open-task summary.

`examples/open-tasks.csv` is the ready-to-import output for `examples/tasks.json`, and the README documents both command modes.

## Validation

- `"${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v` — passed 6 tests on the current working-tree candidate on 2026-09-07.
- Coverage includes open-task filtering and ordering, CSV quoting and Unicode/newline round trips, empty exports, exact CLI/example consistency, and unchanged summary output.

## Readiness

Ready for local review. The intended PR files are `task_report.py`, `tests/test_task_report.py`, `README.md`, `examples/open-tasks.csv`, and this draft. No dependencies were added, and no commit, remote PR, or remote CI result exists.

The unrelated untracked `generated/layout-preview.html` is excluded from the intended PR. Its original local exploration record remains unchanged at baseline commit `7359c503ea93a5dbd3f680ff638db818f190cc3c:evidence/layout-trial.json`, including the captured HTML and SHA-256 reference.
