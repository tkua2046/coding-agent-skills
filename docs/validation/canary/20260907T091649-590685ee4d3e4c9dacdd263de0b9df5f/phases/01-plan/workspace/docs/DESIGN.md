# Design: settings v2 migration

Status: proposed; design review pending. Authority: [original requirement](ORIGINAL.md),
with proposed contract details in [SPEC.md](SPEC.md). No implementation is authorized
in this phase. The [plan](PLAN.md) also awaits its separate review.

Preserve the original v1 file and construct a complete v2 file before atomically
switching `active.json`. This costs temporary disk space but keeps v1 usable across
interruption; retry rebuilds a whole snapshot instead of appending entries.
The next action is design review, especially the compatibility and durability
decisions below, followed by plan review. Separate documents are warranted because
activation changes persistent state and has consequential failure boundaries.

Outline: [baseline](#baseline), [choices](#choices), [protocol](#protocol),
[validation and open decisions](#validation-and-open-decisions).

## Baseline

`settings.load(path)` reads v1 and returns a dictionary, rejecting duplicate IDs.
It neither reads `active.json` nor performs migration. The existing design states
that the caller reads the marker. The fixture selects `settings-v1.json` with
`format: 1`; its entries are `theme = "dark"` and `timeout = 30`.
Two tests verify that mapping and duplicate-ID rejection. Neither exercises
activation, v2, malformed data, or interruption. See [inspection and probe evidence](evidence/migration-baseline.md).

Historical baseline, retained from the preceding design:
> The caller reads data/active.json and loads the selected v1 file. Stable IDs are
> unique; duplicate IDs are errors. No migration or recovery protocol exists yet.

## Choices

| Proposed decision | Reason and credible alternative | Consequence/example |
|---|---|---|
| Immutable source, complete replacement snapshot | In-place rewriting risks losing the usable source; a journal adds recovery states unnecessary for this small fixture. | Never truncate, rename, delete, or rewrite the v1 source, even after success. Disk must accommodate both versions and staging files. |
| Keep `active.json` as the only activation authority | Inferring activation from a v2 file's existence would expose an orphan after a crash. | A complete `settings-v2.json` plus a v1 marker still means v1. |
| Explicit migration; dual-format reader | Migrating during `load` would turn reads into writes and obscure errors. | Preserve `load(path)` returning an ID/value mapping; add proposed `load_active(active_path)` and `migrate(active_path)` entrypoints. See SPEC for semantics. |
| Validate the complete candidate against the source before activation | Counts alone cannot detect an ID substitution or value corruption. | Exact ID set and type-aware JSON value equality are required; `30` must not silently become `"30"` or `true`. |
| Reject ambiguous or unrepresentable source data | v2 JSON object keys cannot faithfully represent arbitrary v1 IDs. Stringifying IDs can merge numeric `1` and string `"1"`. | Proposed migration preflight rejects non-string IDs and duplicate JSON keys before dictionary construction; this is a compatibility decision awaiting review. Existing direct v1 reads retain their behavior. |
| Single writer, quiescent settings during migration | Multi-process coordination is excluded by the original request; snapshots of concurrent edits need additional coordination. | Caller must serialize migration and source/marker writes, including threads. This assumption needs review if live writes are expected. |

## Protocol

The proposed fixture destination is `settings-v2.json`, beside `active.json`.
Marker paths resolve relative to the marker directory, not the working directory.
Require supported marker format and matching selected-file version. Reserve the
destination for migration; reject a source/destination alias, symlinked mutation
targets, or paths outside that directory. No generalized storage framework or new
dependency is needed.

1. Read the marker. If it already selects v2, strictly validate that selected file
   and return success without rewriting anything. An invalid selected v2 fails
   explicitly; do not silently fall back or overwrite it.
2. If it selects v1, strictly parse and validate the complete source before any
   mutation. Keep its bytes unchanged. Build the candidate with the same unique
   string IDs and JSON values. An error leaves the v1 selection unchanged.
3. Write a uniquely named temporary file in the destination directory. Flush and
   `fsync` it, close it, reopen it, and validate both v2 structure and semantic
   equivalence to the validated source. On failure, never change the marker.
4. Replace the inactive `settings-v2.json` with the validated candidate using a
   same-directory atomic replacement; sync the directory. It is safe to replace
   an orphan destination only while the marker selects v1. Treat directory-sync
   failure here as a preactivation failure.
5. Write a separate temporary marker containing exactly
   `{"format":2,"path":"settings-v2.json"}`; flush, sync, and close it. Atomically
   replace `active.json`, then sync its directory. Only now acknowledge success.
   Never delete the marker before replacement. The caller reloads the marker via
   the validated reader; it must not cache a speculative v2 selection.

Marker replacement is the logical commit point. A process crash before it leaves
v1 active; a process crash after it can leave v2 active even if success was never
returned. That is safe because validation and destination publication preceded
the switch, and the original v1 still exists. If the final directory sync fails,
report an indeterminate commit outcome, retain both files, and reconcile by
reading/validating the marker on retry. Do not roll back an already visible marker.
“Only after successful validation” governs activation, not receipt of the success
response, which cannot be atomic with a disk write.

Retry with v1 selected validates the source and creates a fresh snapshot; it never
merges or appends an old candidate. Ignore leftover temporary files. The future
implementation may remove only its own known temporary files on normal failure;
automated sweeping and source cleanup are outside this migration. Retry with valid
v2 selected is a no-op. This makes a lost success response safe.

## Validation and open decisions

The decisive [acceptance examples](SPEC.md#acceptance-examples) are the behavioral
oracle. Future tests should inject failures at write, sync, validation and replace
boundaries and kill a subprocess on both sides of marker replacement. Always check
the original source byte-for-byte, selected-reader output, and repeated retries.
Use temporary fixture copies; do not migrate checked-in data during tests.

The local probe verified that file sync, same-directory replacement and directory
sync are callable in this environment. It did **not** establish persistence under
power loss. Process-crash safety is the proposed minimum acceptance; the write/sync
ordering is also intended for durable local filesystems. Design review must settle
whether “crash” additionally requires power-loss guarantees on named platforms.
If so, implementation must first establish the relevant filesystem/OS guarantees
(including whether stronger synchronization is needed) and extend acceptance.
Do not claim universal durability from this probe or from mocked failures.

Other review decisions: approve string-only migration IDs, strict migration JSON
validation, the quiescent-writer prerequisite, the proposed public entrypoints and
destination ownership. These are proposals, not new confirmed user requirements.
If broader v1 IDs must migrate, the mandated v2 object shape needs clarification;
lossy key conversion is not an acceptable fallback. No design or plan review has
been performed in this phase.
