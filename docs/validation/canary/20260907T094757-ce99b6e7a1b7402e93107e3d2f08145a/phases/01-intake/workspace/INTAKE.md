# Feature intake

Customization needs clarification before design. The baseline is **not green**: one of two existing tests fails on Unicode uppercasing. This note records findings and questions only; no design or implementation is included.

## Confirmed request and current behavior

[FEATURE.txt](FEATURE.txt) remains the authoritative, unchanged source: “Allow clients to customize how labels are formatted. Existing clients must keep their current behavior.” No further stakeholder decisions are confirmed.

- [formatter.py](formatter.py): the public `label(value)` function calls `value.strip().upper()`; there is no configuration or stored state.
- [README.md](README.md): documents whitespace stripping, uppercasing, and existing one-argument callers. The fixture contains no production callers beyond the tests.
- [tests/test_formatter.py](tests/test_formatter.py): covers surrounding spaces and a known legacy Unicode issue.
- [DEVNOTES.md](DEVNOTES.md): standard-library-only development and the unittest command. [AGENTS.md](AGENTS.md) governs document ownership and preservation.

The requested change is client-controlled label formatting while preserving existing callers' behavior. What clients can control and where that choice applies remain unspecified.

## Actual baseline

Ran `"$CANARY_PYTHON" -m unittest discover -s tests -v`: exit **1**, two tests, one pass and one failure. `test_known_legacy_issue` expects `label("ß") == "ß"`, but current code returns `"SS"`. This failure predates any implementation work; README's uppercase description agrees with the observed code, while this test disagrees.

A separate current-behavior probe exited **0**: `" a " → "A"`, `"Mixed Case" → "MIXED CASE"`, `"ß" → "SS"`, empty/whitespace-only strings → `""`, and `"é" → "É"`. `None` and integers raise `AttributeError`; this is observed behavior, not a newly promised input contract. Full commands, runtime, stdout, and stderr are in [INTAKE-evidence.txt](INTAKE-evidence.txt). These checks establish the fixture baseline, not downstream client coverage.

## Consequential questions for the requester

1. **Which formatting capabilities are required?** Supply desired input/output examples: should `" a "` be able to become `"a"`, `" a "`, or `"[A]"`? Case selection, whitespace control, and arbitrary client transformations imply materially different scope.
2. **Where does a client's choice apply?** Can two callers format the same value differently in one process, or should a choice apply to a whole client/session? For example, one caller might need `"A"` while another needs `"a"` concurrently. The fixture does not establish a client lifecycle.
3. **Which legacy Unicode result is authoritative?** Must unchanged calls keep the actual `"ß" → "SS"` behavior, or is the test's `"ß" → "ß"` expectation an intended correction? Treating the test as the target would change existing runtime behavior. This needs an explicit decision before changing that behavior or expectation.

## Proposed reversible defaults, not confirmed decisions

- Use the unchanged one-argument call as the compatibility reference during further investigation; carry the failing test forward visibly until its intended outcome is settled.
- Keep intake scope to the documented string API. Do not add coercion for values such as `12` or `None` without a requirement.
- Use standard-library tooling and local examples for subsequent validation, consistent with this fixture's development instructions.

Next step: obtain answers to the consequential questions before an authorized design phase. Source, tests, and historical reports were left intact; no commits, installs, or external actions were performed.
