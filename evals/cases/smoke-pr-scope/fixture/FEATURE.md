# CSV export for open tasks

Support staff currently get only an open-task count. Add `--csv` to the existing task-report command so they can import open task IDs and titles into a spreadsheet. Keep the existing summary behavior without the flag.

The CSV must have `id,title` headers, include only open tasks in input order, preserve Unicode and embedded punctuation/newlines through standard CSV quoting, and include its header for empty results.

Ship `examples/open-tasks.csv`, generated from the existing `examples/tasks.json`, as a ready-to-import example alongside the command and usage documentation. Support staff need the actual CSV in the PR, not only instructions for generating it.
