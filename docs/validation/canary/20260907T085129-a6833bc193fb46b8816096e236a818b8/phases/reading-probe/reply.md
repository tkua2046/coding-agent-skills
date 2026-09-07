1. The proposed change adds v2 settings reading and explicit migration to `{"version":2,"settings":{...}}`, with no automatic migration on reads. It preserves every stable ID and JSON value, `load(path)` compatibility and its mapping return value, valid v1 behavior, and the original v1 file.

2. The main decision is to copy, validate, then atomically replace `active.json`. Interruption leaves a usable v1 source, and the selector references a complete validated file. Retaining source and staging files costs disk space.

3. The next implementation outcome is S1: a compatible v1/v2 reader and validated v1 conversion without file activation, with tests and README usage. It depends on S0 resolving open design decisions, documenting filesystem guarantees, and obtaining design and plan reviews; both reviews remain pending. One decisive acceptance example is that the duplicate-ID fixture still raises `ValueError`. Implementation has not started.

These answers reflect only the exposed excerpts; this machine comprehension probe does not establish human usability.