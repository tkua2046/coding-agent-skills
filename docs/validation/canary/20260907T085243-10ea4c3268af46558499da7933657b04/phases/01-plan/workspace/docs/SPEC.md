# Migration contract and clarifications

Status: proposed addendum; review pending. [ORIGINAL](ORIGINAL.md) remains unchanged
and authoritative. This is intended behavior, not implemented functionality.
Rationale: [DESIGN](DESIGN.md).

## Requirements and proposed clarifications

Required: produce v2 settings, preserve stable IDs/values, keep original v1 usable
before completion including crashes, retry without loss/duplication, and switch
through `active.json` only after validation. Multi-process migration is excluded.

Proposed: migrate unique string IDs and finite standard JSON values only. Preserve
ID spelling/case and recursive value types. Reject unknown structural fields to
avoid silently dropping unmodelled data; expected shapes have exactly
`version`/`entries`, `id`/`value`, `version`/`settings`, or `format`/`path`.
Version/format must be integer 1 or 2, excluding booleans. Member names must be
unique. Existing direct v1 reading retains compatibility. These restrictions need
review, particularly numeric IDs accepted by today's reader.

Proposed APIs: `load(path)` supports both formats; `load_active(selector_path)`
checks selector/version agreement and resolves relative paths from its directory;
`migrate(selector_path)` returns the validated mapping after durable activation,
or immediately for valid active v2. Validation failures use `ValueError`; I/O
errors preserve their cause, distinguishing uncertain completion after selector
replacement. No implicit fallback or source removal occurs.

## Decisive acceptance examples

These are future checks. Unless stated otherwise, start with fixture format-1
selection; source bytes must remain unchanged in every case.

| Input / event | Expected result and state |
|---|---|
| Fixture theme `"dark"`, timeout `30` | Target is `{"version":2,"settings":{"theme":"dark","timeout":30}}`; selector is `{"format":2,"path":"settings-v2.json"}`. Direct v1 and active v2 loads return identical mappings. |
| Duplicate fixture theme IDs with dark/light values | Validation error before publication; selector and source unchanged, including the source's existing duplicate-ID error. No lossy map is accepted. |
| Numeric ID `7`, alone or alongside string `"7"` | Migration validation error without writes; no coercion. Existing direct v1 reading still accepts numeric IDs. |
| IDs `Theme`, `theme`, `""` with values `false`, `null`, `[1,{"x":"é"}]` | Three exact keys and original typed values survive migration and retry. |
| Empty entries | Successful v2 `settings: {}` activation. |
| Existing target timeout `"30"` versus source `30`, or target `true` versus source `1` | Full comparison fails, even with equal entry count; v1 remains selected. |
| Repeated JSON members, missing/unknown structural fields, malformed or non-finite values | Explicit validation error without activation; repeated members must be detected before dictionary construction loses them. |
| Crash leaving truncated target temporary file | v1 still loads; retry ignores temporary content, builds complete output and activates one exact mapping. |
| Crash after final target publication, before selector replacement | v1 remains selected; retry revalidates matching target and completes. Divergent target produces collision error without overwrite. |
| Crash during temporary selector write or around atomic replacement | Fresh caller sees complete old selector and v1 or complete new selector and validated v2, never partial selector bytes. Retry converges to v2. |
| Selector replaced; final sync or response fails | Uncertain completion; no rollback, original remains usable. Retry succeeds when selector validates as v2. |
| Repeated successful migration | Same mapping/selection, no added or dropped entries, no source rewrite. |
| Active v2 missing/corrupt or pointing to version 1 | Explicit error, no silent fallback. Valid relative selection also works from a different working directory. |
| Inject write, sync, validation or rename errors before selector replacement | No activation; source byte-identical. Retry after removing fault succeeds unless a divergent final target requires explicit resolution. |

Actual verification is recorded separately in [baseline evidence](evidence/migration-baseline.md).
