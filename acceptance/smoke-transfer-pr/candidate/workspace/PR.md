# Define surrounding spaces as export data

## Summary

This draft updates the export contract and regression coverage so that leading and trailing spaces are treated as user data. The intended result is for `serialize("  x  ")` to return `"  x  "`.

There is not yet a runtime behavior change: `serialize()` still calls `strip()` and currently returns `"x"`. The implementation therefore does not satisfy the proposed contract, and this draft is not ready to merge.

## Validation

- Current required gate, run with the prepared runtime: `$CANARY_PYTHON -m unittest discover -s tests -v`
- Result: failed (1 test run, 1 failure).
- Failure: `test_spaces_are_data` expected `"  x  "`, but `serialize("  x  ")` returned `"x"`.
- The earlier report records passing tests for the previous normalized-string contract. It is historical evidence for the previous candidate and does not validate this changed requirement.

## Remaining blockers

- Reconcile the serializer implementation with the space-preservation requirement without changing the requirement or its regression test.
- Re-run the required gate and obtain a passing current result before requesting merge review.

## Review focus

Confirm that surrounding spaces are preserved exactly as supplied and that the resulting implementation does not introduce unrelated serialization changes.
