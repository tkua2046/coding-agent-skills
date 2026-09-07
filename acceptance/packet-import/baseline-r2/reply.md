Implemented safe ZIP preview and atomic import.

- Shared validation rejects unsafe paths, duplicates/conflicts, parent-file conflicts, symlinks, and special Unix files with `ValueError`.
- Import copies validated bytes into a sibling staging directory, then atomically renames it into place.
- Failures clean staging and leave the destination retryable; dangling symlinks count as existing.
- CLI failures produce concise errors without tracebacks or success listings.
- Operating boundaries and retry behavior are documented in [README.md](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-r2tcm5qr/README.md:16).
- Regression coverage is in [test_packet_import.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-r2tcm5qr/tests/test_packet_import.py:1).

Checks run with `CANARY_PYTHON`:

- Existing baseline: 3 tests passed.
- Final unittest gate: 12 tests passed.
- Python compilation check passed.
- `git diff --check` passed.
- Confirmed no `extract()`/`extractall()` calls remain.

No known functional issues. Independent/human review was not available in this run; no commit was created, as requested.