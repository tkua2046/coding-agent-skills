# Feature intake: non-expanding uppercase labels and public prefixes

Status: proposed clarification. Original requirement: [`REQUEST.md`](REQUEST.md) (baseline commit `b9a3c6f:REQUEST.md`). Existing contract and implementation: `b9a3c6f:README.md` and `b9a3c6f:labels.py`.

## At a glance

The requested prefix is already accepted by `label(value, prefix="")`, but is documented as internal. Publishing it with its present behavior is straightforward. The Unicode requirement conflicts with exact compatibility: today, for example, `label("ß") == "SS"`, so that result cannot both stay exactly the same and stop expanding. The owner needs to decide the narrow compatibility precedence and what a non-expanding uppercase result should be.

## Confirmed requirements

| ID | Requirement | Acceptance example |
|---|---|---|
| R1 | Preserve existing callers' outputs. | `label("abc") == "ABC"` remains true. |
| R2 | A one-character Unicode input must no longer be expanded into multiple characters, including for an existing caller. | The new result of `label("ß")` must have one character, unlike today's `"SS"`. |
| R3 | Make a per-call string prefix part of the public API; it is optional and defaults to the empty string. | `label("abc", prefix="id:") == "id:ABC"`; `label("abc") == "ABC"`. |

R1 and R2 are incompatible for the affected inputs under current behavior. Neither is silently treated as overriding the other below.

## Decisions the owner needs to make

### 1. Is R2 a narrow exception to exact output compatibility?

Current `label("ß")` returns the two-character string `"SS"`. Keeping that output satisfies R1 and violates R2; returning any one-character result satisfies R2 and changes an existing caller's output.

**Proposed reconciliation:** R2 overrides R1 only when the entire `value` is one Unicode code point and `value.upper()` contains multiple code points. Preserve all other existing results and exceptions. This reads “including existing callers” as an intentional, narrowly scoped compatibility break, but it remains a proposal until confirmed.

Owner answer needed: accept that exception, or state which requirement takes precedence instead.

### 2. What one-character result replaces an expanding uppercase mapping?

There is no result implied by “stop expanding.” Representative current mappings include:

| Input | Current result | Option A: preserve input | Option B: replacement mapping |
|---|---|---|---|
| `"ß"` | `"SS"` | `"ß"` | for example, `"ẞ"` |
| `"ﬃ"` | `"FFI"` | `"ﬃ"` | would need a specified replacement or fallback |
| `"ǰ"` | `"J̌"` | `"ǰ"` | would need a specified replacement or fallback |

**Proposed default:** if uppercasing a one-code-point value produces more than one code point, return the original value unchanged. It is lossless, uniform across scripts, and avoids inventing or maintaining a partial mapping. The consequence is that some such labels are not uppercase. A replacement-mapping policy is also viable, but the owner must define its source and fallback; `"ß" → "ẞ"` alone does not address ligatures and decomposing mappings.

Owner answer needed: preserve the original character, or specify the replacement and fallback policy.

### 3. Does “one-character” mean one Python/Unicode code point?

**Proposed default:** apply R2 only when `len(value) == 1`. Thus `label("ß")` is protected, while a multi-code-point value retains current behavior—for example, `label("straße") == "STRASSE"`. A user-perceived grapheme can contain several code points (for example, `"é"`), and treating graphemes as the unit would broaden the change and require a segmentation policy not present in the request or library.

Owner answer needed only if “character” is intended to mean a grapheme rather than a code point.

## Justified defaults that do not need reopening unless unwanted

- Preserve prefix text verbatim and apply uppercasing only to `value`: under the proposed answers above, `label("ß", "id:") == "id:ß"`. The prefix is not included when deciding whether the value expanded.
- Keep both existing positional and keyword prefix calls valid. The current signature already permits `label("a", "id:")` and `label("a", prefix="id:")`; restricting either form would create an unnecessary compatibility break.
- Add no new type coercion or validation. Existing non-string failures should remain the same, including `label(None)` raising `AttributeError`, and non-string prefixes failing through concatenation. “String prefix” describes the supported input rather than requiring a new validation layer.
- Preserve current behavior for empty strings, ordinary one-code-point mappings, and all multi-code-point values. Examples: `label("") == ""`, `label("é") == "É"`, and `label("abc") == "ABC"`.

## Baseline evidence

Inspected the repository's only implementation and public note (`labels.py`, `README.md`) at baseline commit `b9a3c6f`. There are no repository tests.

Using the supplied `CANARY_PYTHON` (Python 3.12.4, Unicode database 15.0.0):

- `label("ß")` returned `"SS"`; `label("ﬃ")` returned `"FFI"`; `label("և")` returned `"ԵՒ"`; and `label("ǰ")` returned `"J̌"`.
- An exhaustive scan of Unicode code points found 102 values for which Python's `str.upper()` returns more than one code point. This count is runtime-data evidence, not a promised stable inventory across Python/Unicode versions.
- `label("abc", prefix="pre:")` returned `"pre:ABC"`.
- Existing exception types were observed for representative unsupported inputs: `label(None)` raised `AttributeError`; `label(b"a")`, `label("a", None)`, and `label("a", 1)` raised `TypeError`.

No implementation or full design is included in this intake.
