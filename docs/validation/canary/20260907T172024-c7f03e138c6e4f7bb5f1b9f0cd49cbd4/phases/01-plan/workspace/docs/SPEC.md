# Proposed migration contract

Status: draft supporting [DESIGN.md](DESIGN.md); review status is in [PLAN.md](PLAN.md).
This describes proposed behavior, not implemented capability. [ORIGINAL.md](ORIGINAL.md)
is unchanged and authoritative.

## Input, output and caller

- The selector is a JSON object with integer `format` 1 or 2 and a nonempty `path`
  naming a sibling file. Reject absolute paths, parent traversal and aliases that
  would overwrite the source or selector. Resolve paths against the selector's
  directory, not the working directory.
- Migration accepts integer `version: 1` and an `entries` array of records with
  unique string `id` and a `value`. Reject malformed records, duplicate IDs,
  duplicate JSON members, unsupported versions and non-finite values before
  modifying authoritative files. Extra v1 metadata may be ignored: preserved data
  are the stable IDs and their values.
- v2 has integer `version: 2` and a `settings` object mapping exact IDs to exact
  semantic JSON values. Empty entries become `{}`. Reject duplicate members and
  invalid/non-finite values in v2 too. Boolean versions/formats are invalid.
- `load(path)` returns a mapping for valid v1 or v2. `load_active(active_path)`
  reads one selector snapshot, requires matching format/file version and returns
  the selected mapping. Missing, malformed or mismatched state raises an error;
  reads neither migrate nor guess a fallback.
- `migrate(active_path)` follows the design's publication protocol and returns
  the validated mapping on success. Validation/conflict errors use `ValueError`;
  filesystem errors remain visible as `OSError`. On errors the caller keeps its
  prior in-memory mapping, and inspects/retries uncertain completion.
- For v1 selection, require identical source/output ID sets and recursively equal
  values with matching JSON types. Reuse a matching destination after revalidation;
  preserve and reject conflicting output. For v2 selection, validate the selected
  file and sync file, selector and directory to finish a possibly interrupted
  commit. Return that mapping without regeneration or a retained-source comparison:
  the selector is the authority for completion.
- Success selects `{"format":2,"path":"settings-v2.json"}` for the supplied v1.
  Old source bytes remain unchanged on success, rejection, interruption and retry.
  Scratch files and unselected output never authorize a caller switch.

## Acceptance examples

| Case | Required observation |
|---|---|
| Supplied source and selector | Output parses as `{"version":2,"settings":{"theme":"dark","timeout":30}}`; active reads return the same mapping; source bytes unchanged. |
| IDs `"01"`, `"1"`, `""` with values `null`, `false`, `{"items":[1,"1",true]}` | Three distinct keys and all value types survive. Empty entries yield empty settings. |
| Supplied duplicate `theme`, or non-string IDs `1` and `"1"` | Error before activation, no coercion or deduplication; original selector/source unchanged. |
| Candidate changes `false` to `0`, drops/adds an ID or changes a nested value | Full comparison fails even if parsing or entry counts pass; v1 stays selected. |
| Truncated JSON, duplicate JSON members, wrong version, missing value or non-finite number | Validation error; no activation. |
| Crash during scratch write or after candidate sync, before output publication | v1 selector still works; source unchanged; retry ignores orphan scratch and completes without duplication. |
| Crash after output publication/directory sync, before selector replacement | v1 remains selected; retry validates/reuses matching output and activates. |
| Crash during selector scratch write or immediately before replacement | Original selector remains complete/readable; retry completes normally. |
| Crash immediately after selector replacement, including before final directory sync or success response | Under supported crash recovery, selector is old or new, never torn; either points to a complete valid file. Retry completes from either state; original v1 remains usable. |
| Disk-full, write/replace/fsync errors at every persistence boundary | No success reported. Before commit v1 remains selected; after commit completion may be uncertain and retry resolves it. |
| Repeat after successful migration | Same mapping and source bytes; no new or duplicated settings. |
| Existing matching / conflicting destination | Matching output is revalidated/reused; corrupt or different output blocks activation and preserves source, selector and conflicting bytes. |
| Corrupt selector, format/version mismatch or missing selected file | Explicit error, no fallback or destructive repair. |
| Reader runs from another working directory, or holds old selector during activation | Relative resolution still works; old reader finishes with preserved v1 and fresh reader sees validated v2. |

Tests use isolated copies and verify source bytes and persisted state, not only
return values. Process-kill tests do not simulate actual power loss.
