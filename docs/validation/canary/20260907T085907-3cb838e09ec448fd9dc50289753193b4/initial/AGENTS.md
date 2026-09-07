# Working here

This is a local Python standard-library utility. Keep the current CLI and CSV/JSON
contract. Tests live in qa/ and use unittest with the pattern in quality.ini.
Use tools/check.py for normal checks; hooks/pre-commit delegates to that command.
Keep usage in README and contributor operations in DEVNOTES. Preserve useful
content when moving it; detailed development records belong under docs/.
Use the prepared runtime, without adding dependencies or changing global settings.
This task authorizes local workflow and documentation edits only: no commits,
tags, pushes, releases, external services or additional approval rounds.
