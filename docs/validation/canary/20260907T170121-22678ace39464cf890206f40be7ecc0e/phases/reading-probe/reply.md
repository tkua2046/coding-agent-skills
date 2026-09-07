1. **Change and preservation:** The proposal adds v2 and selector-aware reading, strict migration validation, and recoverable migration from v1 to v2. Preserve the original v1 bytes and values, including their types; legacy parsing alone cannot establish lossless conversion.

2. **Main decision and tradeoff:** Keep v1 untouched, create and validate a separate v2 file, then atomically replace the active selector. Retry follows the selector, never partial output. This requires temporary space and retains unselected files.

3. **Next implementation outcome:** S1 adds safe reading of both formats, selector-aware reading, and strict migration-input validation, without migration writes. It depends on document reviews and later implementation authorization. One decisive acceptance example: relative selection works regardless of the working directory and rejects a format mismatch.

4. **Interrupted migration acceptance:** Check that interruption before activation leaves v1 unchanged and the selector pointing to v1, and that retry follows that selector rather than partial output. The excerpts do not supply the full acceptance contract or the exact handling of an existing partial destination.

These answers reflect only the exposed excerpts; this machine comprehension probe is not human usability proof.