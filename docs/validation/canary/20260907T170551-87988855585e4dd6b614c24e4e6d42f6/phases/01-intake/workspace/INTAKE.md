# Label customization intake

Customization needs clarification before design: the request does not define the desired formatting choices, and a legacy test conflicts with current behavior. The baseline is **not green**. No design or implementation was performed.

## Confirmed requirements and current behavior

- [FEATURE.txt](FEATURE.txt:1) is the unchanged source request: allow clients to customize label formatting; existing clients must keep their current behavior. No additional stakeholder answers are confirmed.
- [formatter.py](formatter.py:1) exposes `label(value)` and returns `value.strip().upper()`. [README.md](README.md:1) documents strings and existing one-argument callers. Only test callers are present in this fixture; external client expectations cannot be verified here.
- Observed examples: `" a " → "A"`, `" Mixed Case " → "MIXED CASE"`, `"ß" → "SS"`, `" Straße " → "STRASSE"`; empty and whitespace-only strings produce `""`. Interior spaces remain intact.
- [tests/test_formatter.py](tests/test_formatter.py:1) has two tests. [DEVNOTES.md](DEVNOTES.md:1) owns the standard-library test command. [AGENTS.md](AGENTS.md:1) requires preserving requirements/history and limits document ownership. No prior reports or separate behavior specs were found.

## Actual baseline

Ran `"$CANARY_PYTHON" -B -m unittest discover -s tests -v` with bytecode writing disabled, using prepared Python 3.12.4: **exit 1**, two tests, one pass and one failure. `test_known_legacy_issue` expects `label("ß") == "ß"`, but receives `"SS"`. This failure predates feature changes; source and tests remain unchanged.

A read-only signature/behavior probe exited **0**, confirming the examples above and the single-argument interface. Exact executed arguments, exit statuses, and raw stdout/stderr are in [INTAKE-evidence.txt](INTAKE-evidence.txt). These checks establish this fixture's behavior, not compatibility across all clients or Python versions. An initial `git status --short` returned no entries but emitted sandbox cache/global-ignore access warnings; it is not relied on as a clean-tree guarantee.

## Consequential questions for the user

1. **What customization must clients support?** Supply representative input/output pairs: should `" Mixed Case "` become `"mixed case"`, `"Mixed Case"`, retain surrounding spaces, or support other transformations? This determines the feature's behavioral scope; no particular format or extension mechanism is confirmed.
2. **Where should a formatting choice apply?** Can two calls in the same process need different formatting, or should a client select a persistent default? For example, one client may need `"A"` while another needs `"a"` from the same input. The answer affects configuration scope and isolation.
3. **Which Unicode behavior is authoritative for existing clients?** Should `"ß"` continue producing `"SS"`, as the implementation and documented uppercasing do, or is the test's unchanged `"ß"` intentional? Resolving this may require a separate legacy correction; intake does not change either behavior or the failing test.

## Proposed reversible defaults (not confirmed answers)

- Use current one-argument results as the provisional compatibility reference, including trimming and empty-string handling; keep the Unicode conflict explicitly open. Any customization should require an explicit client choice.
- Keep the documented string-input scope; do not add coercion of numbers or `None` unless requested.
- Stay within the standard library and existing repository conventions. Defer API shape and configuration mechanism to design after the consequential answers.

Next step: obtain the behavioral examples, choice scope, and legacy Unicode decision before authorizing design. No commits, installs, external actions, or changes to source requirements, implementation, tests, or prior reports were made.
