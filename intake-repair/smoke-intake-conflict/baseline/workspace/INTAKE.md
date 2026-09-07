# Feature intake: non-expanding labels and public prefixes

Status: one behavioral decision is still required. The original specification in
[`REQUEST.md`](REQUEST.md#L1) remains authoritative.

## At a glance

`label` already accepts a per-call `prefix`, but that parameter is documented as
internal. The requested release makes it public and changes the uppercase result
for a one-code-point string when Python's full Unicode uppercase mapping contains
more than one code point. Existing behavior can otherwise remain compatible.

The next consequential decision is what single code point to return when the full
uppercase mapping expands.

## Current behavior and relevant files

- [`labels.py`](labels.py#L1) defines the entire implementation as
  `label(value, prefix="")`: it evaluates `value.upper()` and prepends `prefix`
  unchanged.
- [`README.md`](README.md#L1) is the only API documentation. It promises existing
  results and exceptions for `label(value)` and says `prefix` is not yet public.
- There are no tests or other in-repository callers.

On the prepared Python 3.12.4 runtime, focused probes observed:

| Call | Current result |
|---|---|
| `label("a")` | `"A"` |
| `label("ß")` | `"SS"` |
| `label("ﬀ")` | `"FF"` |
| `label("ΐ")` | `"Ϊ́"` |
| `label("ß", "id:")` | `"id:SS"` |
| `label("straße")` | `"STRASSE"` |

Baseline command: `"$CANARY_PYTHON" -` with the focused assertions and probes
supplied on stdin. Exit status was 0; it covered ordinary text, empty text, the
existing prefix, and the existing `AttributeError` for `label(None)`. The
repository has no test command or test suite. Probe stdout is in the current
task execution record; no durable evidence file was created.

## Supplied behavior and justified defaults

| Requirement | Intake interpretation | Status |
|---|---|---|
| Preserve old callers' exact outputs. | Preserve results and exceptions except where the explicitly required non-expansion rule necessarily changes a result. | Confirmed by `REQUEST.md`; the exception follows from “including existing callers.” |
| A one-character Unicode input must not expand. | Apply the rule when `value` contains one Unicode code point. The transformed value must contain at most one code point; a prefix is separate and may make the complete label longer. | Confirmed requirement; code-point interpretation is the narrow compatibility-preserving default. |
| Add an optional per-call string prefix, default empty. | Publicize the existing `prefix=""` parameter. Preserve its current positional-or-keyword use, prepend it verbatim, and add no new validation. | Confirmed requirement plus compatibility-preserving defaults. |
| Inputs longer than one code point. | Keep current full-uppercase behavior: for example, `label("straße")` remains `"STRASSE"`. A combining sequence such as `"e\u0301"` is also outside the one-code-point rule. | Proposed default: this follows the request's explicit one-character scope and preserves old outputs. |

## Outstanding decision

When a one-code-point input has a multi-code-point full uppercase mapping, what
single-code-point result should `label` return?

- **Preserve the input code point:** `label("ß") -> "ß"`,
  `label("ﬀ") -> "ﬀ"`, and `label("ΐ") -> "ΐ"`. This is uniform and
  guarantees no expansion, but the result is not uppercase where a distinct
  single-code-point uppercase form exists.
- **Use a single-code-point uppercase form when one is available, otherwise
  preserve the input:** for example, `label("ß") -> "ẞ"`, while a character
  without a suitable one-code-point uppercase form remains unchanged. This keeps
  more of the function's uppercase intent, but requires defining which Unicode
  mapping/version is authoritative and can produce a mix of converted and
  unchanged characters.

This choice also determines the value after a prefix: with prefix `"id:"`, the
examples above become either `"id:ß"` or `"id:ẞ"`. Truncating the existing
mapping (for example, `"ß" -> "S"`) is not proposed because it loses information
without support in the request.
