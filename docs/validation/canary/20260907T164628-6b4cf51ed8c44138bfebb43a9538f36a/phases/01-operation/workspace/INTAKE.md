# Prefix API intake

The existing function already supports per-call prefixes. The next consequential decision is **when an invalid prefix fails relative to evaluating `value.upper()`**. Ordinary prefix behavior can follow the existing implementation. This small API change needs a short intake; no implementation or full design is included.

## Confirmed scope

[REQUEST.md](REQUEST.md) requires exposing prefixes through the existing function, a string prefix defaulting to empty, no coercion, and preservation of **every result and error when the prefix is omitted**. Shared configuration and callbacks are excluded. These decisions need no further confirmation. [README.md](README.md) identifies the prefix parameter as currently internal; [AGENTS.md](AGENTS.md) limits this work to intake and preservation of supplied records.

## Existing behavior and baseline

[labels.py](labels.py:1) is the sole library entry point: `label(value, prefix="")` returns `prefix + value.upper()`. There are no supplied callers, tests, or development/check commands. A local probe using `"$CANARY_PYTHON" -B -` completed with exit status 0; [raw output and probe details](INTAKE-evidence.txt) record observations, not a passing test suite.

- `label("ab")` returns `"AB"`; either positional or keyword `"pre-"` returns `"pre-AB"`.
- Omitted-prefix calls on `None` raise `AttributeError`; bytes raise `TypeError`. A custom `upper()` result with reflected addition can even produce a tuple. Preserving the old expression's behavior matters beyond ordinary strings; adding value validation or returning `value.upper()` directly for an empty prefix would change existing behavior.
- Non-string prefixes are not currently checked. Two bytes arguments succeed; an invalid prefix paired with a failing `upper()` reports the latter's error first. The bytes success conflicts with the requested string-only contract for the newly public argument.

## Owner decision

**For an explicitly supplied non-string prefix, should rejection precede `value.upper()`, or should existing evaluation order be retained?** For `label(None, prefix=None)`, early prefix validation would raise a prefix `TypeError`; evaluating the value first currently raises `AttributeError`. If `upper()` performs work or raises its own exception, this choice also determines whether that work happens. The request fixes prefix type and forbids coercion, but does not settle this ordering for invalid explicit prefixes. Early rejection is a reasonable preference for the public API; this remains an owner decision, not an accepted requirement.

## Proposed defaults

- Preserve literal concatenation: `label("ab", prefix="pre-") → "pre-AB"`, with no automatic separator or uppercasing of the prefix. This follows existing behavior.
- Retain the parameter name, position, and empty default, allowing both positional and keyword calls. No fixture evidence justifies narrowing the signature.
- Reject non-string prefixes with `TypeError`, accept string subclasses, and add no validation or coercion of `value`. Treat exact wording of new prefix errors as an implementation detail; existing omitted-prefix errors remain protected by the request.

These defaults are proposed, not additional confirmed requirements. Once the owner answers the error-order question, the behavior is sufficiently bounded for a later design or implementation phase.
