# Settings migration contract

Status: proposed; design and plan reviews pending. [Original requirements](ORIGINAL.md)
remain unchanged and authoritative. This is a proposed contract, not shipped behavior.

## Required invariants

- Preserve every stable ID and value; reject duplicate IDs instead of choosing a winner.
- Leave original v1 bytes unchanged and readable, including after a crash. Retain v1
  after success too; source deletion is outside scope.
- Retry must neither duplicate nor omit entries.
- `active.json` selects the file and format. Switch only after independently reading
  back and validating the complete persisted v2 file against the source.
- No multi-process migration is required.

## Proposed interfaces and input boundary

Keep `settings.load(path)` returning an ID-to-value mapping and add v2 support while
retaining legacy direct v1 reading behavior. Add `settings.load_active(active_path)`
to resolve the selected path relative to the selector directory and enforce agreement
between selector `format` and selected file `version`. Add explicit
`settings.migrate(active_path)`, returning the validated settings mapping on success.
Reads do not initiate migration. These API names and return semantics await review.

The supplied source becomes `{"version":2,"settings":{"theme":"dark","timeout":30}}`.
Object order and whitespace are immaterial. Migration IDs must be strings: do not
stringify, normalize or fold case. Empty strings and Unicode remain unchanged.
Values may be any finite JSON value, including null, arrays and nested objects;
preserve types and array order, and insert no defaults. In particular, `true` and `1`
must not compare equal for migration validation.

Strict migration parsing rejects duplicate IDs, repeated JSON members at any depth,
nonstring IDs, nonfinite numbers, invalid container shapes, missing fields and
unsupported versions. Require integer versions/formats, excluding booleans. Reject
extra source envelope/entry fields rather than silently discarding metadata. New v2
envelopes and selectors have exactly their documented fields. These migration rules
do not retroactively tighten the legacy direct v1 reader.

Malformed data and selector mismatch raise `ValueError`; filesystem failures surface
as `OSError`. Identify the file/condition without dumping settings. Invalid active
data fails visibly; there is no automatic fallback. The caller must serialize source
edits and migration so validation and publication use one source snapshot.

## Decisive acceptance examples

A1–A8 are proposed tests shared by design and plan, not completed checks.

| ID | Input or interruption | Expected result/state |
|---|---|---|
| A1 | Supplied source, selector `{"format":1,"path":"settings-v1.json"}` | v2 settings exactly `{"theme":"dark","timeout":30}`; validated destination selected with format 2; original source bytes unchanged. Direct v1 and active v2 reads return the same mapping. |
| A2 | Supplied duplicate fixture: theme `dark`, then theme `light` | `ValueError`; source and selector unchanged; no winner chosen. |
| A3 | IDs `""`, `"7"`, `"Theme"`, `"theme"`, `"é"` with respective values `null`, `false`, `0`, `[]`, `{"x":[1,"1"]}` | Exactly those five keys and typed values survive. Empty entries produce empty settings. Numeric ID `7` instead of `"7"` is rejected without changing the source. |
| A4 | Missing value, repeated `value` member, NaN, extra source field, unknown version or selector/file disagreement | Error before activation; unchanged source remains readable under the old reader wherever it was readable before. No guessing or defaults. |
| A5 | Crash during destination write, after durable destination publication, or after selector staging but before replacement | Original v1 remains selected and usable. Retry reconstructs all entries and selects one complete validated v2 file. Orphans never become selected merely because they exist. |
| A6 | Readback changes timeout to `31`, drops theme, adds a key, changes `30` to `true`, or truncates JSON; also inject write/sync/replace failures before activation | Error and no selector switch; original source and selector bytes unchanged. |
| A7 | Crash after selector replacement, before function return | Selected file is complete validated v2; v1 retained. Retry validates selected v2 and returns without another conversion or activation. Success acknowledgement is not necessary for committed activation. |
| A8 | Selector already names v2; alternatively its v2 target is missing/corrupt | Valid v2: validate and return without writes. Invalid v2: visible error, preserve selector and retained v1; never overwrite the active file or silently roll back. |

## Pending contract decisions

The original does not define nonstring IDs, ambiguous JSON, extra metadata, API,
concurrent settings edits, or whether crash includes power loss. The proposed strict
boundary, serialized writes and API await review. Numeric IDs cannot retain their
type as JSON object keys: supporting them requires an explicit contract change.
See [design](DESIGN.md#validation-and-review-boundaries) for crash scope and the
activation commit point. No unresolved choice is treated as approved.
