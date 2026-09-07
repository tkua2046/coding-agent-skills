# Feature intake: non-expanding labels and public per-call prefixes

Status: clarification needed before design. The next consequential decisions are the result to return when uppercase expands and whether the rule applies only when the entire argument is one code point or to every code point in a longer string.

## Original requirements

Source: [`REQUEST.md`](REQUEST.md), preserved verbatim:

> All old callers must get exactly the same output. The new release must also stop expanding any one-character Unicode input into multiple characters, including existing callers. Add optional per-call string prefixes, default empty.

The repository also states in [`README.md`](README.md) that `label(value)` produces uppercase text, existing results and exceptions are relied upon, and the currently internal prefix parameter is not public.

## Current behavior and relevant files

[`labels.py`](labels.py) contains the whole library. Its public behavior is currently implemented as `prefix + value.upper()` with `prefix=""` by default.

- `label("abc")` returns `"ABC"`.
- `label("abc", "pre:")` returns `"pre:ABC"`; the prefix is unchanged and is prepended after uppercasing the value.
- Python's full uppercase mapping can expand one Unicode code point: `label("ß")` returns `"SS"`, `label("ﬃ")` returns `"FFI"`, and `label("ΐ")` returns the three-code-point string `"Ι\u0308\u0301"`.
- Existing error behavior follows naturally from the two operations: `label(1)` raises `AttributeError`, while `label("abc", None)` raises `TypeError`.

No tests or packaging metadata are present. On the supplied Python 3.12.4 runtime (Unicode database 15.0.0), `python -m unittest discover -v` found zero tests and exited 5, so there is no green test baseline. `python -m py_compile labels.py` exited 0. Probe output and exact commands are recorded in [`INTAKE-EVIDENCE.txt`](INTAKE-EVIDENCE.txt).

## Supplied decisions and compatibility boundary

- Existing callers retain their exact outputs.
- One-character Unicode inputs must no longer expand, and this change includes existing callers.
- Prefixes are per-call strings, optional, and default to the empty string.
- Existing results and exceptions are compatibility-sensitive (`README.md`).

The first two requirements conflict for an existing call such as `label("ß")`: retaining `"SS"` preserves its exact output, while preventing expansion requires a different result. The new Unicode rule appears to be an explicit exception to general compatibility, but that precedence and the replacement result are not stated.

## Decisions the owner needs to make

### D1 — What result replaces an expanding uppercase mapping?

This needs an explicit answer because it defines the feature's visible output and Unicode strategy.

- Preserve the original code point when `.upper()` expands: `label("ß") → "ß"`, `label("ﬃ") → "ﬃ"`, and `label("ΐ") → "ΐ"`. This guarantees one output code point but can leave lowercase text in an otherwise uppercase label.
- Use a single-code-point uppercase form where one can be selected, otherwise preserve the input: for example, `label("ß") → "ẞ"`, while `"ﬃ"` has no equivalent single uppercase ligature and would remain `"ﬃ"`. This needs a defined mapping source/version beyond Python's current `.upper()` result.
- Preserve today's output for compatibility: `label("ß") → "SS"`. This resolves the conflict in favor of old output but does not satisfy the stated non-expansion rule.

Also confirm that the chosen non-expanding behavior is the intended exception to “exactly the same output” for existing callers. There is no justified default here: the first two choices produce materially different public text, while the third contradicts the new rule.

### D2 — Where does the non-expansion rule apply?

Does it apply only when the entire `value` contains one Unicode code point, or must no code point expand inside any input string?

- Whole-input rule: `label("ß")` changes, but `label("straße")` remains `"STRASSE"` because the argument has more than one code point.
- Per-code-point rule: both calls suppress the expansion; under D1's preserve-input option, `label("straße") → "STRAßE"`.

The phrase “one-character Unicode input” most directly supports the whole-input rule, so that is the proposed default. Owner confirmation is warranted because callers are likely to encounter these characters inside ordinary multi-character labels, and the alternatives have different compatibility impact.

## Justified implementation defaults

These details are already constrained by the request or current behavior and need not be reopened unless the intent differs:

- Interpret “character” as one Unicode code point (`len(value) == 1`), not one user-perceived grapheme cluster. For example, precomposed `"é"` is one code point, while decomposed `"e\u0301"` is two. This matches Python string iteration and avoids introducing a new grapheme-segmentation contract.
- Measure expansion in the transformed value only, excluding the prefix; otherwise any non-empty prefix would itself violate the length rule.
- Publicize the existing optional `prefix` parameter without changing its behavior: keep positional and keyword calls, preserve prefix casing, and produce `label("abc", "pre:") → "pre:ABC"`.
- Accept strings as the documented prefix type but add no new coercion or eager validation. This preserves current results and exception behavior, including the exception from a non-string prefix.
- Keep the empty-prefix path behaviorally identical except for the Unicode case selected in D1/D2.

Once D1 and D2 are answered, the behavioral boundary is specific enough for a focused design; this note intentionally stops before proposing an implementation.
