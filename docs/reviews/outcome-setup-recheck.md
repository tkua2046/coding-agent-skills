# Outcome setup — targeted OSR-01 recheck

**Verdict: ready for the reviewed evaluator correction. OSR-01 is reviewer-verified resolved. No material finding remains from this targeted recheck.** The positive control passes, and the saved conditional-skip mutant now fails specifically at the new documentation-only probe, with and without coverage installed.

Reviewed 7 September 2026. The [original review and counterexample](outcome-setup-review.md) remain unchanged. Only `workflow-setup/oracle.py` differs from the case snapshot reviewed there; no broader case or skill review was repeated.

## Tested identity

- Oracle SHA-256: `42127aa172895c51f3f9d28079449c85528c120530ca67a769adecb5ead08a9e`.
- Workflow-setup case tree: `b6fcdb87e7c39e8f3a3b9c122699ecdcd2601ad6e63361774b9dbdc8269d2e6d`, using the original review's tree-hash convention.
- Frozen engine: `40df1bb684f719db6013129e741cce106b7176714d0b5ace9bc0a3eed80d4fe2`.

The [hashed raw evidence](../validation/outcome-runtime/20260907T083358-osr01-recheck/manifest.json) retains the current case, the exact saved positive/mutant sources, interpreter availability checks, full sandbox executions, isolation results and before/after filesystem inventories. All manifest hashes were verified, and the current oracle still matched the executed bytes when this report was written.

## Actual results

All four executions used `runtime.sandbox_command` in disposable fixtures with the normal initial Git commit and installed hook. The second interpreter was the actual base Python with coverage absent, not a simulated import failure.

| Interpreter | Control | Whole oracle exit | New documentation-only hook result |
|---|---|---:|---|
| Prepared; coverage available | Saved positive | 0 | Exit 1; six tests executed, seeded assertion failed |
| Prepared; coverage available | Saved conditional-skip mutant | 1 | Exit 0; shortcut skipped tests, correctly rejected |
| Base; coverage absent | Saved positive | 0 | Exit 1; six tests executed, seeded assertion failed |
| Base; coverage absent | Saved conditional-skip mutant | 1 | Exit 0; shortcut skipped tests, correctly rejected |

[Detailed results](../validation/outcome-runtime/20260907T083358-osr01-recheck/summary.json) confirm that the scratch Git difference was exactly `README.md` in each run. For both positive runs, the transcript names `test_existing_failure` and reports `AssertionError: 7 != 8`; the rejection was caused by the intended failing test, not a launcher, discovery, coverage or working-directory error. Each mutant failed only the new `documentation-only-staging-runs-failing-baseline` check. All preceding oracle checks passed.

Private-read/network denial passed in all four runs. Independent before/after inventories, including Git metadata, confirmed restoration of entries, bytes and modes; no timeout or interruption occurred. Nonfatal macOS Git cache/global-ignore warnings were retained and did not determine the verdict.

## OSR-01 disposition

The correction establishes the adapted gate and known failing test in a scratch baseline before installing its hook, then stages only a documentation edit. This removes the pending Python change that masked the previous mutant. The optional `cwd` parameter correctly directs scratch commands while preserving the original helper's default root. The original success, seeded-failure, empty-discovery and restoration controls remain effective.

**Closed at the tested oracle hash above.** No actual control error was found. This is acceptance of the targeted evaluator correction, not semantic skill performance or human usability evidence. No runtime, grader, case product or prior review files were edited by the recheck; no broader testing or new rule was added.
