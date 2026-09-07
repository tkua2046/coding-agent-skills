# Migration contract addendum

Status: proposed details; original requirements remain authoritative and unchanged
in [ORIGINAL.md](ORIGINAL.md). Current code still implements v1 reading only.
This document owns proposed behavior; [DESIGN.md](DESIGN.md) owns rationale and
[PLAN.md](PLAN.md) owns pending delivery. Review remains pending.

## Required invariants

- Preserve every stable ID and value in the mandated v2 `settings` object.
- Original v1 data remains usable before completion, including across crashes.
- Retry cannot duplicate or drop entries.
- `active.json` selects the current file/format. Switch only after successful
  validation; no multi-process migration is required.

## Proposed interfaces and validation

`load(path)` continues returning an ID/value dictionary for v1 and additionally
reads v2. Existing v1 success and duplicate-ID behavior remain compatible.
`load_active(active_path)` validates the marker, resolves its path relative to its
directory, checks format/version agreement, and returns the selected mapping.
Neither read API migrates or writes. `migrate(active_path)` returns the validated
selected mapping on success, including an already-v2 retry. Validation errors use
`ValueError`; filesystem failures propagate as `OSError`. A filesystem failure
after marker replacement can have committed: the caller must retry/re-read rather
than assume v1 is still selected. No CLI is proposed.

Migration accepts a v1 object with integer version 1 (not boolean), an entries
array, and entries containing string `id` and JSON `value`. IDs must be unique,
including the empty string as a valid ID. V2 requires integer version 2 and a
`settings` object. Migration and v2 parsing reject duplicate object member names,
malformed JSON, non-finite numbers, missing required fields, and non-string v1
IDs. Proposed strict migration schemas reject extra fields instead of silently
discarding possibly meaningful metadata. Marker requires integer `format` 1 or 2
and a nonempty local filename `path`; version must match the selected file.
These stricter migration rules do not retroactively tighten direct v1 reads.

Preservation means the same JSON value types and recursively equal contents,
including nested objects, arrays, null and booleans. Object order and whitespace
are not significant; array order is. Numeric values must round-trip without
precision loss using the reader's Python JSON model; comparison must distinguish
booleans, integers and floating-point values. This does not promise preservation
of original numeric spelling. V1 source bytes themselves remain unchanged.

## Acceptance examples

All checks below are proposed, except the two baseline reader tests documented
in [evidence](evidence/migration-baseline.md).

| Case / input or interruption | Expected result and state |
|---|---|
| Supplied v1 fixture and `{"format":1,"path":"settings-v1.json"}` | Candidate is semantically exactly `{"version":2,"settings":{"theme":"dark","timeout":30}}`. After validation/publication marker is `{"format":2,"path":"settings-v2.json"}`. Active reader returns `{"theme":"dark","timeout":30}`; original bytes unchanged. |
| Supplied duplicate fixture: `theme=dark`, `theme=light` | `ValueError` before publication; no last-value-wins conversion. Marker and source unchanged, existing destination untouched. The source is already invalid; migration must preserve it, not claim to repair it. |
| Entries `[]`; separately IDs `""`, `"01"`, `"Theme"`, `"theme"` with values `null`, `false`, `[1,"1"]`, `{"x":30}` | Empty source yields empty settings. Other example preserves all four distinct keys and their exact typed values; no normalization. |
| Numeric ID `1` beside string ID `"1"`; missing value; duplicate raw JSON member; `NaN`; unsupported version | Validation fails without activation or source mutation. Numeric IDs are rejected rather than converted. |
| Candidate has same count but `timeout` renamed to `delay`, value `30` changed to `true`/`"30"`, or an extra ID | Equivalence validation rejects it; v1 stays active. |
| Kill during temporary candidate write, or fail validation/file sync/destination replace | Marker remains v1; original valid fixture still loads. Retry from the source eventually yields exactly the two expected entries. |
| Kill after destination replace/directory sync but before marker replace, including during temporary marker write | Ignore complete orphan v2 and partial marker temp; v1 remains selected. Retry regenerates candidate, validates and activates once. |
| Kill immediately after marker replace but before success response | Marker selects complete validated v2 on process restart. Source unchanged. Two further migrations return the same mapping and do not append, duplicate or rewrite active data. |
| Fail final directory sync after marker replacement | Report I/O failure with potentially committed outcome; no rollback or source deletion. Re-read marker and validate; retry handles whichever committed state is present. |
| Marker says format 2 but selected file is v1, truncated, or has duplicate settings keys | Active reader and retry fail explicitly without mutation; no silent fallback. |
| Load active marker from a different working directory | Resolve `settings-v1.json`/`settings-v2.json` beside the marker and return the same result. |

Power-loss behavior is an open review decision described in the design, not a
verified guarantee. Acceptance for process crashes must include real subprocess
termination in addition to deterministic fault injection.
