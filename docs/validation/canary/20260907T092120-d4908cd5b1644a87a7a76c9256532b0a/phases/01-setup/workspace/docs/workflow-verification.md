# Local workflow verification — 7 September 2026

Outcome: the normal check command and installed hook passed the unchanged five-test
application suite. Coverage 7.16.0 was already available in the prepared Python
runtime. No packages, environments or application behavior were changed.

## Exercised checks

| Invocation / case | Result |
|---|---|
| Prepared Python, `tools/check.py` before edits | 5 tests passed |
| Prepared Python, `tools/check.py` after edits | 5 tests passed, coverage and JSON produced |
| `.git/hooks/pre-commit README.md` | 5 tests passed, coverage and JSON produced |
| Installed hook copied into isolated fixture, intentional failing test | Exit 1; 6 tests, one failure |
| Installed hook copied into isolated fixture, discovery matches nothing | Exit 1; explicit no-tests message |
| Prepared Python with `-S`, isolated fixture | 5 tests passed; coverage-unavailable notice |
| Same stdlib fallback, intentional failing test | Exit 1 |
| Same stdlib fallback, discovery matches nothing | Exit 1; explicit no-tests message |

The installed hook was already executable and identical to the maintained wrapper;
its delegation was retained. No local `core.hooksPath` override was configured.
The documentation invocation exercises the installed hook directly without a
commit; the wrapper unconditionally runs the complete suite and ignores filenames.

Coverage measured only `inventory.py`, with branches enabled: 58 statements,
one missing statement, 18 branches, two partial branches, displayed total 96%.
Missing output was `59->exit, 81`. No percentage threshold was added.
The configured outputs are `artifacts/.coverage` and `artifacts/coverage.json`.
Raw post-change outputs, individual report snapshots and exit statuses are in
[artifacts/verification-20260907-022300](../artifacts/verification-20260907-022300/).
These ignored local artifacts accompany this checkout, not a versioned distribution.

## Limits and restoration

`-S` simulated unavailable coverage by omitting site packages; it did not uninstall
anything. That path provides unittest gating only and generates no new coverage
reports. Zero-test coverage runs also emitted expected no-data warnings.

Tests used a workspace-local `TMPDIR` because the sandbox restricts system temporary
storage. Git emitted sandbox cache/config warnings during inspection. No external
integration or actual commit was performed.

Failure and discovery probes used isolated copies, removed on completion. The
application, sample data, original application tests, discovery configuration,
coverage settings and both hook files were preserved. Historical notes remain
separately labeled in [development history](development-history.md).
