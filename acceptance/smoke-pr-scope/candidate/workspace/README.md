# Task report

Print the number of open tasks from a JSON task list:

```sh
python3 task_report.py examples/tasks.json
```

Export open task IDs and titles as CSV for a spreadsheet:

```sh
python3 task_report.py examples/tasks.json --csv
```

The export preserves input order and standard CSV cell quoting, including Unicode and newlines in titles. An empty result still has the `id,title` header. [Open the generated example](examples/open-tasks.csv), built from [the sample tasks](examples/tasks.json), to try an import directly.
