# Prefix API intake

Intake only; no implementation or full design. This note supplements the unchanged [REQUEST.md](REQUEST.md:1).

## Confirmed scope

[REQUEST.md](REQUEST.md:1) requires a per-call string prefix, defaulting to empty, through the existing function; no coercion, shared configuration, or callbacks. Every result and error with an omitted prefix must remain compatible. These decisions need no further owner answer.

[README.md](README.md:1) identifies `label(value)` as the public interface and the existing prefix parameter as internal. [labels.py](labels.py:1) already accepts positional and keyword prefixes and returns `prefix + value.upper()`. With strings, `label('hello', prefix='pre:')` already returns `'pre:HELLO'`. The change exposes that capability publicly and establishes its input/error contract.

## Baseline and implications

The fixture contains no tests, test configuration, or documented check command. A bounded diagnostic probe completed with exit status 0; this is an observed baseline, not a passing test suite. Reproduction command, exit status, and raw stdout/stderr are recorded in [evidence](intake-evidence/run.txt); [probe source](intake-evidence/probe.py) and [output](intake-evidence/behavior.txt) are retained.

Omitted-prefix behavior includes `AttributeError` for `None`, `TypeError` for bytes, and even a custom `upper()` result whose reflected addition returns a tuple. Consequently, restricting or coercing `value`, or validating its uppercase result as a string, could violate the supplied compatibility requirement.

The internal implementation currently permits non-string prefixes in some combinations: bytes plus bytes returns bytes, and a list prefix plus a custom list-valued `upper()` returns a list. Those observations do not override the requested string contract. With an invalid prefix and invalid value together, `label(None, 7)` currently raises `AttributeError` while evaluating `value.upper()`.

## Owner decision

**For a supplied non-string prefix, should rejection occur before evaluating `value.upper()`, or should evaluation of the value retain priority?** Both can enforce the required string contract, but differ in observable exceptions and side effects:

- Prefix first: `label(None, 7)` raises a prefix `TypeError`; a custom `upper()` is not called.
- Value first: the same call raises the existing `AttributeError`; a custom `upper()` may run or raise before the prefix is rejected.

Recommendation, pending the owner's answer: reject invalid prefixes first with `TypeError`. This gives the newly public argument a consistent failure contract, including for bytes/list combinations that currently succeed. The explicit compatibility guarantee covers omitted prefixes, so it does not settle this choice for invalid supplied prefixes. No error-message wording is specified; use a clear message unless exact text is required by the owner.

## Proposed reversible defaults

- Preserve prefix text literally, including case and whitespace; add no separator. Example: `'pre:'` plus `'hello'` yields `'pre:HELLO'`, matching existing behavior.
- Retain positional and keyword use, with the existing empty default. Treat an explicit empty string like omission; introduce no distinction without a requirement.
- Accept `str` subclasses as strings, without coercion, matching the current ordinary subclass behavior. Do not add validation of `value` or its `upper()` result; the omitted-prefix examples above remain compatibility constraints.

These defaults follow the existing function and avoid additional API choices. The unresolved error-order decision above is the next consequential owner answer.
