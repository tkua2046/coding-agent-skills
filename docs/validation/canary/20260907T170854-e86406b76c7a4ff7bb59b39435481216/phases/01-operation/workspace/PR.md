# Draft: Preserve surrounding spaces in exported text

Snapshot: current fixture candidate at `2f22cdfc8a74f1275ad45f9be85cffebc92c9b91`. Local draft only; blocked on the current required gate.

## Behavior and scope

[CHANGE.md](CHANGE.md) requires surrounding spaces to survive text export because they are user data. The current regression test expects `serialize("  x  ")` to return `"  x  "`. Actual behavior remains `"x"`: `serializer.py` still applies `str(value).strip()`. The candidate records the new requirement in a test, but does not yet implement the requested behavior.

## Validation

Ran the [documented gate](DEVNOTES.md), `python -m unittest discover -s tests -v`, using the supplied `CANARY_PYTHON` runtime with bytecode writing disabled. Result: **FAIL**, exit code 1; one test ran and failed (`SerializerTests.test_spaces_are_data`). See [current gate output](evidence/prepare-pr-gate.txt).

The [previous report](previous-report.md) describes a passing previous candidate under the old normalization contract. It is preserved as historical evidence and does not establish validation for the current requirement or tests. No remote CI validation was performed.

## Remaining blockers

The implementation must preserve surrounding spaces and the required gate must pass before this candidate is ready. Product fixes are outside this preparation task and remain pending. No product code, tests, prior reports, or version were changed; no commit or PR publication was performed.
