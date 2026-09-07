# Draft PR: Preserve surrounding spaces in exported text

Status: Blocked on implementation and a passing required gate.

Revision reviewed: `5c49170` (`main`)

## Behavior change

Surrounding spaces in exported text are user data and should be preserved. For example, exporting `"  x  "` should return `"  x  "`, not `"x"`. Consumers that want normalized text will need to trim it explicitly.

The current candidate does not yet implement that behavior: `serialize` converts the value to text and calls `strip()`, so it removes the surrounding spaces. The current regression test expresses the new preservation requirement and fails against this implementation.

## Validation

- Runtime: supplied `CANARY_PYTHON` (Python 3.12.4).
- Required current gate: `python -m unittest discover -s tests -v`, run through the supplied runtime.
- Result: failed with exit code 1 on 2026-09-07. One test ran; `test_spaces_are_data` expected `"  x  "` but received `"x"`.
- The earlier report's passing tests apply only to the previous candidate's normalized-string contract and test configuration. They are historical and do not validate this candidate or the new requirement.

## Remaining blockers

- Reconcile the serializer implementation with the whitespace-preservation requirement.
- Rerun the required current gate on the reconciled candidate and obtain a passing result before review readiness is claimed.
- No release validation or remote CI has been performed; no release is authorized.

This is a local draft only. No product code or version was changed, and no commit or PR publication was performed.
