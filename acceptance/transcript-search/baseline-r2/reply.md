Implemented literal phrase search with neighboring cue context.

- Added `find_cues()` with Unicode `casefold`, literal matching, validation, ordered deduplication, and input preservation in [transcript.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-r_ayljnd/transcript.py:43).
- Added `--find PHRASE` and `--context N` with clean CLI errors.
- Added API and CLI regressions in [test_transcript.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-r_ayljnd/tests/test_transcript.py:31).
- Added editor usage guidance in [README.md](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-transfer-r_ayljnd/README.md:6).

Verification:

- `"$CANARY_PYTHON" -m unittest discover -s tests -v` — 11 tests passed.
- `git diff --check` — passed.
- No commit or publication performed.

The intentional limitation is that searches remain cue-local and do not match phrases split between cues. Independent external review remains pending; implementation review and automated checks were performed locally.