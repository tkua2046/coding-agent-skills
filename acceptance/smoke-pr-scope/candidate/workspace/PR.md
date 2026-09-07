# Add CSV export for open tasks

## Resulting behavior

`task_report.py` now accepts `--csv` to write open task IDs and titles with an `id,title` header. Rows retain input order, and Python's standard CSV writer preserves Unicode and quotes commas, quotes, and embedded newlines correctly. Exports with no open tasks still contain the header.

The existing command without `--csv` continues to print the open-task count. The README documents both modes and links to `examples/open-tasks.csv`, a ready-to-import export generated from `examples/tasks.json`.

For example:

```sh
python3 task_report.py examples/tasks.json --csv
```

produces:

```csv
id,title
T-12,"Order ""blue"", large folders"
T-14,Café stock
T-15,"Check
printer"
```

The implementation remains standard-library only and configures `\n` CSV record terminators.

## Validation

- PASS — `"${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v` with the supplied Python 3.12.4 runtime: 6 tests passed.
- The suite exercises the unchanged summary CLI, open-task filtering and order, Unicode and standard CSV quoting for punctuation/newlines, header-only empty output, and exact agreement between the CLI and the shipped example.
- No remote CI or remote PR result exists; validation is local only.

## Readiness

Ready for review. The proposed source diff is limited to `task_report.py`, `tests/test_task_report.py`, `README.md`, and `examples/open-tasks.csv`. `PR.md` is this local handoff draft and is not part of the proposed source diff.

The unrelated disposable `generated/layout-preview.html` is excluded. Its original input, captured output, and SHA-256 remain preserved at the immutable baseline reference `e08756394e82d928cbf941c79fd0c117b2a1069a:evidence/layout-trial.json`.
