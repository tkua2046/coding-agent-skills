Implemented the scoped R1/R2 fix.

- `import_packet()` now converts malformed DEFLATE `zlib.error` into contract-compatible `BadZipFile` before final placement, preserving cleanup and retry behavior: [packet_import.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-packet-fix-x5j0kvpy/packet_import.py:59)
- Added real corrupted-DEFLATE API and CLI regressions covering error type/reporting, no traceback or success output, cleanup, destination absence, and corrected-archive retry: [test_packet_import.py](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-packet-fix-x5j0kvpy/tests/test_packet_import.py:34)

Checks completed:

- Focused regressions: 2 passed.
- Full existing gate using Python 3.12.4: 14 passed.
- `git diff --check`: passed.
- Confirmed `REQUEST.md` and `reviews/R1.md` unchanged.
- Only `packet_import.py` and `tests/test_packet_import.py` are modified.

No known implementation issues remain. Independent recheck/acceptance of the original review is still pending. No commit was created.