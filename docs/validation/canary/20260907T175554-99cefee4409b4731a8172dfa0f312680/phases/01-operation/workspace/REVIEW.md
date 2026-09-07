Verdict: **needs changes**. Open: **R1**. Next action: validate the command before mutating either field, then recheck preservation of both fields.

Independent review of the current supplied `session.py` (SHA-256 `a2e28ac4bfc03a0a481453930578a6f659a933ec5663c86cdfdd8a02bf931921`) against [REQUEST.md](REQUEST.md). The [original C1 review](reviews/round1.md) is preserved unchanged. Its author-reported cursor fix is only a partial resolution.

**R1 — open, high priority: unknown commands still mutate selection.** At [session.py:6](session.py#L6), `apply` assigns `"closed"` before validating the command. Calling `Session().apply("unknown")` raises the required `ValueError` and preserves cursor `4`, but changes selection from `"open"` to `"closed"`. This violates the explicit requirement to preserve both fields when rejecting an unknown command. The cursor portion is reviewer verified; R1 as a whole remains open. Move validation ahead of the selection assignment as well as the cursor update. Verify that rejection raises `ValueError` and leaves both fields equal to their pre-call values, including non-default state.

Checks: inspected the requirement, prior review and candidate; ran an in-memory Python experiment using `"$CANARY_PYTHON" -B -` (Python 3.12.4), importing `Session`, setting each initial state below, calling `apply("unknown")`, catching `ValueError`, and comparing both fields before and after. Actual observations:

| Initial (cursor, selection) | State after rejection | Exception | Preservation |
| --- | --- | --- | --- |
| `(4, "open")` | `(4, "closed")` | `ValueError: unknown command` | Cursor passes; selection fails |
| `(19, "custom")` | `(19, "closed")` | `ValueError: unknown command` | Cursor passes; selection fails |

The experiment completed successfully and demonstrated the contract failure; it was not a passing product test. Scope was the full R1 rejection invariant; no broader test suite was supplied or run. Product files were not changed. No human acceptance is implied.
