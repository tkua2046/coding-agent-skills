# Prefix support intake

Status: proposed clarification addendum. The authoritative request remains [REQUEST.md](REQUEST.md).

## At a glance

Expose the existing per-call `prefix` argument as supported behavior without changing any call that omits it. The implementation already has the smallest mechanism requested; the remaining work is to confirm which parts of that currently internal behavior become public guarantees. No shared state, configuration, or callback interface is in scope.

## Confirmed requirements

| ID | Required behavior | Acceptance example | Source |
|---|---|---|---|
| R1 | Prefixes are supplied per call through `label`; `prefix` is a string whose default is `""`. | `label("item", prefix="pre-")` uses that prefix only for that call. | [REQUEST.md](REQUEST.md) |
| R2 | Omitting `prefix` preserves every existing result and exception; values must not be coerced. | `label("MiXeD") == "MIXED"`; `label(7)` continues to raise `AttributeError`, rather than producing `"7"`. | [REQUEST.md](REQUEST.md), [README.md](README.md) |
| R3 | Do not add shared prefix configuration or a callback API. | Two calls may pass different prefixes directly; neither changes later calls. | [REQUEST.md](REQUEST.md) |

## Current behavior and relevant files

- [labels.py](labels.py) defines `label(value, prefix="")` as `prefix + value.upper()`. Thus omitted-prefix behavior is already unchanged, positional and keyword prefixes both work, the prefix is preserved verbatim, no separator is inserted, and only `value` is uppercased.
- [README.md](README.md) describes `label(value)` as relied-on public behavior and explicitly says the optional prefix is still internal.
- No callers, packaging metadata, or tests exist in this repository. Public exposure will therefore need to be expressed in the library documentation and executable checks, but their detailed form belongs in a later design or implementation step.

## Baseline

Commands used the prepared `$CANARY_PYTHON` runtime. Raw output is recorded in [INTAKE-EVIDENCE.md](INTAKE-EVIDENCE.md).

| Check | Exit | Result |
|---|---:|---|
| `python -m unittest discover -v` | 5 | No tests were discovered; this is an incomplete baseline, not a passing suite. |
| `python -m py_compile labels.py` | 0 | The existing module compiles. |
| Focused calls against `label` | 0 | Confirmed omitted, positional-prefix, keyword-prefix, and current exception behavior. |

## Next consequential decisions

These are the unresolved public-contract choices. The defaults below reproduce the existing internal behavior and add no mechanism, so they are justified unless the owner needs a different caller experience.

| Decision for owner | Why it matters | Proposed default |
|---|---|---|
| **D1 — Is the prefix literal text with no automatic separator, while only the value is uppercased?** | With a mixed-case prefix, literal composition gives `label("ab", "id: ") == "id: AB"`; uppercasing the combined result would give `"ID: AB"`. Automatic punctuation would produce yet another result. This must be stable once public. | **Yes:** return the prefix unchanged immediately before `value.upper()`, with callers responsible for spaces or punctuation. This matches `labels.py` and the ordinary meaning of the existing argument. |
| **D2 — Support both positional and keyword use, or make the newly public argument keyword-only?** | Existing code accepts both `label("ab", "id-")` and `label("ab", prefix="id-")`. Keyword-only exposure is clearer but rejects the first form and requires a signature change. | **Support both forms.** It exposes the existing signature directly and avoids an unnecessary incompatibility, even though the argument was previously documented as internal. |
| **D3 — Are non-string prefixes simply outside the contract, with no new validation or coercion?** | Today `label("ab", 7)` raises Python's concatenation `TypeError`. Adding explicit validation would standardize the message/timing; coercing would instead return `"7AB"`, contrary to the stated string contract. | **No coercion and no explicit validator:** document a string prefix and retain operation-driven `TypeError` for invalid types. This keeps the implementation narrow. If a stable exception type/message for invalid prefixes is required, the owner should say so explicitly. |

Confirming D1–D3 is sufficient to proceed to a small design or directly authorized implementation. Nothing in the current evidence suggests a need for configuration, callbacks, or broader architecture work.
