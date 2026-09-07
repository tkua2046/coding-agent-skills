# Design: source-preserving settings migration

Status: proposed; **design review pending**. Implementation is deferred.
Authority: [original requirement](ORIGINAL.md); proposed behavior and acceptance:
[migration contract](SPEC.md). Next: review the decisions below, then review the
[delivery plan](PLAN.md). Neither requested review has been performed.

Keep v1 untouched, create and validate a separate v2 file, then atomically replace
the active selector. Retry follows the selector, never partial output. The cost is
temporary space and retained unselected files. Separate design and plan documents
are warranted because preservation, activation durability and compatibility are
consequential choices.

Outline: [baseline](#current-behavior), [decisions](#decisions),
[protocol](#publication-and-recovery), [validation](#validation-and-review-boundaries).

## Current behavior

`settings.py` exposes only `load(path)`: it parses v1, rejects duplicate IDs and
returns a dictionary. Two tests cover the normal and duplicate fixtures.
`data/active.json` selects `settings-v1.json` with format 1. The earlier design
describes a caller reading this selector, but no caller or selector reader is
implemented in the fixture. No migration or recovery implementation exists.

[Local evidence](evidence/migration-baseline.md) records passing baseline tests and
bounded probes: numeric IDs load but become strings in a naive v2 roundtrip;
repeated JSON members and NaN also load. Migration therefore cannot rely on the
legacy reader alone to establish lossless conversion.

## Decisions

All choices below are proposed, not approved requirements.

| Choice | Reason / credible alternative | Consequence/example |
|---|---|---|
| Separate v2 file; never rewrite v1 | In-place conversion risks the only usable source. Backup-and-overwrite adds recovery states. | Half a destination leaves original theme `dark` readable; extra space is needed. |
| Selector replacement is the activation commit point | Publishing the target alone must not switch callers. A transaction journal adds unnecessary state for one selector and one migrator. | A crash after replacement but before return is committed activation, discoverable on retry. |
| Exclusively create a unique destination beside the selector | A fixed destination name requires collision/ownership rules and may overwrite a reader's target. | Name may be `settings-v2-<unique>.json`; orphan files can accumulate but mapping entries cannot duplicate. Cleanup is deferred. |
| Rebuild from unchanged v1 on uncommitted retry | Resuming partial entries needs bookkeeping and invites drops/duplicates. | Retry after writing only theme reconstructs both theme and timeout. |
| Validate persisted bytes against validated source | Validating only the conversion misses serialization and I/O damage. | Exact key set and recursively typed values must match after reopening the target. |
| Strict migration JSON and string IDs | JSON keys cannot preserve numeric ID types; permissive decoding loses repeated members. | Reject numeric `7` and ambiguous input; preserve legacy direct v1 compatibility. |
| Explicit migration, selector-aware loading | Hidden migration would turn ordinary reads into writes. | Caller explicitly invokes migration; active loading checks format agreement. API proposals are in SPEC. |

## Publication and recovery

Migration owns its new output and selector staging files and the final selector
replacement. It never changes the source. The caller serializes source edits and
migration; multi-process coordination is out of scope. Readers holding an old
selector can still load its retained target.

1. Read the selector once and resolve its target relative to the selector directory.
   Enforce format/version agreement. Already-v2 means strictly validate and return
   without writes; invalid selected data is an error, not implicit rollback.
2. Strictly validate all v1 input and construct the complete mapping. No source
   writes, appending or coercion. Reject invalid input before creating output.
3. Exclusively create a unique v2 file in the selector directory. Write strict JSON,
   flush and fsync, close, reopen, strictly decode and compare against the source's
   complete key set and typed values. Sync the directory so the destination filename
   is durable before publishing a reference to it. Partial output stays unselected.
4. Write a unique selector staging file in that same directory, containing format 2
   and the destination's relative path. Flush and fsync, then reopen and validate its
   exact intended contents. Use `os.replace` to atomically replace `active.json`, and
   fsync the parent directory before reporting normal success.
5. Return the validated mapping. Retain original v1 and all previously selected
   targets. Best-effort cleanup can remove this invocation's selector staging file,
   but never mask the original error or delete a selected destination.

| Last reached state | Reader after process restart | Retry |
|---|---|---|
| Input validation or partial destination | Original v1 | Rebuild from v1; ignore orphan output. |
| Complete destination; selector not replaced | Original v1 | Rebuild; file existence alone is not evidence of validation. |
| Selector replaced; return not delivered | Valid v2 | Validate selected v2 and return without rewriting. |

Do not roll back a successful selector replacement because later sync or return
fails. If final directory sync fails, surface the I/O error and report uncertain
activation to the caller, who must reread and validate the selector before further
use/retry. No separate success flag is necessary: the selected valid representation
is the commit record. Pre-replacement failures leave v1 selected; later failures can
leave v2 selected, always after full target validation. Original v1 remains usable
in either case. A7 separates committed activation from a delivered success response.

## Validation and review boundaries

[A1–A8](SPEC.md#decisive-acceptance-examples) specify hand-derived acceptance. Future
checks must inspect source bytes, selector state, typed value equality and retry,
not only return values. Inject write, flush/fsync, validation and replace failures.
Subprocess tests must terminate at publication boundaries and inspect recovery in a
fresh process; catching simulated exceptions alone does not demonstrate crash recovery.

The proposed platform is a local filesystem supporting same-directory atomic replace
and file/directory fsync. For process crashes, an old selector retains v1 and a new
selector names an already validated target. For power loss, the intended ordering
is durable target and directory, durable selector staging, replacement, then directory
sync. Recovery may see the old or new selector, each with a usable target. This
session has not verified filesystem durability guarantees or power-loss behavior.
Confirm deployment guarantees and the required crash model before claiming that
coverage; fail before publication when required sync operations are unsupported.
Network filesystems and stronger hardware durability are outside verified evidence.

Review must settle strict migration input handling, serialized source writes, API,
commit-point semantics and durability/platform scope. The existing tests and input
probes are verified; new APIs, protocol and acceptance are unimplemented. Design
review, plan review and later implementation authorization remain pending.

## Preserved prior design

Original `docs/DESIGN.md` text before this drafting phase:

> # Current design
> The caller reads data/active.json and loads the selected v1 file. Stable IDs are
> unique; duplicate IDs are errors. No migration or recovery protocol exists yet.
