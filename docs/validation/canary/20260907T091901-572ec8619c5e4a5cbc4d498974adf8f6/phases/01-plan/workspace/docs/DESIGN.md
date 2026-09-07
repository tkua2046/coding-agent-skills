# Design: v1 to v2 settings migration

Status: proposed; design review pending. Authority: [original requirement](ORIGINAL.md), preserved unchanged.

Outcome: preserve every stable ID and value while moving entries into the v2
`settings` object. Main choice: retain v1, publish a validated separate v2 file,
then atomically replace the active selector. This needs additional disk space,
but an interrupted attempt leaves v1 usable. For example, interruption before
selector replacement leaves `theme=dark` and `timeout=30` selected from v1.
Implementation is deferred. Next: resolve the open contract decisions below and
complete the requested design review; the [plan](PLAN.md) is provisional.

Outline: [baseline](#baseline-and-compatibility), [choices](#decisions-and-consequences),
[protocol](#state-and-failure-protocol), [acceptance](#decisive-acceptance),
[open decisions](#validation-and-open-decisions).

## Baseline and compatibility

Historical design, retained verbatim:

> The caller reads data/active.json and loads the selected v1 file. Stable IDs are
> unique; duplicate IDs are errors. No migration or recovery protocol exists yet.

Inspection: `settings.load(path)` checks version 1, rejects duplicate entry IDs,
and returns an ID-to-value dictionary. It does not implement selector resolution,
migration, or strict schema validation. The historical caller behavior is context,
not an implemented caller found in this fixture. `active.json` selects format 1
and `settings-v1.json`. The valid data yields `{"theme":"dark","timeout":30}`;
the duplicate fixture repeats `theme`. Both existing tests passed; see
[local evidence](evidence/migration-planning-baseline-2026-09-07.md).

Proposed interfaces in `settings.py`: retain `load(path)` and its dictionary
result, extend it to v2, add `load_active(selector_path)` and
`migrate(selector_path)`. Resolve selected paths relative to the selector's
directory, never the process working directory; require the selected version to
match `format`. Migration returns the same dictionary only after activation;
an already-active valid v2 returns it without writing. These API names and error
details are proposals, not existing usage. Semantic/schema errors use `ValueError`,
I/O failures propagate `OSError`; no silent fallback on a corrupt selector.
README remains the owner of runnable usage, updated when these APIs exist.

## Decisions and consequences

| Decision | Reason / credible alternative | Consequence | Example |
|---|---|---|---|
| Store IDs as v2 object keys, retain typed JSON values | Matches the required shape; a v2 entries array would change it | Requires string IDs and unique keys; never silently stringify or overwrite IDs | `timeout` remains numeric `30`, not `"30"` |
| Preserve source bytes; write a separate destination | In-place rewriting can destroy the only usable source | Additional space and retained legacy data; deletion is outside this migration | A failed candidate write leaves v1 byte-identical |
| Validate source before conversion and persisted candidate before activation | Successful serialization alone does not prove preservation | Reject invalid schemas, duplicate IDs/JSON keys, unsupported versions and mismatches before switching | Two `theme` entries fail rather than choosing one |
| Atomically replace only the selector as the activation point | Updating selector and data in place exposes mixed states | Requires atomic same-filesystem replacement and ordered persistence; caller reads one selector snapshot | Selector names either valid v1 or complete v2 |
| Use a fresh exclusively created candidate per attempt | Reusing a fixed destination risks overwriting unrelated data or trusting stale output | Orphans can remain after interruption; retry never merges or appends entries | Stale candidate does not add a second `theme` |
| Treat validated, already-active v2 as successful retry | The process can crash after switching but before returning | Success is defined by durable active state, not delivery of the return value | Retry after lost acknowledgement returns the existing map |

## State and failure protocol

`active.json` owns selection, each selected document owns its settings, and the
migrator owns only its newly created candidate and selector temporary file.
Assume no concurrent migration or settings edits during migration; concurrent
readers may hold a selector snapshot since selected files remain available.
No automatic cleanup, rollback, or source retirement is included.

1. Read and validate a selector snapshot and selected source. Format 1 must select
   valid v1. A format 2 selection must load valid v2 and is a no-write success.
   A malformed, missing, or mismatched selection fails without repairing it.
2. Validate the entire v1 source before constructing a one-to-one dictionary.
   Under the proposed domain, IDs are strings and values are JSON null, boolean,
   finite number, string, array, or object. Preserve nested types and contents;
   equality must distinguish boolean from number. Ordering, whitespace, and number
   spelling are not preserved. Empty entries map to an empty object.
3. Exclusively create a fresh candidate in the selector directory, avoiding the
   source and selector paths. Write `{"version":2,"settings":...}`, flush and
   synchronize the file, then close and reopen it. Strictly validate the bytes as
   v2 and compare its ID set and typed values against the validated source.
   Persist the candidate directory entry before proceeding. Never activate a
   merely parseable but incomplete or altered dictionary.
4. Write a temporary selector in the same directory with `format: 2` and the
   candidate's relative path; flush/synchronize it. Atomically replace `active.json`
   and synchronize its directory. Return success only after the required steps.
   Publication must follow candidate validation and persistence.
5. Before replacement, any failure leaves the active v1 selector and original
   bytes intact. After replacement, failure or interruption can mean activation
   happened without a success return: report the I/O failure without claiming a
   rollback. Re-read on retry. A visible old selector starts a fresh conversion;
   a visible new selector validates v2 and returns without writes. V1 remains
   intact in both cases. Never choose candidates by filename or recency.

Atomic replacement is the logical commit point; directory synchronization is the
proposed durability completion point. Process interruption leaves a complete old
or new selector under the stated filesystem assumption. Power-loss behavior needs
the platform decision below; atomic rename alone is not a power-loss guarantee.

## Decisive acceptance

These expected outcomes are derived from the requirement, not yet implemented
or verified. Paths for generated candidates may vary; selected contents may not.

| Case / explicit input or interruption | Expected output and persistent state |
|---|---|
| Supplied valid v1 and active selector | Migration returns `{"theme":"dark","timeout":30}`; selected file parses exactly as `{"version":2,"settings":{"theme":"dark","timeout":30}}`; selector format is 2; original v1 bytes unchanged |
| Supplied duplicate-ID v1 selected | `ValueError`; selector and source unchanged; no v2 activation |
| Entries `[{"id":"01","value":false},{"id":"1","value":{"x":[null,30,"30"]}}]` | Two distinct keys `"01"` and `"1"`; boolean, null, number and string retained recursively |
| Empty entries | Selected v2 has `"settings":{}`; no invented defaults |
| Non-string ID, duplicate JSON key, nonfinite number, wrong shape/version, or selector/version mismatch | Reject under proposed validation policy; no activation or source mutation |
| Candidate reopens with `timeout: "30"`, missing `theme`, or an extra key | Validation fails despite valid JSON; active selector still names original v1 |
| Disk full during candidate or selector-temporary write | I/O error; v1 bytes and active selector unchanged and readable |
| Interrupt after candidate write, after validation, or just before selector replacement | v1 remains selected and usable; retry yields exactly the two supplied entries in selected v2; leftover candidates do not affect results |
| Interrupt immediately after selector replacement, before return | New selection is complete validated v2; retry succeeds without changing it or duplicating entries; v1 still usable directly |
| Directory synchronization fails after replacement | Report failure with activation outcome uncertain; re-read/retry follows whichever valid selector is visible; do not overwrite it blindly |
| Start from valid active v2 and run migration twice | Both calls return the same map; selected path and file bytes unchanged |
| Reader launched from a different working directory | `load_active` resolves the selected relative path against the supplied selector directory and returns the same map |

## Validation and open decisions

Confirmed: required v2 shape, stable ID/value preservation, usable original before
completion including crashes, safe retry, validation before switching, selector
ownership, and no requirement for multiprocess migration. The source requirement
does not define the complete input domain or filesystem durability contract.

Pending design-review decisions (proposed defaults above are not confirmed):

- **ID/value domain and metadata:** require string IDs and finite standard JSON
  values, reject unknown schema fields to avoid silent metadata loss. The old
  reader accepts some numeric IDs and ignores extra fields; object keys cannot
  preserve numeric ID identity. If such inputs must migrate, a representation or
  explicit conversion contract must be agreed before execution.
- **Crash scope and platform:** target local filesystems supporting atomic replace,
  file synchronization and directory synchronization; include power-loss ordering
  only with confirmed platform guarantees. Decide whether process-crash recovery
  suffices. Unsupported persistence operations must fail explicitly; do not promise
  durability based on injected exceptions alone.
- **Completion and writers:** confirm activation as committed state even if return
  is lost, and absence of concurrent source edits. Supporting writers would need
  coordination beyond the current no-multiprocess migration scope.

Future validation combines schema/compatibility tests, injected I/O failures and
subprocess interruption at publication boundaries, plus real filesystem checks
on the agreed platform. Power-loss durability cannot be established by unit tests.
Design and plan reviews remain pending; no review reports are generated in this
phase. Existing baseline checks establish only current v1 behavior.
