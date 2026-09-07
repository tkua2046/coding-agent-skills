# Design: recoverable settings migration

Status: proposed; design review pending. Implementation is deferred. Authority:
[ORIGINAL](ORIGINAL.md); proposed behavior clarifications: [SPEC](SPEC.md).

Publish and validate a complete v2 file before atomically replacing `active.json`.
Retain the original v1 indefinitely. This preserves recovery at the cost of a
second file. Deploy a dual-version reader before activation. Retry consults the
selector, including when activation succeeded but the previous call never returned.
Next: resolve pending design choices, then review [PLAN](PLAN.md). Neither review
has been performed.

Contents: [baseline](#baseline), [choices](#consequential-choices),
[protocol](#publication-and-recovery), [validation](#validation-and-open-decisions).

## Baseline

`settings.load(path)` reads a supplied v1 file, rejects duplicate IDs and returns
an ID/value dictionary. Two tests cover ordinary loading and duplicate rejection.
There is no implemented selector reader or migration. The fixture selector names
`settings-v1.json` with format 1. [Local evidence](evidence/migration-baseline.md)
shows numeric IDs currently load but become strings as JSON object keys; default
JSON parsing silently collapses repeated object members.

Historical design retained verbatim:

> The caller reads data/active.json and loads the selected v1 file. Stable IDs are
> unique; duplicate IDs are errors. No migration or recovery protocol exists yet.

## Consequential choices

All choices below are proposed, not approved.

| Choice | Reason, alternative and consequence |
|---|---|
| Extend `load(path)` for v2; add `load_active(selector_path)` and `migrate(selector_path)` | No caller implementation exists here. Explicit selector APIs make the switch testable. Resolve relative paths against the selector directory. Migration returns the validated mapping. |
| Migrate unique string IDs only; retain legacy direct v1 reader compatibility | Coercing numeric ID `7` to `"7"` changes identity and can collide. Reject unsupported inputs without mutation; an alternative v2 encoding would change the requested format. Needs review. |
| Strict migration/selector/v2 parsing | Reject duplicate JSON member names before parsing loses them, non-finite numbers and malformed structures. Ordinary v1 direct loading retains compatibility. Preserve nested JSON values and types, not formatting or object order. |
| Compare persisted output with the entire source mapping | Version/count checks miss a changed timeout. Compare exact keys and recursive JSON values with boolean/number distinction. |
| Stage both files beside the selector; publish target before selector | In-place v1 rewriting risks the only usable copy. Same-filesystem atomic rename plus file/directory sync gives an ordered commit protocol without new dependencies. |
| Reserve `settings-v2.json`; reuse only an exactly matching validated target | Fixed naming makes retry discoverable without a journal. Fail on divergent or unrelated existing output; never overwrite it. Reject source/target aliasing. |
| Retain source; no automatic rollback or deletion | A corrupt selected v2 must produce an error rather than hide damage through fallback. Explicit recovery remains possible from retained v1. |

## Publication and recovery

Assume one migrating/writing actor: source and selector stay unchanged by other
writers throughout migration. Read-only callers may continue. Initial support
is ordinary local files, with symlinks and non-regular selected files rejected
before mutation. The filesystem must support atomic replacement and file/directory
sync. Multi-process migration is excluded by the original requirement.

1. Strictly read the selector once and require selected format/version agreement.
   If it already selects valid v2, return its mapping without writes. Missing or
   corrupt active v2 is an error, never an implicit rollback.
2. Strictly validate selected v1, including unique string IDs, before any writes.
   Build the expected complete v2 mapping in memory. Never modify source bytes.
3. If the reserved target exists, validate it against the source and fail on any
   difference. Otherwise write a uniquely named temporary target in the selector
   directory, flush/fsync, reopen, and validate all persisted content against the
   source. Rename to the final target and sync the directory. Reused targets must
   also be validated and synced before activation.
4. Write a unique temporary selector containing
   `{"format":2,"path":"settings-v2.json"}`. Flush/fsync and reopen to validate;
   atomically replace `active.json`, then sync its directory before returning.
   Callers use one selector snapshot and check the selected version. Target
   existence alone never signals activation.
5. Before selector replacement, failures leave v1 selected. Remove only this
   invocation's temporary files when possible. Retry ignores orphan temporaries,
   rebuilds from v1 and reuses only matching validated final output. Do not append
   entries or glob-delete unknown files.

Selector replacement is the logical commit point. Failure of the subsequent
directory sync, or a crash before returning, means completion is uncertain even
though activation may have occurred. Report that distinction; do not roll back.
Retry inspects and validates the selector and succeeds for active valid v2.
The original remains independently readable in every window. An error does not
promise no activation; activation always follows complete target validation.

## Validation and open decisions

Future tests must exercise [decisive examples](SPEC.md#decisive-acceptance-examples)
with isolated directories, source byte comparisons, injected I/O failures and
fresh-process reading/retry after interruption at each publication boundary.
These tests establish protocol behavior, not physical power-loss guarantees.
The local probe established replacement and directory fsync availability only.

Review must resolve string-only migration eligibility, the proposed public API,
fixed-target collision policy, exclusive writer coordination and supported
platform/storage guarantees. Proposed crash scope includes process interruption;
host/power-crash durability is conditional on storage honoring atomic rename and
file/directory fsync. If broader unconditional durability is required, validate
the target platform and revise this design before implementation. No review,
external research or destructive crash experiment occurred in this phase.
