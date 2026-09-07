# Prefix exposure intake

Status: proposed clarification. Original requirement: [`REQUEST.md`](REQUEST.md) at baseline commit `3a2623b`. Relevant implementation: [`labels.py`](labels.py); stated compatibility surface: [`README.md`](README.md).

## At a glance

The requested outcome is to make the existing per-call `prefix` argument public. The request already settles the default, omitted-call compatibility, lack of coercion, and exclusion of shared configuration and callbacks; those constraints are not reopened here.

The owner should decide D1 and D2 below. D3 is a behavior-preserving default that only needs a response if different behavior is intended.

## Decisions for the owner

### D1 — Which invocation forms become public?

The current signature is `label(value, prefix="")`, so both of these work today:

```python
label("mixed", "pre-")          # "pre-MIXED"
label("mixed", prefix="pre-")  # "pre-MIXED"
```

Choose one:

- **Positional or keyword (proposed default):** publish the current signature and make both calls supported. This is the smallest change and does not silently withdraw an already-working form, even though the second parameter was previously internal.
- **Keyword-only:** publish `label(value, *, prefix="")`. This makes call sites more self-explanatory and leaves more positional flexibility later, but `label("mixed", "pre-")` would start raising `TypeError`.

Owner can answer: `D1 both` or `D1 keyword-only`.

### D2 — Is the string requirement enforced at runtime?

Direct concatenation rejects many non-strings, but not all. The current implementation produces this surprising result for a non-string with its own addition behavior:

```python
class AddablePrefix:
    def __add__(self, text):
        return f"custom:{text}"

label("ok", AddablePrefix())  # currently "custom:OK"
```

Choose one:

- **Enforce `isinstance(prefix, str)` (proposed default):** reject every non-string prefix with `TypeError`, accept `str` subclasses, and never coerce. This makes the stated type rule true rather than relying on incidental operator behavior.
- **Document the requirement only:** retain direct operator behavior. Ordinary invalid inputs such as `prefix=3` raise `TypeError`, but custom non-string operands can succeed; their behavior remains outside the supported contract.

If enforcement is selected, the proposed routine default is to validate `prefix` before calling `value.upper()`. Thus `label(None, 3)` reports the invalid prefix first, while the required omitted call `label(None)` retains its existing `AttributeError` unchanged.

Owner can answer: `D2 enforce` or `D2 document-only`.

### D3 — Preserve literal, delimiter-free concatenation

Proposed default: expose the parameter with its current semantics—prepend `prefix` exactly as supplied, add no separator, and uppercase only `value`:

```python
label("ßeta", "MiX-")  # "MiX-SSETA", not "MIX-SSETA"
label("item", "[A] ")  # "[A] ITEM"; spacing belongs to the caller
```

This follows the existing implementation and keeps presentation choices per call. If the prefix itself should be uppercased or a delimiter should be inserted, the owner should override D3 explicitly because either choice changes observable results.

The proposed related default is that explicitly passing `prefix=""` is equivalent to omitting it, including existing results and exceptions.

## Existing behavior and evidence

Using the prepared runtime, the following local probe was run:

```sh
"$CANARY_PYTHON" - <<'PY'
import inspect
from labels import label

cases = [
    ("basic omitted", lambda: label("MiXeD")),
    ("prefix positional", lambda: label("MiXeD", "pre-")),
    ("prefix keyword", lambda: label("MiXeD", prefix="pre-")),
    ("prefix preserved", lambda: label("ßeta", "MiX-")),
    ("invalid value omitted", lambda: label(None)),
    ("invalid prefix", lambda: label("ok", 3)),
]
print("signature", inspect.signature(label))
for name, call in cases:
    try:
        print(name, "=>", repr(call()))
    except Exception as exc:
        print(name, "=>", type(exc).__name__, repr(str(exc)))

class AddablePrefix:
    def __add__(self, other):
        return f"custom:{other}"

print("non-string with __add__ =>", repr(label("ok", AddablePrefix())))
PY
```

Observed baseline:

| Probe | Result |
|---|---|
| `inspect.signature(label)` | `(value, prefix='')` |
| `label("MiXeD")` | `"MIXED"` |
| `label("MiXeD", "pre-")` | `"pre-MIXED"` |
| `label("MiXeD", prefix="pre-")` | `"pre-MIXED"` |
| `label("ßeta", "MiX-")` | `"MiX-SSETA"` |
| `label(None)` | `AttributeError: 'NoneType' object has no attribute 'upper'` |
| `label("ok", 3)` | `TypeError: unsupported operand type(s) for +: 'int' and 'str'` |
| `label("ok", AddablePrefix())` | `"custom:OK"` |

No tests, packaging metadata, or in-repository callers are present, so local evidence cannot show whether any external user has adopted the internal two-argument form. That is why D1 remains an explicit public-compatibility choice rather than an inferred requirement.
