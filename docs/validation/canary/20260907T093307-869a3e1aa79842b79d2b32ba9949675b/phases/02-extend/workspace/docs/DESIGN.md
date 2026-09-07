# Design: YAML initialization and fixed occupied cells

Status: YAML and occupied-cell scope confirmed; extension proposed, implementation
and reviews pending. D1 remains accepted. Load and validate the entire YAML input
before exposing a starting pose and immutable occupancy; reuse a hash lookup during
movement. At about 200,000 cells this trades memory for expected O(1) queries and
avoids repeated parsing or scans. Next: resolve the [open contracts](#open-contract-decisions),
then deliver the revised [pending plan](PLAN.md). No YAML dependency is selected or installed.

Sources and behavior: [current spec](SPEC.md), [YAML request](YAML_REQUEST.md),
[occupied request](OCCUPIED_REQUEST.md), and [example](../examples/start.yaml).
Sections below cover preserved behavior, loading/lookup rationale, open contracts,
and acceptance. The earlier per-run copy proposal is revised for reusable loaded
occupancy; its malformed-input exclusion no longer applies to YAML initialization.

## Accepted design D1 (preserved)

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Movement and compatibility

Inspection of [navigator.py](../navigator.py) shows `_target` already computes a
candidate pose without mutation. For F, check its coordinates before replacing
pose. A blocked move appends False and continues; accepted F and L/R append True.
Unknown commands still raise `ValueError("unknown command")`.

Propose retaining `run(pose, commands, occupied=())`: old two-argument calls retain
existing behavior. Mutable or one-pass caller collections are normalized once
before command consumption; later caller mutations cannot affect movement.
Loader-produced immutable occupancy is reused directly, including across runs,
rather than rebuilt for each run. Direct malformed Python input guarantees remain
outside the YAML contract; this is not an invitation to let malformed YAML through.

## Loading, validation, and ownership

Proposed boundary: `load_start(path)` returns `(pose, occupied)` after successful
validation, with pose a tuple and occupied a `frozenset` of coordinate tuples.
Commands remain supplied separately to `run`; no CLI or global session is needed.
An explicit load followed by runs makes load-once ownership clear: changing or
removing the source file afterward cannot change the active occupancy. Reloading
requires a new explicit load; automatic reload and caches are unnecessary.

Read one YAML document, parse safely, validate all structure and agreed values,
then publish the complete result. Never yield a partial configuration or consume
commands while validating. Required shape follows the example: root mapping;
required `pose` mapping with `x`, `y`, `heading`; required `occupied` sequence;
each cell a sequence of exactly two coordinates. Empty occupancy is valid; a null
root, missing pose, scalar occupancy, or three-element cell is a startup error.
In particular, an invalid final cell after 199,999 valid cells must leave no
usable partial result and no commands consumed, even if the first move is clear.

Propose one public configuration-error category carrying source path and a useful
field/index, for example `start.yaml: occupied[199999]: expected two coordinates`.
Syntax failures should include parser line/column when available; missing-file and
read failures should name the source and reason. Do not silently substitute an
empty board, coerce malformed entries, or fall back to another parser. Validation
also runs when there are no commands. Ordinary command errors remain separate.

Safe parsing and schema validation are both necessary: safe parsing prevents
arbitrary object construction but does not establish the navigator's schema or
preserve duplicate keys automatically. Select a parser/configuration that can
report repeated mapping keys before they are overwritten if that policy is agreed.
Reject custom object tags; propose a single document with primitive schema values.
Alias handling and duplicate semantics are still [open](#open-contract-decisions).

For n entries and u unique cells, conversion/lookup construction takes expected
O(n) time and O(u) retained occupancy space; YAML parsing also depends on input
byte size. Movement membership is expected O(1), not a worst-case constant-time
guarantee. Scanning 200,000 entries on each F makes command cost scale with map
size. A dense grid conflicts with unbounded sparse coordinates; an index service
or database is unnecessary for the requested in-memory use.

Peak load memory includes source/parser objects, the parsed cell list, and the
final set, so retained set size alone understates the requirement. Drop temporary
parse data after validation. Begin with a normal safe parser and immutable set;
measure loading time and peak/retained memory at the requested scale before
considering streaming complexity. No memory or latency budget has been supplied,
and current evidence does not establish parser throughput or memory feasibility
on a target deployment. Movement must do no YAML I/O and no map-sized copy per F.

## Open contract decisions

These recommendations remain proposals, not approved policy. Questions have been
raised with the user; silence does not settle them.

| Decision | Proposed default and consequential example | Alternative / impact |
|---|---|---|
| Values and keys | Strict integer coordinates excluding booleans, heading 0–3; reject unknown keys. Reject `x: "1"`, `x: true`, `heading: 4`, and misspelled `headng`. Negative coordinates remain valid. | Coercion or ignored keys accepts more input but can conceal mistakes; heading wrapping would add new startup semantics. |
| Duplicates | Reject repeated YAML mapping keys; collapse repeated cells such as `[[0, 1], [0, 1]]` into one occupied location. | Last-key-wins can silently change the pose; rejecting repeated cells instead makes the same board fail. Parser choice must support the agreed policy. |
| YAML features | One document, safe primitive schema; allow aliases only if their resolved values satisfy the same shape and reject cyclic structures. No custom object tags. | Rejecting all aliases or accepting multiple documents changes which files work; do not assume a parser's defaults define the public contract. Resource limits, if needed, need a concrete budget. |
| Initial occupied pose | Allow turns and departure from an occupied start, block re-entry. Example `(0,0,0)` with `(0,0)` occupied may move north. | Reject initialization instead; earlier design proposed allowance but it was never confirmed. |
| Public loading interface | `load_start(path)` returning reusable pose/occupancy; commands stay external. Errors have a stable configuration category with source/location context. | Stream/text input or a one-call runner changes ownership and public API; confirm before exposing it. |
| Parser dependency | Prefer a maintained safe YAML library; select/version it during authorized implementation after policy resolution. | [DEVNOTES](../DEVNOTES.md) currently says standard library only; Python has no standard YAML parser. A custom subset parser would narrow YAML compatibility and add maintenance cost. Resolve this conflict before loader implementation. |

## Acceptance and compatibility

Hand-derived expectations for future tests; none demonstrates implemented support.
Headings are north=0, east=1, south=2, west=3.

| Input / action | Expected state or error |
|---|---|
| Load `examples/start.yaml`, run `FRF` | `((1, 0, 1), [False, True, True])`; north destination is blocked, turn east, move east. |
| `(0,0,1)`, `{(1,0)}`, `FFLF` | `((0,1,0), [False, False, True, True])`; repeated failure preserves pose and permits later commands. |
| `(0,0,0)`, omitted/empty occupancy, `RF` | `((1,0,1), [True, True])`; existing callers still work. |
| `(0,0,3)`, `{(-1,0)}`, `F` | `((0,0,3), [False])`; negative coordinates work. |
| `(0,0,1)`, `{(0,0)}`, `FRRF` | Proposed: `((1,0,3), [True, True, True, False])`; contingent on initial-occupancy answer. |
| `(0,0,1)`, `{(1,0)}`, `F?` | `ValueError("unknown command")`; blocking does not hide later command errors. |
| Root `[]`, missing `pose`, `occupied: 7`, or cell `[2,3,4]` | Clear configuration error before any commands are consumed; no partial initialized result. |
| Correct prefix, malformed last cell near entry 200,000 | Same atomic failure; location identifies the offending entry. |
| Empty or malformed YAML, or unreadable path | Clear source-aware startup error; no fallback and no movement. |
| Valid YAML with empty occupied sequence and empty commands | Starting pose unchanged, outcomes `[]`. |
| Duplicate cell, boolean/string coordinate, duplicate mapping key, alias, occupied start | Add exact success/error assertions after the open policies are answered. |

Also verify occupancy is coordinate-only, mutable caller input is snapshotted,
one-pass input works, and the loaded immutable set can be reused across runs with
no reparse/copy. After loading, modifying the source file must not alter movement.
A command iterator with observable consumption should remain untouched on load
failure. Measure a generated 200,000-unique-cell input with both hit/miss movement
queries and report dataset shape, runtime/parser versions, load time and memory;
do not invent a timing threshold. This is proposed validation, not a benchmark result.

## Validation status and limits

The [fresh baseline](evidence/yaml-baseline.md) records three passing existing
movement tests only. The [earlier report](evidence/occupied-baseline.md) and
[historical acceptance](history/completed.md) remain unchanged. No implementation,
new tests, YAML parsing experiment, dependency installation, or design/plan/code
review was performed in this phase. Both revised documents await review. Full
checks remain owned by [DEVNOTES](../DEVNOTES.md); revise its dependency policy only
when that decision is resolved in a future authorized implementation.
