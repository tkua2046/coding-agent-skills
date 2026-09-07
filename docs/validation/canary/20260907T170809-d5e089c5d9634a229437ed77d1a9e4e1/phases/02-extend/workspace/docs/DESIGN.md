# YAML initialization and fixed occupied cells

Load and validate the entire YAML configuration before exposing a starting pose
or consuming movement commands. Retain occupied coordinates in one immutable hash
set and query that set for each forward destination. This supports about 200,000
cells with expected constant-time membership checks, at the cost of set storage
and temporary parsing data. For [the supplied YAML](../examples/start.yaml),
`FFRF` yields `((1, 0, 1), [False, False, True, True])`. A malformed final cell
must reject the entire configuration before even the first command is consumed.

The parser choice is unresolved: general YAML needs a parser dependency while
[DEVNOTES](../DEVNOTES.md) requires the Python standard library only. Strict value,
duplicate and start-cell policies below are also proposals awaiting resolution.
These decisions precede implementation of the YAML boundary; this document does
not select or install a dependency.

Decision: proposed revision of the occupied-cell design, incorporating the
confirmed [YAML request](YAML_REQUEST.md). Sources: [original](ORIGINAL.md),
[occupied request](OCCUPIED_REQUEST.md), and [current spec](SPEC.md). Delivery and
review status: [current plan](PLAN.md#delivery-status). The unchanged accepted
[D1 source](history/design-d1.md) remains historical authority for basic movement.

## Compatibility and state ownership

Keep state local to each run, unbounded integer coordinates, clockwise headings
0–3, and the existing `(final_pose, outcomes)` return shape. Unknown commands still
raise `ValueError` and abort processing. Direction lookup and turning behavior
remain as in D1. Only the forward destination is tested: blockage appends `False`,
preserves the full pose, and continues; a free move or turn appends `True`.

Retain the proposed direct API `run(pose, commands, occupied=())`, supporting both
positional and keyword occupancy. Existing two-argument calls still work. Finite
iterables of integer-coordinate tuples are snapshotted before consuming commands;
caller collections are never mutated. This protects against caller mutation during
command iteration. General malformed direct-API inputs remain outside that
supported contract; YAML has an explicit validation boundary.

Propose a separate `load_config(path)` returning an immutable configuration with
`pose` and `occupied` fields. Usage would be `config = load_config(path)`, then
`run(config.pose, commands, occupied=config.occupied)`. Commands stay with the
caller, and loading once and reusing occupancy across runs is explicit. Direct
navigation should remain usable without importing a YAML dependency. A CLI, global
session, implicit default file, path cache and automatic reload are not required.
The supplied YAML is an example, not a new mandatory default path.

Reuse loader-produced immutable occupancy without rebuilding or rescanning it per
run. Mutable direct inputs still need a snapshot per run. Each forward command
performs one destination membership query; no file access, reparsing, linear cell
scan or occupancy copy occurs in the command loop. Shared configuration keeps
occupancy fixed while each run owns its pose. This revises the earlier proposal
that every call always owns a fresh snapshot, to avoid repeated work at this scale.

## Load, validate, then activate

Propose reading one UTF-8 YAML document through a safe data-only parser, validating
the complete shape and values, and converting coordinate lists into immutable
pairs in a frozen set. Publish the configuration only after every entry passes.
Do not use a loader that constructs arbitrary application objects. The concrete
parser must support the agreed policies rather than silently losing information
that validation needs.

The structural schema derived from the example is a top-level mapping containing
`pose` (a mapping with `x`, `y`, `heading`) and `occupied` (a sequence of entries
with exactly two coordinates). Proposed strictness rejects missing fields, null
input and extra fields. No partially initialized configuration is returned.
Messages identify the file and failing logical path, for example
`start.yaml: occupied[199999]: expected a two-coordinate sequence`. Syntax errors
should retain line/column information when available. Propose a documented
configuration exception for parsing/schema failures and clear path-bearing I/O
errors for unreadable input. A missing dependency must explain required setup
before movement begins. These API/error details are proposals, not confirmed
requirements.

Candidate construction has no external effects. On failure or interruption,
discard it; any previously loaded immutable configuration remains usable. Correct
an invalid final entry, explicitly reload, and then start movement from the supplied
pose. There is no partially executed command stream to resume. Unknown movement
commands remain runtime errors, not YAML failures or a promise to roll back earlier
valid commands.

## Scale and dependency consequences

For N input entries and U distinct cells, loading/building takes expected O(N)
work and retained occupancy takes O(U) memory. A list would avoid hash-index overhead
but make each membership query O(N); a hash set fits the stated movement workload.
These are expected complexities, not worst-case guarantees or measurements.

A conventional YAML loader may retain file text, a parsed object graph, and the
final set simultaneously. Peak loading memory therefore exceeds steady-state
occupancy memory. Release parsing temporaries; do not retain a second coordinate
list. About 200,000 entries justify measuring load time and peak/retained memory
with the future chosen parser. No numerical budget is supplied, so no measured
performance claim is made. If an agreed budget is exceeded, investigate an event
or streaming parser while retaining full validation before activation. A spatial
index or database is unnecessary for exact fixed-cell membership.

Prefer a maintained safe YAML parser and an explicit amendment to the
standard-library-only policy. The alternative is a negotiated restricted format;
handwritten general YAML parsing adds substantial ambiguity and maintenance cost.
No parser guarantees are established by this fixture. Before choosing a dependency,
verify scalar resolution, duplicate-key detection, document count, tags, aliases
and merge handling against the selected parser. Safe loading alone does not settle
all those policies. This phase uses no external services and installs nothing.

## Unresolved contract questions

These defaults remain proposed. They supersede the previous design's claim that
no material decision remained; resolve them before implementing the YAML boundary.
Accepted basic navigation behavior is unchanged.

| Question | Proposed default and example | Consequence |
|---|---|---|
| May implementation add a parser despite DEVNOTES? | Allow a maintained safe YAML parser; select it after verifying required behavior. | General YAML requires a dependency/policy decision. Keeping standard-library-only requires agreement on a restricted input format instead. |
| Are all fields required and extras rejected? | Require `pose: {x: 0, y: 0, heading: 0}` and `occupied: []`; reject missing `occupied`, null/empty input, and extra `occuped`. | Catches spelling errors; omitting an empty list would fail. |
| Which scalar values are valid? | Integer coordinates excluding booleans; integer heading 0–3. Reject `x: "2"`, `x: 2.0`, `x: true`, and `heading: 4`; accept negative coordinates. No coercion or heading wrapping. | Avoids accidental Python/parser coercion; verify scalar resolution with the chosen YAML version/parser. |
| Which duplicates are allowed? | Collapse `occupied: [[0, 1], [0, 1]]`; reject repeated mapping keys, e.g. two `heading` or two `pose` keys. | Repeated cells do not change occupancy. Duplicate keys must be caught before ordinary mapping construction discards them. |
| Can the start be occupied? | Allow start `(0, 0, 0)` with `occupied: [[0, 0]]`; `RF` reaches `(1, 0, 1)`. | Preserves the prior proposed destination-only convention. Rejecting occupied starts adds an initialization constraint. |
| Which YAML features are supported? | One document; reject custom tags, anchors/aliases and merge keys. A second document following `---` fails. | Restricts YAML features to keep validation/resource behavior understandable; requires parser-specific verification. |

The proposed loader path API keeps the library interface small. No memory or latency
budget is specified; record scale evidence before choosing more elaborate parsing.

## Acceptance targets

These are expected outcomes, not results from the current implementation. Contract
question examples also become acceptance cases once their rules are settled.

| Input or scenario | Expected result |
|---|---|
| Load the supplied file, then `FFRF` | `((1, 0, 1), [False, False, True, True])`. |
| Direct `run((0, 0, 0), "F", {(0, 1)})` | `((0, 0, 0), [False])`. Repeated blockage preserves full pose and allows subsequent commands. |
| Direct `run((0, 0, 0), "LF", {(-1, 0)})` | `((0, 0, 3), [True, False])`; verify blocking in all four headings. |
| Direct `run((0, 0, 0), "RF")`, or empty occupancy | `((1, 0, 1), [True, True])`; existing calls remain compatible. |
| Empty commands after a valid load | Unchanged starting pose and `[]`. |
| `occupied: [[0, 1], [2]]`, including a malformed final entry in a 200,000-entry file | Clear entry-path error; no configuration published and command iterator never advanced. |
| Mapping instead of occupied sequence; list instead of pose mapping; malformed YAML; unreadable path | Clear structural, syntax or I/O error before commands are consumed. |
| Correct an invalid file and explicitly retry | Complete configuration becomes usable from supplied pose; a previously loaded configuration stays unchanged. |
| About 200,000 unique cells reused across runs | Load/build once; no occupancy scans/copies in movement or rebuild on reuse; correct blocked/free queries. Record load time and peak/retained memory without inventing thresholds. |
| Caller mutates direct occupancy during command iteration | Run observes its initial snapshot. Finite one-shot iterables and independent runs work; duplicates follow the settled policy. |
| Direct `run((0, 0, 0), "F?", {(0, 1)})` | Raises `ValueError` after blockage; blockage itself does not stop processing. |

Test structural rejection and zero command consumption independently of the chosen
strict-value defaults. Include duplicate-key and boolean cases when verifying the
actual parser, not just validation of already constructed Python objects.
