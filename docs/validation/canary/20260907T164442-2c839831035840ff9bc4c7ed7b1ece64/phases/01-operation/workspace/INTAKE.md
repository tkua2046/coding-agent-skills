# Feature intake

The owner must resolve a compatibility conflict before design: `label("ß")` currently returns `"SS"`. Keeping that exact result and stopping one-character Unicode expansion for existing callers cannot both hold. No implementation or full design is proposed here.

Confirmed requirements remain in [REQUEST.md](REQUEST.md): preserve all old outputs; stop expansion of any one-character Unicode input, including for existing callers; add optional per-call string prefixes with an empty default. [README.md](README.md) also identifies existing results and exceptions as compatibility obligations and says the current prefix parameter is internal. These supplied decisions need no reconfirmation.

## Current behavior and evidence

[labels.py](labels.py) contains the sole entry point, `label(value, prefix="")`, which returns `prefix + value.upper()`. Prefixes already work internally and are prepended verbatim: `label("abc", "pre:") == "pre:ABC"`. Unicode uppercase can expand: `"ß" → "SS"`, `"ﬃ" → "FFI"`, and `"ΐ" → "Ϊ́"` (three code points). Expansion also occurs within longer strings: `"straße" → "STRASSE"`. Invalid inputs currently raise ordinary Python exceptions.

No tests, callers, package configuration, or documented check commands were found in the fixture. A local probe using `CANARY_PYTHON` exited 0; command, runtime, cases, and captured stdout/stderr are in [INTAKE-evidence.txt](INTAKE-evidence.txt). This establishes representative current behavior, not a passing test suite or exhaustive Unicode coverage. No regression assessment is possible before a change exists.

## Decisions requiring owner answers

1. **Which requirement yields for existing expansion cases?** May the release change old results specifically where Unicode uppercase expands, while preserving other results and exceptions? For `label("ß")`, exact compatibility requires `"SS"`; the new rule forbids it. If exact compatibility is absolute, the no-expansion requirement for existing callers must be revised. An opt-in mode alone would not satisfy the supplied requirement.
2. **What result replaces an expanding uppercase mapping?** Should such characters remain unchanged, or use a specified single-character replacement where available, with an explicit fallback? For example, should `"ß"` become `"ß"` or `"ẞ"`? What should `"ﬃ"` and `"ΐ"` produce when their current uppercase forms expand? A rule covering these cases is needed; choosing only a sharp-s special case would leave “any” Unicode input unresolved.
3. **What is the extent and unit of the no-expansion rule?** Does it apply only when the entire value is one Unicode code point, or to every character within any string? The former can leave `"straße" → "STRASSE"`; the latter changes that existing result too (for example to `"STRAßE"` under an unchanged-character fallback). Does “character” mean a Python code point or a user-perceived character, which can contain several code points? This affects whether decomposed sequences count as one-character inputs and what output length is permitted.

## Proposed defaults, pending those answers

- Reuse the existing `prefix` parameter and its positional/keyword calling forms; keep prefixes verbatim before the converted value. The empty default and per-call string support are already required. For example, `label("abc", prefix="pre:")` remains `"pre:ABC"`.
- Apply the no-expansion constraint to conversion of the value, excluding explicitly added prefix length. Otherwise even `label("a", "pre:") == "pre:A"` would conflict with a total-output-length constraint.
- Preserve existing exceptions and avoid new coercion, validation, or Unicode normalization unless an owner decision requires it. For example, `label(1)` currently raises `AttributeError`, and `label(b"abc")` raises `TypeError`; widening the accepted input domain was not requested.

Next step: record the owner's answers to the three behavioral decisions, then use them as inputs to a separately authorized design phase. No default above resolves the compatibility conflict or selects a Unicode mapping policy.
