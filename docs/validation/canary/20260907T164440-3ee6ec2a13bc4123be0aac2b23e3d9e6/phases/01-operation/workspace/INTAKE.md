# Intake: Unicode labels and public prefixes

Status: clarification pending; no design or implementation proposed. This note supplements the unchanged [REQUEST.md](REQUEST.md:1).

## Supplied decisions and current behavior

[REQUEST.md](REQUEST.md:1) requires exact outputs for all old callers, no multi-character expansion of any one-character Unicode input (including existing callers), and optional per-call string prefixes with an empty default. These are supplied requirements, not questions to ask again. [README.md](README.md:1) also identifies existing results and exceptions as compatibility expectations and says the prefix parameter is internal.

The entire implementation is [labels.py](labels.py:1): `label(value, prefix="")` returns `prefix + value.upper()`. Prefixes already work positionally and by keyword, retain their original case, and are added after uppercasing the value. The requested public prefix capability therefore has an existing behavioral baseline.

## Decisions requiring the owner

1. **Which guarantee may be relaxed where the requirements conflict?** Observed `label("ß") == "SS"` and `label("ﬃ") == "FFI"` prove that exact legacy output and no expansion for existing callers cannot both hold. May these legacy outputs change, or must the no-expansion requirement be revised? An opt-in mode alone would not satisfy the explicit requirement to cover existing callers. There is no justified default for this precedence decision.

2. **If expansion is prohibited, what result should replace it?** For `"ß"`, retaining `"ß"` and choosing `"ẞ"` are different policies; for the ligature `"ﬃ"`, a general fallback is still needed. Should expanding characters remain unchanged, use agreed single-character uppercase mappings with a fallback, or raise an error? For example, retaining `"ﬃ"` returns a label, whereas rejection introduces an exception for a previously successful call. Neither Python's observed expansion nor the supplied text chooses this policy; truncating `"FFI"` to `"F"` is not an established requirement. Decide this only after resolving compatibility precedence.

3. **How far does the Unicode rule extend?** Does it apply only when the complete value is one character, or to each character within longer values? Today `label("aß") == "ASS"`; a policy that retains expanding characters throughout strings would produce `"Aß"`, while a single-input-only rule could leave `"ASS"`. This materially changes the set of legacy results affected. Also confirm whether “character” means a Unicode code point or a user-perceived character: `"é"` has one code point, while `"e\u0301"` has two but can display as one character. Proposed interpretation: code points, matching Python string length, unless the owner intends grapheme-based behavior.

## Proposed defaults, separate from supplied requirements

- Apply the expansion constraint to the transformed value, excluding the prefix. For example, `label("a", prefix="id:")` should remain `"id:A"` even though the complete result has multiple characters. Otherwise the prefix requirement would introduce another conflict.
- Expose the existing `prefix=""` behavior: preserve literal prefix text, support existing positional and keyword forms, and keep it per call. Example: `label("abc", "id:") == "id:ABC"`. No additional prefix formatting or uppercasing is indicated.
- Preserve existing exceptions and input handling outside an explicitly approved Unicode change. Avoid adding coercion or validation by default: currently `None` raises `AttributeError` and bytes raise `TypeError`. Ordinary non-expanding mappings such as `"ı" → "I"` and `"é" → "É"` should remain intact; no normalization is requested.

## Baseline and evidence

No tests, callers, package configuration, or documented check commands were found in the fixture. A bounded probe of the unchanged library completed with exit status **0** using:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$CANARY_PYTHON" intake-evidence/probe.py > intake-evidence/baseline.txt 2>&1
```

[Probe source](intake-evidence/probe.py) and [raw stdout/stderr](intake-evidence/baseline.txt) record the runtime, representative Unicode results, prefix behavior, and exceptions. Exceptions in that record were intentionally caught observations, not failed tests. This establishes the compatibility conflict and current examples; it is not a passing test suite or an exhaustive Unicode audit. The owner's intended precedence, replacement rule, and scope remain unresolved.
