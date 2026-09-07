# Label customization intake

Intake only; design and implementation remain pending. The repository has an existing baseline with **one passing test and one pre-existing failure**. Customization semantics and a legacy Unicode expectation need clarification before design.

## Authority and current behavior

- Original request: [FEATURE.txt](FEATURE.txt:1), preserved unchanged. Clients must be able to customize label formatting, and existing clients must retain current behavior. No customization API or examples are specified.
- [README.md](README.md:1) documents `formatter.label(value)` as stripping surrounding whitespace and uppercasing strings; existing callers use one argument.
- [formatter.py](formatter.py:1) implements `value.strip().upper()` directly, with no configuration or state. For example, `" a "` becomes `"A"`, `"Straße"` becomes `"STRASSE"`, and whitespace-only input becomes `""`.
- [tests/test_formatter.py](tests/test_formatter.py:1) is the only test file. [DEVNOTES.md](DEVNOTES.md:1) owns the standard-library test command; [AGENTS.md](AGENTS.md:1) defines document ownership and preservation rules. No other caller or packaging entry point was found in the fixture.

## Baseline and evidence

Ran the documented unittest discovery with the prepared runtime: `"$CANARY_PYTHON" -B -m unittest discover -s tests -v`. Exit **1**, two tests run: `test_spaces` passes; `test_known_legacy_issue` expects `label("ß") == "ß"`, but actual output is `"SS"`. This failure predates any source change; the baseline is not green.

Raw command, runtime, stdout/stderr: [baseline.txt](intake-evidence/baseline.txt). Separate illustrative observations: [probes.txt](intake-evidence/probes.txt). Original source fingerprints: [source-sha256.txt](intake-evidence/source-sha256.txt). Initial `git status --short` reported no changes but emitted sandbox warnings; see [inspection.txt](intake-evidence/inspection.txt). No source, tests, or historical reports were changed.

## Consequential questions requiring an answer

1. **What custom formatting must clients express?** Supply representative input/output examples: should `" MiXeD "` support `"mixed"`, `"MiXeD"`, or an arbitrary result such as `"[MiXeD]"`? Limited built-in choices and arbitrary client logic imply different scope and contracts.
2. **Does customization replace the entire transformation or retain whitespace stripping?** A preserve-case customization could return `" MiXeD "` or `"MiXeD"`; this determines which input the customization sees and what output is acceptable.
3. **Where must a customization apply?** Can two calls format the same value differently, or must a client configure many existing calls together? For example, one client may need `"abc"` and another `"ABC"` in the same process. This affects configuration scope and isolation.
4. **How should the legacy Unicode conflict be resolved?** Current code and the README's uppercase rule produce `"SS"` for `"ß"`; the test expects `"ß"`. Preserving observed behavior and satisfying that test conflict. Confirm which behavior is authoritative before changing either code or the test.

## Proposed reversible defaults (not confirmed decisions)

- Keep the one-argument path and its observed behavior as the working compatibility baseline, pending the Unicode answer; customization is opt-in.
- Retain Python standard-library tooling and string-focused scope. Do not add coercion or locale behavior by assumption (current `None` and integer inputs raise `AttributeError`).
- Keep usage in README, operations in DEVNOTES, and clarification answers in an addendum linked to FEATURE.txt. Keep the legacy failure visible and unchanged during intake.

Next step: obtain the consequential answers, then request or authorize design. Future acceptance checks should cover approved customization examples and unchanged one-argument behavior; these checks have not been implemented or run.
