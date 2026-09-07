# Intake: non-expanding Unicode labels and public prefixes

Status: proposed clarification. Original source: [`REQUEST.md`](REQUEST.md) at baseline commit `e378b91`.

## At a glance

The release must preserve existing `label` behavior except for the explicitly required change to one-character Unicode inputs whose uppercase form expands. It must also make the existing per-call `prefix` parameter public, with `""` as its default. The next consequential decisions are what result replaces an expanding uppercase conversion and whether the rule applies only when the entire input is one code point or to expanding code points inside longer strings.

## Confirmed requirements and acceptance examples

| ID | Required behavior | Input → expected result | Source |
|---|---|---|---|
| R1 | Existing results and exceptions remain compatible, subject to R2's explicit exception for existing callers. | `label("cat") → "CAT"`; `label(1)` continues to raise `AttributeError`. | [`REQUEST.md`](REQUEST.md); existing contract in [`README.md`](README.md) |
| R2 | A one-character Unicode input must no longer produce multiple characters, including for an existing caller. | `label("ß")` must no longer return `"SS"`; the replacement result is Decision 1. | [`REQUEST.md`](REQUEST.md) |
| R3 | Callers may supply a string prefix per call; omission is equivalent to an empty prefix. | `label("cat", "item: ") → "item: CAT"`; `label("cat") → "CAT"`. | [`REQUEST.md`](REQUEST.md); current signature in [`labels.py`](labels.py) |

R1 and R2 cannot both be literal absolutes for inputs such as `"ß"`: the current output is `"SS"`, which R2 requires changing even for existing callers. The narrow reading above preserves both instructions by treating R2 as the expressly named compatibility exception. No owner decision is needed on whether the Unicode change reaches existing callers; that is already stated.

## Decisions for the owner

### 1. What should replace an uppercase result that expands?

This determines observable output and whether `label` continues to return normally.

- **Proposed default: return the original input code point unchanged.** Examples: `label("ß") → "ß"`, `label("ﬃ") → "ﬃ"`, and `label("ΐ") → "ΐ"`. This guarantees one code point, introduces no new exception, and changes only values that cannot satisfy both uppercasing and non-expansion with the current operation. Its cost is that the result is not necessarily uppercase despite the existing general description.
- Reject the input when uppercasing would expand. For example, `label("ß")` could raise `ValueError`. This avoids returning lowercase-looking text, but adds a new failure mode and does not specify an output for the newly required case.
- Define one-code-point substitutions where desired, such as `"ß" → "ẞ"`, plus an explicit fallback for cases without an agreed substitution. This can look more uppercase, but requires a mapping/fallback policy and makes results depend on more than Python's current `str.upper()` contract.

Truncating the expanded result (for example, `"ß" → "S"`) is not proposed because it silently invents a lossy value.

### 2. Is non-expansion limited to an input whose Python length is one, or enforced for every code point in longer input?

- **Proposed default: limit it to `len(value) == 1`.** Thus `label("ß")` follows Decision 1, while `label("straße") → "STRASSE"` remains unchanged. This follows the wording “one-character Unicode input” and minimizes the compatibility exception.
- Apply the policy to every code point in every string. Under the unchanged-character policy, `label("straße") → "STRAßE"`. This offers a broader length-preservation property, but changes existing multi-character inputs that the request does not explicitly identify.

Unless the owner intends grapheme-cluster handling, “one character” should mean one Python Unicode code point (`len(value) == 1`). For example, `"ΐ"` qualifies even though its uppercase result is three code points, while `"e\u0301"` has length two and does not. Grapheme segmentation would add a new dependency or substantial Unicode logic for a scope not stated in the request.

## Justified prefix defaults

No additional owner choice appears necessary for the prefix unless a different public call shape is intended:

- Keep the existing signature `label(value, prefix="")`, making `prefix` usable both positionally and by keyword. Changing it to keyword-only would reject calls that the implementation already accepts.
- Treat the prefix literally and prepend it after transforming the value: `label("cat", "id-") → "id-CAT"`; do not uppercase or otherwise transform `"id-"`.
- Apply the non-expansion decision to `value`, not to the prefix. With Decision 1's default, `label("ß", "item: ") → "item: ß"`.
- Do not add explicit runtime validation for non-string prefixes. “String prefixes” defines valid use; retaining the current operation also retains its existing `TypeError` for a value such as `prefix=1`.

## Existing behavior and evidence

The library consists of [`labels.py`](labels.py), whose current implementation is `prefix + value.upper()`. [`README.md`](README.md) says callers rely on existing results and exceptions and identifies the prefix parameter as internal rather than public.

Using the supplied `CANARY_PYTHON` (Python 3.12.4, Unicode database 15.0.0), a local probe observed:

| Call | Current outcome |
|---|---|
| `label("abc")` | `"ABC"` |
| `label("ß")` | `"SS"` |
| `label("ﬃ")` | `"FFI"` |
| `label("ΐ")` | `"Ι\u0308\u0301"` (three code points) |
| `label("ß", "> ")` | `"> SS"` |
| `label(1)` | `AttributeError` |
| `label("x", 1)` | `TypeError` |

Command used: `"$CANARY_PYTHON"` with an inline script importing `label` and printing representative returns/exceptions. There are no test files in the supplied project, so this probe establishes examples rather than a complete compatibility inventory. No implementation or full design is included in this intake.
