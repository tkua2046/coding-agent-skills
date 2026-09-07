1. The proposed change lets a caller explicitly migrate v1 settings to v2 and reload validated v2 through `active.json`. Stable IDs and values must be preserved, and the original v1 file must remain byte-for-byte unchanged, including after success.

2. Create a separate v2 file, validate its persisted contents against v1, then atomically replace the selector to activate it. The extra copy preserves recovery without an undo log.

3. The next outcome is explicit migration, validated v2 reload through the selector, and safe retry after interruption. It depends on design and plan reviews, resolution of proposed crash/completion semantics, and later authorization; migration also depends on both reader paths. A decisive acceptance example is interruption after target publication: v1 remains active, retry succeeds, IDs and values are preserved, and v1 bytes remain unchanged.

4. Interrupt after publishing v2 but before activation, verify that the selector still selects v1, then retry successfully and check stable IDs, values, and unchanged v1 bytes. The excerpts do not supply the full crash/completion semantics; those remain pending review.

These answers reflect the exposed text only. This first-screen machine comprehension probe does not establish human usability.