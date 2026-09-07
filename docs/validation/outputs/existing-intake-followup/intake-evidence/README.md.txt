# Intake evidence

All execution took place in this fixture. No network or delegation was used. The shared `.venv` interpreter was used with bytecode writing disabled; pytest's cache provider was disabled to avoid cache writes. No dependencies were installed.

## Baseline

README command: `.venv/bin/python -m pytest`.

Executed command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider`.

Exit status: **1**. Complete supplied suite: **1 passed, 1 failed**. The failure is `tests/test_formatter.py::test_known_legacy_issue`: actual `"SS"`, expected `"ß"`. This is a pre-existing failure, observed with application code and tests untouched.

- [Raw stdout](baseline.stdout.txt)
- [Raw stderr](baseline.stderr.txt) — empty
- [Execution metadata](execution.json) — working directory, revision, exact argument arrays, environment override, exit statuses, and output locations

## Diagnostic probe

Executed with `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -c '<probe source>'` from the fixture root. The exact `-c` argument is recorded in execution metadata and reproduced in [probe.py](probe.py). The probe only invokes the existing formatter on five literal strings; it does not add or modify tests.

Exit status: **0**.

- [Raw stdout](probe.stdout.txt)
- [Raw stderr](probe.stderr.txt) — empty

## Source preservation

The initial read-only status showed an existing modification to `skills/feature-design/prompts/intake-feature.md`. It was used as supplied and left unchanged. No prior trial artifacts or unrelated repository sources were inspected.

- [Tracked source hashes and symlink target before execution](source-integrity-before.json)
- [Status before baseline](git-status-before-baseline.txt) — captured after creating this evidence directory, so it includes that directory as untracked
- [Final preservation check](preservation.txt)
- [Final status](git-status-after.txt)

The source hashes establish preservation during this intake; they do not claim that the supplied working tree was identical to its Git revision.
