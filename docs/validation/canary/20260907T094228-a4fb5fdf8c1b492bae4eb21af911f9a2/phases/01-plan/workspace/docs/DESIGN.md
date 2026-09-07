# Design: settings v2 migration

Status: proposed; design review pending. Authority: [original requirement](ORIGINAL.md).
Implementation is deferred. The proposal preserves v1 bytes and publishes validated
v2 settings through an atomic replacement of `active.json`. This costs a second
data file but makes interruption recoverable without undoing writes to the source.
The next action is the requested design review, followed by the separately pending
[plan review](PLAN.md); neither was performed in this task.

This migration merits explicit compatibility and recovery analysis because a bad
activation could lose persisted settings. Contents: [baseline](#baseline),
[decisions](#decisions), [protocol](#protocol), [acceptance](#acceptance),
[open decisions](#open-decisions-and-validation).

## Baseline

`settings.load(path)` parses v1 and returns an ID-to-value dictionary, rejecting
duplicate IDs and versions other than 1. The two existing tests cover the supplied
normal and duplicate-ID files. `data/active.json` selects `settings-v1.json` with
format 1; selection is described as caller-owned, but no caller implementation is
present. There is no v2 reader, migration, recovery, or crash test.
See [inspection and experiments](evidence/migration-baseline.md).

Historical design, retained verbatim:
> The caller reads data/active.json and loads the selected v1 file. Stable IDs are
> unique; duplicate IDs are errors. No migration or recovery protocol exists yet.

## Decisions

The original requires stable IDs and values, usable original v1 data before
completion including crashes, retry without loss/duplication, validation before
switching, and no multi-process migration. The following are proposed engineering
decisions, not already approved requirements.

| Choice | Reason and consequence / alternative |
| --- | --- |
| Keep the selected v1 source byte-for-byte, including after success. | In-place rewriting needs rollback and exposes partially written originals. A retained source allows manual recovery and avoids defining backup deletion in this task. |
| v2 is `{"version":2,"settings":{ID:value}}`; migratable IDs must be strings and unique. | Object keys match the required example. Coercing numeric IDs changes identity and can collide with string IDs; an entry-array alternative would change the required v2 shape. Reject non-string IDs without activation; do not silently normalize case, whitespace, or Unicode. Existing direct v1 loads keep their compatibility behavior. |
| Strict migration/v2 parsing and round-trip validation. | Reject duplicate object members at all levels, invalid structure, non-finite numbers and unsupported versions. Default JSON decoding silently drops duplicate keys. Preserve complete JSON values, including types, nested structure and array order; object ordering and whitespace are not data. Compare recursively with type-aware equality, not Python's `True == 1`. No defaults or coercion. Extra envelope/entry fields are rejected by migration rather than silently discarded; this narrower migration domain needs review. |
| Keep `load(path)` as a direct reader, add v2 support; propose `load_active(selector_path)` and `migrate(selector_path)`. | Explicit migration keeps reads free of write side effects. `load_active` reads one selector snapshot, resolves its path relative to the selector directory, requires its format to match the payload version, then reads that immutable file. Callers using direct v1 paths must adopt selector loading to switch. There is no existing caller code to update here. |
| One atomic selector replacement is the logical commit. | Replacing data and selector independently as mutable active files creates inconsistent windows. An immutable validated target must exist first. A crash after commit but before return can leave v2 active; retry determines success from disk. Requiring v1 whenever no return was observed would be incompatible with crash-safe acknowledgement. |
| One migration/writer at a time; concurrent readers allowed. | The requirement excludes multi-process migration. This proposal also requires no settings or selector edits during migration, including other threads. Source rechecks alone cannot close that race. Locking and concurrent-write merging are deferred. |

Selector contract: exactly `format` (integer 1 or 2) and `path` (nonempty string).
For this fixture, supported migration paths are relative filenames in the selector
directory. Reject source/target/selector aliasing, symlinks and non-regular files;
do not overwrite unrelated destination data. Broader paths and symlink behavior
are pending compatibility decisions. Readers surface missing files, malformed
JSON and version/format mismatch as errors; they never guess a replacement file.
Validation failures use `ValueError`; filesystem failures retain `OSError` details.
The migration returns the validated settings on success; error messages identify
the failed phase and whether activation may already have occurred.

## Protocol

1. Read and validate the selector and selected payload. If already format 2,
   strictly validate the selected v2 file and return its settings without rewriting
   it. An invalid active v2 file is an error, not permission to revert to v1.
2. For format 1, strictly validate the complete source and build the exact v2 map
   in memory. Do not open the source for writing. Reject duplicate or unsupported
   IDs and values before creating a candidate. Full-file memory use follows the
   current reader; streaming and very large datasets are outside this proposal.
3. Write a uniquely named migration candidate in the selector directory, flush
   and fsync it, close it, then reopen and validate the serialized representation
   against the source's exact ID set and typed values. A parseable file alone is
   insufficient. Use that unique filename as the immutable final v2 target;
   fsync its directory before permitting activation. Never reuse an unvalidated
   leftover or modify a file named by an active selector.
4. Write a separate unique temporary selector containing format 2 and that target's
   basename; flush/fsync and close it. Atomically replace `active.json` in the same
   directory, then fsync the directory before reporting success. The original
   v1 file remains present and readable. Old selector snapshots still name v1;
   new snapshots name the complete validated v2 file.
5. On failure before selector replacement, leave v1 selected. Best-effort removal
   of this attempt's unselected files must not hide the original error. After an
   interruption with format 1 still selected, retry starts from the original,
   creates a fresh complete candidate, and never appends or merges leftovers.
   After replacement, retry validates active v2 and returns success. Orphans may
   consume disk space but do not duplicate logical entries. Automated historical
   orphan cleanup and source deletion are deferred; never delete an active target.

File fsync, same-directory replacement, and directory fsync succeeded in a bounded
workspace probe. This supports feasibility, not a proven crash guarantee. The
intended supported environment is a local filesystem with atomic rename and working
file/directory durability barriers. A process crash exposes either old or new
selector, never partially written JSON. Machine/power-loss durability additionally
depends on filesystem and hardware guarantees; those must be confirmed for the
deployment environment. No claim is made for network filesystems or broken storage.
A failed post-replacement directory sync has an uncertain durability outcome:
report the error, retain both data files, and inspect the selector on retry; do not
attempt rollback. In all cases, v1 bytes survive and every potentially active v2
target was validated before selector replacement.

## Acceptance

These are proposed checks, not implemented tests. Expected values are derived from
the fixture and original requirement, independently of a future converter.

| Example / input | Expected result and persisted state |
| --- | --- |
| Supplied v1: `theme="dark"`, `timeout=30`, active format 1. | Candidate parses exactly as `{"version":2,"settings":{"theme":"dark","timeout":30}}`; active format 2 references it; both direct readers and `load_active` return `{"theme":"dark","timeout":30}`. Original v1 bytes unchanged. |
| Supplied duplicate fixture (`theme` twice). | `ValueError`; original and selector bytes unchanged, no activation and no first/last-wins result. |
| IDs `1` and `"1"`, or numeric ID `1` alone. | Migration rejects non-string ID, leaving v1 usable. No coercion to `"1"`. String IDs `"01"` and `"1"` remain distinct. |
| Empty entries; or `{"id":"payload","value":[null,true,1,1.5,{"x":"é"}]}`. | Empty settings object; or same ID and exact typed nested value, respectively. No dropped nulls, boolean/number substitution, or list reordering. |
| Candidate has missing `timeout`, an extra ID, changed value/type, duplicate member, or truncated JSON. | Validation fails before activation; selector stays format 1 and original remains readable. |
| Terminate during candidate write, after candidate validation/directory sync, or during temporary selector write. | `active.json` still selects intact v1. Retry produces the exact two-entry v2 result regardless of partial/complete orphan candidates. |
| Terminate at selector replacement or after replacement before return. | Selector is intact old or new JSON. Old implies retry from v1; new implies validate/return v2. Both paths end with exactly `theme` and `timeout`, no duplication, original bytes unchanged. |
| Repeat migration after success. | Validate and return the same active settings; selector and active target unchanged, no additional candidate. |
| Disk full, write/fsync/replace error. | Before replacement, v1 stays active; after replacement, report uncertain completion and retry from selector. Original remains readable throughout. |
| Selector format disagrees with payload, selected file missing, or active v2 corrupt. | Explicit error; no inferred fallback, no activation or destructive repair. |

## Open decisions and validation

Design review remains pending for the stricter migration input domain (string IDs,
standard JSON values, unknown-field rejection), selector path restrictions, caller
API, exclusive-writer assumption, retained-orphan policy, and deployment crash /
durability expectations. These are concrete proposals; none is confirmed by a
review or hidden assumption about existing callers. If numeric IDs must migrate,
the required v2 object representation needs an explicit encoding contract first.

Future validation combines existing regressions, independent expected v2 values,
malformed-input checks, deterministic I/O failure injection, and child-process
termination at persistence boundaries followed by fresh-process retry. Assert
original bytes and readability, selector integrity, exact IDs/types/values, and
idempotence. Unit failure injection alone cannot establish process-crash behavior;
process termination alone cannot establish power-loss durability.
