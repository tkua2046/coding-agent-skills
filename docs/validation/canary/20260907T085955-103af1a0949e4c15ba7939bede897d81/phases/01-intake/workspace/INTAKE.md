# Feature intake

Intake is complete; design is deferred pending the decisions below. The baseline has one pre-existing failure. This is a small public-interface feature whose main uncertainty is compatibility, so focused clarification is sufficient before design.

## Authority and current behavior

The unchanged source request is [FEATURE.txt](FEATURE.txt:1):
> Allow clients to customize how labels are formatted. Existing clients must keep their current behavior.

Confirmed requirements are customization and preservation of existing clients' behavior; no customization contract has been confirmed. [README.md](README.md:1) documents one-argument `formatter.label(value)` calls and stripping followed by uppercase. [formatter.py](formatter.py:1) implements exactly `value.strip().upper()`, with no configuration or stored state. The only callers found in this fixture are [tests/test_formatter.py](tests/test_formatter.py:1); real client needs cannot be inferred from them. [DEVNOTES.md](DEVNOTES.md:1) supplies the standard-library test command.

Examples observed: `" a " → "A"`, `" Straße " → "STRASSE"`, and whitespace-only input → `""`. `None` and integers raise `AttributeError`; broader input support is not requested. The proposed behavioral change is to allow an explicit client choice of formatting while preserving ordinary existing calls. Its interface and semantics remain undecided.

## Actual baseline

Ran `"$CANARY_PYTHON" -m unittest discover -s tests -v`: exit **1**, two tests, one pass and one failure. `test_known_legacy_issue` expects `label("ß") == "ß"`, but the implementation returns `"SS"`. This failure occurred before any code changes; the baseline is **not green**. A read-only behavior probe exited **0** and confirmed the examples above. Commands, runtime, stdout, and stderr are in [INTAKE-evidence.md](INTAKE-evidence.md). These are the checks actually run; no feature validation is claimed.

## Decisions requiring the user's answer before dependent design

1. **What customization must clients perform, and at what scope?** For example, should one call produce `"Hello"` from `" hello "`, must clients be able to add arbitrary prefixes such as `"ID: hello"`, or must a reusable client preference affect many calls? Representative desired input/output pairs and per-call versus persistent scope determine the required capability; the fixture does not answer this.
2. **Does customization receive the original string or an already normalized string, and what happens on failure?** A client preserving `" hello "` needs the original spaces and case, which are lost after existing normalization. If custom formatting fails, should the call raise or fall back to `"HELLO"`? These choices materially affect observable results.
3. **Which behavior governs the existing Unicode conflict?** Should an unchanged call to `label("ß")` continue returning `"SS"`, consistent with current code and documented uppercasing, or return the test's expected `"ß"`? The latter changes today's behavior. Keep this conflict explicit; the feature request alone does not authorize choosing a correction.

## Proposed reversible defaults (not confirmed answers)

- Use existing one-argument calls and observed results as the provisional compatibility reference; leave the failing Unicode expectation and implementation intact pending a decision.
- Keep investigation within the existing formatter and standard-library workflow. Do not add dependencies, broader input coercion, or unrelated cleanup without a demonstrated requirement.
- Reuse the current unittest location for later acceptance examples once behavior is agreed; no API signature or implementation mechanism is selected here.

No source, tests, usage documentation, or historical reports were changed. No design, implementation, installs, commits, or external actions were performed. Next step: obtain the consequential answers above, then authorize design separately.
