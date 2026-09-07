# Feature intake

Source: [FEATURE.txt](FEATURE.txt), unchanged. This note is an addendum, not a replacement. Intake only; no design or implementation is authorized by this note.

## Confirmed scope and current behavior

The request allows clients to customize label formatting and requires existing clients to keep their current behavior. No customization modes, interface, or error policy have been confirmed.

[formatter.py](formatter.py) exposes `label(value)` and returns `value.strip().upper()`. [README.md](README.md) documents this behavior and one-argument callers. Leading/trailing whitespace is removed, internal spaces remain, and Unicode uppercasing applies: `" a " → "A"`, `"ß" → "SS"`, `" Straße " → "STRASSE"`, and `"" → ""`. A `style` keyword currently raises `TypeError`; this probe establishes only that the keyword is unsupported, not a proposed API.

[tests/test_formatter.py](tests/test_formatter.py) contains the only callers found in this fixture. External client needs and usage are not available here. There is no configuration or persistent state in the implementation. [AGENTS.md](AGENTS.md) defines artifact ownership; [DEVNOTES.md](DEVNOTES.md) provides the standard-library test command.

## Practical baseline

Executed the documented command using the prepared runtime: `"$CANARY_PYTHON" -m unittest discover -s tests -v`, with `PYTHONDONTWRITEBYTECODE=1` (Python 3.12.4). Exit **1**: two tests ran, one passed and one failed. `test_known_legacy_issue` expects `label("ß") == "ß"`, while the unchanged implementation returns `"SS"`. This is a reproduced pre-existing failure, not a feature regression; the baseline is not green.

Raw evidence: [command and status](evidence/intake-baseline/unittest.command.txt), [stdout](evidence/intake-baseline/unittest.stdout.txt), [stderr](evidence/intake-baseline/unittest.stderr.txt).

A separate behavior probe exited **0** and confirmed whitespace, case conversion, Unicode expansion, empty strings, and rejection of the sampled customization keyword. Evidence: [command and status](evidence/intake-baseline/behavior-probe.command.txt), [stdout](evidence/intake-baseline/behavior-probe.stdout.txt), [stderr](evidence/intake-baseline/behavior-probe.stderr.txt). Its successful exit does not supersede the failed suite.

An initial `git status --short` emitted sandbox warnings about inaccessible Git configuration and tool cache paths. It produced no status entries, but is not relied upon as proof of repository cleanliness. No commits or external actions were performed.

## Consequential questions for the requester

1. **What customization outcomes are required, and who supplies them?** Are callers choosing case/whitespace options, adding a prefix/template, or supplying arbitrary formatting logic? For example, should `" Ab "` support `"ab"`, `" Ab "`, `"ID: AB"`, or client-defined output? These imply materially different capabilities. Request representative input/output pairs before selecting an interface.
2. **Where should customization apply?** Is it chosen per invocation or configured once for a client? For example, can two clients format `" Ab "` as `"ab"` and `"AB"` independently in the same process? This determines the needed scope and isolation. If multiple transformations are requested, also confirm whether they receive the original or already normalized value: preserving `" Ab "` requires access to its original spaces.
3. **How should the existing Unicode test conflict be resolved?** The request and README favor preserving the observed `"ß" → "SS"` behavior, but the test expects `"ß"`. Confirm whether the test expectation is stale or whether Unicode preservation is a separately authorized behavior change. Changing the legacy result could break existing clients; do not silently resolve the conflict by changing code or tests.

These questions are outstanding, not confirmed decisions. No stakeholder has been contacted.

## Proposed reversible defaults

- Keep customization opt-in and preserve the existing one-argument path, including stripping and Python Unicode uppercasing, pending resolution of the test conflict. Thus `label(" a ")` remains `"A"` and the observed Unicode result remains `"SS"`.
- Keep the scope to string formatting and standard-library facilities; do not introduce implicit coercion, locale-specific rules, or persistence without a concrete requirement. For example, accepting `42` as `"42"` would be new behavior, not a required compatibility fix.
- Leave the known failing test and source code untouched during intake. Track the conflict explicitly rather than bundling a legacy fix into customization work.

These are proposals that can be revised before design, not a selected implementation. Invalid customization handling and detailed acceptance examples remain dependent on the requested capabilities. No additional checks are claimed as executed. Next justified step: obtain the consequential answers before designing the customization contract.
