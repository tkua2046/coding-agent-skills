1. The proposed change adds v2 and selector reading, then recoverable migration using validated output and an atomic `active.json` replacement. No selector reader or migration is implemented yet. Preserve direct v1 compatibility, duplicate-ID rejection, the original v1 file indefinitely, and recovery through complete old/new selection and safe retry.

2. The main decision is to publish and validate a complete v2 file before atomically switching the selector, while retaining v1 indefinitely. This preserves recovery at the cost of a second file. A dual-version reader must be deployed before activation.

3. The next implementation outcome is **S1: compatible readers and validation**, including tests and README usage. It depends on reviewed contract choices and later implementation authorization; design and plan reviews remain pending. One stated acceptance example is direct v1/v2 equivalence. The exposed text names that check but does not supply its detailed inputs or expected outputs.

These answers reflect only the exposed excerpts; this machine comprehension probe does not establish human usability.