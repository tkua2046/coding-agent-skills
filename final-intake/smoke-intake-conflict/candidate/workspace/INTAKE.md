# Intake: non-expanding Unicode labels and public prefixes

Status: two owner decisions are open. Original requirements: [REQUEST.md](REQUEST.md) at baseline commit `d2d9eeeed719166cb17d66c90cb5adf33983df0f`; existing public contract: [README.md](README.md); implementation inspected: [labels.py](labels.py).

## At a glance

The requested Unicode change conflicts with exact output compatibility for inputs that expand today: `label("ß")` currently returns `"SS"`, so it cannot both keep that output and stop producing multiple characters. The owner next needs to choose which requirement prevails for those calls and, if no-expansion prevails, define their single-code-point result. The prefix behavior can otherwise be exposed with preservation defaults below.

Evidence is limited to this repository and the prepared Python 3.12.4 runtime (Unicode database 15.0.0). There are no tests or in-repository callers, so compatibility with external callers cannot be inspected here.

## Confirmed requirements (not questions)

| ID | Required behavior | Acceptance example or boundary | Source |
|---|---|---|---|
| R1 | Existing callers retain their results and exceptions. | `label("a") == "A"`; existing invalid calls must fail as before. | [REQUEST.md](REQUEST.md), [README.md](README.md) |
| R2 | The new release must not expand a one-character Unicode input into multiple characters, including for existing callers. | Today `label("ß") == "SS"` (length 2), which the new behavior must not return for that one-code-point input. | [REQUEST.md](REQUEST.md) |
| R3 | A caller may supply an optional string prefix per call; omission means the empty prefix. | The preserved call shape supports both `label("ab", "pre-")` and `label("ab", prefix="pre-")`. | [REQUEST.md](REQUEST.md); current [labels.py](labels.py) |

R1 and R2 cannot both hold literally for currently expanding inputs. Any exception to compatibility remains proposed until the owner resolves D1.

## Decisions needed from the owner

### D1. Which requirement prevails for existing one-code-point calls that expand?

There is no implementation that satisfies both statements for `label("ß")`:

| Precedence | Consequence | Example |
|---|---|---|
| Exact output compatibility | R1 holds, but R2 cannot: `label("ß")` remains the two-code-point string `"SS"`. |
| No expansion, including existing callers | R2 holds; R1 needs an explicit, narrow exception for affected one-code-point inputs, whose new results are decided in D2. |

The wording “including existing callers” points toward the second choice, but the absolute “exactly the same output” statement prevents treating that precedence as confirmed. If the second choice is confirmed, compatibility should remain exact for all inputs and exceptions outside the narrow rule.

### D2. What should replace an uppercase expansion?

The requirement states what must not happen but does not define the result. A single general uppercase replacement does not exist for all cases. The owner should confirm representative expected outputs, especially these:

| Input | Current result | Proposed lossless fallback | Other possible policy and consequence |
|---|---|---|---|
| `"ß"` | `"SS"` | `"ß"` | A special case could produce `"ẞ"`, but that is not a general rule for all expanding characters. |
| `"ﬃ"` | `"FFI"` | `"ﬃ"` | Taking only `"F"` would lose information. |
| `"ΐ"` | `"Ι\u0308\u0301"` | `"ΐ"` | Taking only `"Ι"` would discard both marks. |

Proposed default: when the applicable input's normal uppercase result has more than one code point, return that input code point unchanged. This guarantees one code point and preserves information, but it intentionally means that some results are not uppercase. Truncating the uppercase result should not be inferred because it is lossy.

## Justified preservation defaults

Unless the owner says otherwise, these choices follow the existing implementation and the exact-compatibility requirement:

- Interpret “one-character Unicode input” literally as a complete `value` containing one Unicode code point (`len(value) == 1`), not as each code point within a longer value or as a user-perceived grapheme cluster. Thus `label("straße")` remains `"STRASSE"`. This is directly testable and minimizes the compatibility impact without reopening the supplied one-character scope.
- Keep `label(value, prefix="")`, allowing the prefix as either the second positional argument or the `prefix=` keyword.
- Preserve the prefix verbatim and prepend it to the transformed value: `label("ab", "pre-") == "pre-AB"`, not `"PRE-AB"`. A prefix is deliberate added content and is outside the no-expansion rule for `value`.
- Do not normalize Unicode or change behavior for uppercase operations that already return zero or one code point.
- Do not add eager type validation. Existing exceptions remain observable: for example, `label(None)` raises `AttributeError`, while `label("x", None)` raises `TypeError`.
- Preserve empty-string behavior: `label("") == ""` and `label("", "pre-") == "pre-"`.

## Baseline evidence

Repository inspection found only `README.md`, `REQUEST.md`, and the two-line `labels.py` outside the supplied skill; no tests or callers are present. Running the prepared interpreter with direct calls established:

- `label("a") -> "A"`
- `label("ß") -> "SS"` (2 code points)
- `label("ﬃ") -> "FFI"` (3 code points)
- `label("ΐ") -> "Ι\u0308\u0301"` (3 code points)
- `label("ab", "pre-") -> "pre-AB"`, identically via `prefix="pre-"`

An exhaustive scan of the prepared runtime found 102 individual code points whose `str.upper()` result contains more than one code point. That count is runtime/Unicode-version evidence, not a proposed hard-coded compatibility list.
