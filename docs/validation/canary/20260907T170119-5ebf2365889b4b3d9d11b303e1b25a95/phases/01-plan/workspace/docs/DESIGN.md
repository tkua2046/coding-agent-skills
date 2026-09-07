# Settings migration design

Produce a separate v2 file, validate its persisted contents against v1, then
atomically replace `data/active.json` to select it. Keep the original v1 file
unchanged, including after success. This costs an additional copy but preserves
recovery without an undo log. For the supplied data, the result is
`{"version":2,"settings":{"theme":"dark","timeout":30}}`, and the selector
changes from `{"format":1,"path":"settings-v1.json"}` to
`{"format":2,"path":"settings-v2.json"}` only after validation.

Decision status: proposed; design and plan reviews remain pending. The crash
scope and completion boundary below are consequential proposals for those
reviews. No implementation is authorized in this task.
Requirements: [unchanged original](ORIGINAL.md). Delivery and review status:
[plan](PLAN.md). Baseline and bounded experiment: [evidence](EVIDENCE.md).
Previous documents: [snapshot](history/PRE-MIGRATION.md).

## Verified baseline and scope

`settings.load(path)` parses v1 and returns an ID-to-value dictionary. It rejects
duplicate IDs and versions other than 1. The two tests cover the supplied valid
file and duplicate-ID file. `active.json` selects a relative filename and format,
but no caller/selector reader is implemented in this fixture. The previous
design describes that caller as intended context, not verified code.

The migration covers one selected settings file, one process, and no concurrent
settings writers during migration. A caller can keep an already loaded snapshot;
new loads resolve the selector once and load its selected file. No removal of v1,
background migration, database, dependency, or multi-process coordination is
needed. Concurrent writes would require a separate consistency design.

## Data and caller contract

Retain `load(path)` and its dictionary return shape, adding v2 support. Add a
selector-aware load entry point and an explicit migration entry point; their
exact names can be chosen during implementation. Resolve selector paths relative
to the selector directory, not the working directory. Limit this migration to
ordinary files within that directory; reject escaping paths and source/target/
selector aliases before writing. The supplied fixture satisfies this boundary.
Check selector format against the selected file's version and fail visibly on
missing files, malformed selectors, or mismatches; do not silently fall back.

V1 stable IDs become v2 object keys, preserving spelling and case. Require unique
string IDs before conversion: non-string IDs cannot map losslessly to JSON object
keys, so reject them without activation. Preserve each JSON value recursively,
including null, booleans, numbers, arrays, and objects. Order of entries/object
keys is not meaningful. Missing fields, invalid structure, non-finite numbers,
and duplicate JSON object member names are errors. Duplicate-member rejection
must happen while parsing, before a dictionary can discard information.

Validate the entire source before creating output. The migration accepts the
documented envelope and entry fields; reject unknown envelope/entry metadata
rather than silently discarding it. Objects inside values retain all keys.
These stricter malformed-input rules are proposed; the existing reader checks
only version and duplicate IDs and accepts some inputs outside this contract.
Existing valid v1 callers and the two fixture expectations must remain compatible.

For v2 require version 2 and a `settings` object. Read back the staged file using
the v2 parser and compare its complete ID set and type-sensitive JSON values
against the validated source, not just counts or a successful parse. In particular,
`true` must not compare equal to `1`. Encoding whitespace is not an acceptance
condition. The same validation rules apply to direct and selector-aware loads.

## Publication, interruption, and retry

Use `settings-v2.json` beside the selector as the destination for this fixture.
Write temporary artifacts in that same directory so replacement does not cross
filesystems. Reserve and document migration-owned temporary names; never delete
arbitrary files. A previously present destination is a conflict unless it is a
valid, complete semantic match for the current v1 source. Never overwrite a
conflicting destination. Under the single-writer scope, a matching destination
may be reused after full validation.

1. Read the selector once. When it selects v1, validate and hold the full source
   mapping; do not modify the source. When it already selects valid v2, return
   that mapping as an idempotent success without rewriting it. Invalid selected
   v2 is an error, not permission to rebuild or silently select v1.
