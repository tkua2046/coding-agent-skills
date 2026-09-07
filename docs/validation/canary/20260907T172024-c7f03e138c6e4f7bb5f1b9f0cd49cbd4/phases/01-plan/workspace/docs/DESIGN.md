# Settings migration design

Propose writing a separate v2 file, validating it against the complete v1 mapping,
then atomically replacing `active.json`. Preserve the v1 file indefinitely. This
costs an extra copy but gives one activation point and a safe retry: interruption
after writing v2 leaves v1 selected; retry validates and reuses that output.
For the supplied source, the result is
`{"version":2,"settings":{"theme":"dark","timeout":30}}`.

Decision status: proposed, awaiting the requested design review. The original
[requirement](ORIGINAL.md) remains authoritative; the [proposed specification](SPEC.md)
defines detailed behavior. Delivery and review status live in [PLAN.md](PLAN.md).
The prior design is preserved [verbatim](history/DESIGN.before-migration.md).

## Verified starting point

`settings.load(path)` requires version 1, rejects duplicate entry IDs and returns
an ID/value dictionary. The valid fixture contains string IDs `theme` and `timeout`;
the other fixture repeats `theme`. `active.json` selects `settings-v1.json` with
format 1. No actual caller, pointer reader, writer or recovery code exists in this
fixture, despite the prior design describing a caller. The two tests cover v1
success and duplicate IDs only. See [local evidence](EVIDENCE.md).

## Consequential decisions proposed for review

**Representation.** IDs become JSON object keys. Require string IDs for migration
and preserve them exactly; reject duplicates rather than coercing keys or selecting
a winning value. The old reader's permissiveness does not establish a lossless v2
encoding for non-string IDs. Those sources fail safely and remain available through
v1. Accept finite JSON values, including nested values. Reject nonstandard NaN and
Infinity and duplicate JSON members rather than silently losing information.
Compare the full ID set and values recursively with matching JSON scalar types
(for example, `true` must not validate as `1`). Whitespace and object order are
irrelevant. Preservation is semantic, not preservation of textual number spelling.

**Compatibility and caller.** Extend `load(path)` to read both versions; add
`load_active(active_path)` and `migrate(active_path)` in the existing module.
Preserve the returned mapping and existing valid-v1/duplicate-ID behavior. The
active reader checks selector format against file version. Migration returns the
validated mapping only after publication finishes. There is no CLI or application
caller to update in this fixture; README examples will establish the caller path.
Strict migration validation can remain separate from permissive legacy direct-v1
reading where tightening it would be unrelated to this task.

**Publication.** Use a fixed sibling destination `settings-v2.json`, a unique
scratch output and a scratch selector on the same local filesystem. Never mutate,
rename or delete v1. Reject any destination alias to the source or selector. A
matching existing destination can be reused after full source comparison; a
conflicting or corrupt destination blocks activation and is preserved. This avoids
overwriting unrelated data but requires explicit operator resolution of conflicts.

Write, flush and fsync the candidate, close/reopen it, then validate schema and full
mapping. Publish it by same-directory replacement only when the destination is
absent under the single-writer assumption; fsync the directory. For reuse, validate
and sync the destination and directory instead. Only afterward write, flush and
fsync the new selector, replace `active.json`, and fsync its directory. Read the
selected result before returning success. In-place source conversion risks losing
the only usable original; separate non-atomic edits to selector format/path risk
a mismatched pointer. Neither is acceptable.

**Commit and retry.** The caller adopts the mapping only on successful return.
Selector replacement is the persistent commit point: a process can die after it
but before returning success. Restart may therefore find validated v2 already
selected. Retry validates that active v2, finishes synchronization and returns
success without regenerating entries. The v1 source still remains usable. Persistent
activation and delivery of a success response cannot be simultaneous; this
interpretation of the requirement awaits design review. An I/O error after selector
replacement is uncertain completion: inspect/retry, never blindly roll back.
Selector state and validation determine recovery; no journal is needed.

**Supported crash boundary.** Single-process migration, with no concurrent source,
selector or destination writers, on a local filesystem supporting atomic replacement
and file/directory synchronization. The input source and selector must already be
durably stored; migration cannot recover pre-existing corruption. Process interruption is in scope; power-loss
durability relies on storage honoring these operations. The local probe established
that these calls work here, not a universal durability guarantee. Do not claim
network-filesystem or arbitrary-platform support. Sync failures are errors, not
silently weakened success. This boundary needs confirmation in the pending review;
implementation must not proceed if the required deployment cannot meet it.

## Acceptance and operational consequences

The [acceptance examples](SPEC.md#acceptance-examples) cover exact values, collisions,
failures on both sides of activation and repeat migration. Readers take one selector
snapshot and load that immutable file; an old snapshot remains usable during
activation because v1 is retained. Invalid selectors or files fail closed instead
of guessing a fallback that might conceal corruption and select stale settings.
Scratch files never determine active state and may be explicitly removed when no
migration is running. Automatic deletion of sources or conflicting destinations,
automatic rollback, and post-migration settings writes are outside this migration.
