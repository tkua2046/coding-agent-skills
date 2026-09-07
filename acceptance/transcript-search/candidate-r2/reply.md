Implemented literal phrase search with neighboring cue context.

- Added `find_cues()` with Unicode `casefold()` matching, strict validation, overlapping-window deduplication, source ordering, and input immutability.
- Added `--find PHRASE` and `--context N` CLI options with clean errors and unchanged timestamp rendering.
- Added regression coverage for library and CLI behavior.
- Expanded [README.md](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-ds9vyzv2/README.md) with editor examples and search rules.

Validation: `CANARY_PYTHON -m unittest discover -s tests -v` — all 16 tests passed. Direct CLI success, no-match, and error cases also passed.

Remaining limitation: intentionally, search is literal within each individual cue—there is no fuzzy/regex search, and phrases cannot cross cue boundaries. No commits or publishing were performed.