2. Write the complete v2 snapshot to a migration-owned temporary file, flush and
   sync it, close it, reopen it, and validate against the source. Never append or
   merge on retry. Validation or I/O failure leaves the v1 selector in place.
3. Publish the validated file by same-directory atomic replacement into the
   absent destination (or reuse a validated identical destination). Sync the
   directory before preparing activation. The selector still selects v1.
4. Write a complete new selector to a separate temporary file; flush/sync it and
   validate its format and target. Recheck the published target against the
   source. Atomically replace `active.json`, then sync its directory before
   acknowledging durable success. The caller loads v2 only via this validated
   publication sequence.

The selector replacement is the logical completion/activation point. A process
crash before it leaves v1 selected and usable; a crash after it can leave v2
selected even if the caller never received success. Retry resolves that lost
acknowledgement by validating the selected v2 and returning success. This is
necessary because a filesystem commit and a caller acknowledgement cannot be
atomic together. “Successful completion” is proposed to mean the validated
publication, not receipt of a return value. The original v1 remains usable in
either case.

If the final directory sync fails after selector replacement, report an
indeterminate durability outcome, reread the selector on retry, and do not claim
that v1 is necessarily still selected. Do not attempt an automatic rollback
which would introduce another uncertain write. Before activation, abandoned temp
files and an unselected complete target indicate interrupted work; retry ignores
or removes only owned temporary artifacts, validates/reuses a matching target,
and otherwise stops on a conflict. No separate progress journal is required:
the selector is the authority and all outputs are complete snapshots.

Crash guarantee proposed for this fixture: process interruption on a filesystem
providing atomic same-directory replacement. File and directory sync ordering
also targets durable publication, but the local probe establishes syscall support
only; it does not prove power-loss behavior. If the requirement includes machine
or storage failure, supported filesystem durability guarantees and power-loss
testing must be established before claiming that wider acceptance. Review must
resolve this scope; do not silently assume it away.

In-place conversion is rejected because a partial write could destroy v1.
Selecting v2 before read-back validation is rejected because parseable output can
still omit an entry. Append-based recovery is rejected because retries could
duplicate entries. Keeping immutable source plus a single selector avoids the
extra recovery states of a journal for this one-file, single-writer migration.

## Decisive acceptance examples

These are proposed requirements-derived checks, not executed migration tests.

| Case | Required observable result |
|---|---|
| Supplied v1 and active selector | Persist exact v2 mapping above, activate format 2, and return the same mapping through both read APIs; v1 bytes unchanged. |
| IDs `Theme` and `theme`, empty string ID; values null, false, 0, arrays and nested objects | Preserve distinct keys and all value types/content, including across reload. |
| Supplied duplicate-ID v1; duplicate JSON keys; non-string ID; malformed input | Fail before activation; original bytes and selector unchanged; no silently lost entry. |
| Candidate parses but drops `timeout`, changes 30 to 31, or changes true to 1 | Read-back comparison rejects it; v1 stays active. |
| Inject failure during output write or validation | Partial output is unselected; selected v1 still loads; retry produces one complete mapping. |
| Interrupt after target publication but before selector replacement | Selector remains v1; retry validates and reuses the complete target, activates once, and loses no entries. |
| Interrupt during atomic selector replacement | Fresh load sees either complete v1 selector or complete v2 selector, never partial JSON; each selected file is valid. |
| Interrupt after replacement but before acknowledgement | Fresh load and retry validate selected v2; no duplicate/drop, and v1 remains readable. |
| Final sync error after replacement | Report uncertain durability; retry inspects actual selector, with no false assertion that activation failed. |
| Existing conflicting target, invalid selected v2, selector/version mismatch | Stop with a diagnostic and preserve files; no overwrite or implicit fallback. |
| Repeated migration after success | Same mapping and selection, no additional entries or output copies; original v1 unchanged. |

Verification must cover fresh-process reloads at publication boundaries, injected
I/O failures, selector-relative paths, and preservation of source bytes. Unit
tests alone cannot establish atomic replacement or storage durability guarantees.
