1. The proposal adds validated v2 settings reading and migration, publishing v2 through atomic replacement of `active.json`. It preserves original v1 bytes, stable IDs and values, and current direct v1 loading behavior. Implementation remains deferred.

2. The main decision is to preserve the source and activate validated v2 settings through an atomic selector replacement. This requires a second data file but makes interruption recoverable without undoing source writes.

3. The next implementation outcome is S1: compatible v2 reading, selector loading, and strict validation. It depends on reviewed design and plan, then a later implementation task; both reviews remain pending. One decisive acceptance example is that selector resolution works from another working directory.

4. The excerpts establish original-byte preservation and require interruption/retry recovery coverage. They do **not** supply the specific acceptance scenario or expected result for interruption before activation followed by retry; the relevant acceptance text is not exposed.

These answers reflect first-screen machine comprehension, not human usability proof.