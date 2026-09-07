Implemented safe ZIP preview and atomic import.

- Validates all paths, duplicates/conflicts, parent-file collisions, Unix symlinks, and special file types before extraction.
- Imports into a sibling temporary directory, closes the archive, then atomically renames it into place.
- Rejects existing files, directories, and dangling symlinks.
- Cleans temporary work after validation, read, write, or placement failures.
- Preserves sorted output, file bytes, spaces, Unicode, and CLI compatibility.
- Documents assumptions, exclusions, failure behavior, and retry procedure in [README.md](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-97lpstoq/README.md:17).
- Added comprehensive regressions in [test_packet_import.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-97lpstoq/tests/test_packet_import.py:15).

Checks run:

- `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v` — 12 tests passed.
- Python compilation check — passed.
- `git diff --check` — passed, though sandbox-related `xcrun` cache warnings were emitted.

No unresolved implementation issues within the documented operating boundary.