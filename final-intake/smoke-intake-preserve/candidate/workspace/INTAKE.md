# Prefix support intake

Status: proposed clarification. Original requirement: [REQUEST.md](REQUEST.md).

## At a glance

The requested API shape already exists internally as `label(value, prefix="")`; the remaining work is to define which parts of that behavior become a public contract. The next consequential decisions are whether a prefix is always literal, whether both positional and keyword calls are supported, and whether invalid prefixes need deliberate validation semantics. There are no repository tests or callers, so the observations below establish the local baseline but cannot prove downstream compatibility.

## Confirmed requirements

| ID | Required behavior | Acceptance example | Source |
|---|---|---|---|
| R1 | Prefixes are supplied per call through `label`; there is no shared configuration or callback API. | Two calls may independently use `label("one", "A-")` and `label("two", "B-")`. | [REQUEST.md](REQUEST.md) |
| R2 | Omitting the prefix preserves every existing result and exception. | `label("MiXeD") == "MIXED"`; an unsupported value must fail exactly as it did before prefix exposure. | [REQUEST.md](REQUEST.md) |
| R3 | The prefix is a string whose default is the empty string, and values are not coerced into strings. | `label("x", 7)` must fail rather than return `"7X"`. | [REQUEST.md](REQUEST.md) |

## Decisions for the owner

### 1. Is the prefix literal, including case and separators?

The requirement does not say whether uppercasing applies only to `value` or to the complete label, nor whether separators are inserted automatically.

- **Proposed default:** preserve the existing internal behavior: concatenate the prefix unchanged, with no implicit separator, before the uppercased value.
- Examples: `label("MiXeD", "pre-") == "pre-MIXED"`, `label("x", "") == "X"`, and `label("", "pre-") == "pre-"`.
- Alternative contract: `label("MiXeD", "pre-") == "PRE-MIXED"` if the prefix is part of the text to uppercase. That is observably different and should be chosen explicitly if desired.

The proposed default is justified by the existing implementation and introduces no new formatting rules.

### 2. Are both positional and keyword prefix calls public?

The current signature accepts both `label("x", "pre-")` and `label("x", prefix="pre-")`. The request calls `prefix` a parameter but does not state whether it should be keyword-only.

- **Proposed default:** support both forms because they already work; making the parameter keyword-only would reject an existing call form.
- Alternative contract: publish only `label("x", prefix="pre-")` and deliberately reject a second positional argument. This is clearer at call sites but changes the current signature.

### 3. What rejection behavior is promised for a non-string prefix?

“Do not coerce” establishes rejection, but not whether the library must validate eagerly or may rely on concatenation to fail.

- **Proposed default:** do not add explicit validation; require only that a non-string prefix is not coerced and that the call raises `TypeError` when concatenation is reached. Example: `label("x", 7)` currently raises `TypeError`.
- If a stable exception message, an earlier failure, or rejection before processing `value` is required, that needs an explicit contract. For example, `label(7, 8)` currently raises `AttributeError` while evaluating `value.upper()` before the invalid prefix is encountered.

The proposed default keeps omitted-prefix exception behavior untouched and avoids expanding the compatibility promise to exact new error text.

## Existing behavior and evidence

`labels.py` currently implements `return prefix + value.upper()`. With the prepared `$CANARY_PYTHON` runtime, a local probe observed:

| Call | Observed result |
|---|---|
| `label("MiXeD")` | `"MIXED"` |
| `label("MiXeD", "pre-")` | `"pre-MIXED"` |
| `label("MiXeD", prefix="pre-")` | `"pre-MIXED"` |
| `label("", "pre-")` | `"pre-"` |
| `label("MiXeD", 7)` | `TypeError` |
| `label(7)` | `AttributeError` |
| `label(7, 8)` | `AttributeError` |

Probe command: `"$CANARY_PYTHON" - <<'PY'` ran an inline script that imported `labels`, inspected `inspect.signature(labels.label)`, and invoked the cases above. The observed signature was `(value, prefix='')`. A repository file listing with `rg --files` found no test files or in-repository callers; `README.md` only says that callers rely on the old one-argument results and exceptions and that the prefix parameter is not yet public.
