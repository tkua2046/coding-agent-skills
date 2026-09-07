# Navigator design

Current goal: load starting pose and roughly 200,000 fixed occupied cells from
YAML once, validate before movement, and retain D1 and blocked-move behavior.
Status: revised design proposed; implementation and design review pending.
Use a separate load/validate boundary producing a pose and immutable hash set;
movement performs only destination membership queries. This costs O(n) retained
storage and expected O(1) per lookup, with additional YAML parsing peak memory.
Next: resolve the [open contracts](#open-contracts), then deliver the
[pending plan](PLAN.md). No YAML dependency has been selected or installed.

Sources: [original](ORIGINAL.md), [occupied request](OCCUPIED_REQUEST.md),
[YAML request](YAML_REQUEST.md), [sample](../examples/start.yaml), and
[current specification](SPEC.md). Evidence: [prior baseline](evidence/occupied-baseline.md)
and [fresh YAML baseline](evidence/yaml-baseline.md).

## Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment

Inspection: `navigator.run(pose, commands)` currently assigns `_target(pose)` on
every F and appends True for every recognized command. Existing tests cover basic
movement, left-turn wrapping and unknown commands; occupancy and YAML are absent.
Keep the direction lookup and turn logic.

Propose `run(pose, commands, occupied=())`, preserving existing two-argument calls.
Normalize caller-supplied coordinate pairs into a frozenset once at entry; reuse
an already normalized loader-produced frozenset without rebuilding it. The snapshot
is fixed while commands execute. A caller's mutable collection cannot alter it.
Duplicate-cell semantics remain open below, superseding the earlier assumption
that duplicates are silently ignored for all inputs.

For F, compute the candidate pose, test only its `(x, y)` against occupancy, and
append False without changing position or heading if blocked. Otherwise adopt
the candidate and append True. Turns append True and do not consult occupancy.
Each recognized command yields one boolean in order. Unknown commands still raise
ValueError, including after a blocked move, without returning a partial result.

## YAML loading and ownership

Proposed public boundary: `load_start(path)` returns `(pose, occupied)` for use
with `run(pose, commands, occupied)`. Commands remain caller supplied; no command
field, CLI, reload mechanism, routing, persistence or session framework is added.
The caller loads once and retains the normalized values for movement. Multiple
runs may share immutable occupancy; each run still owns its pose and outcomes.
README will own usage once implemented, not this document.

Read one YAML document, parse with a safe data-only parser, validate the complete
structure and values, then publish the normalized result. Do not yield cells or
start consuming commands while loading. A malformed final entry must fail just
as early as a malformed first entry: no partially usable configuration escapes.
Proposed errors are ValueError with the source path and field/index (for example,
`start.yaml: occupied[199999]: expected two integer coordinates`); syntax errors
include line/column when available. File-read errors retain OSError with path
context. These error details are proposals, not a confirmed exception contract.

A frozenset of integer pairs is the proposed retained representation: expected
O(n) construction, O(n) storage and expected O(1) membership per F. A list would
scan up to 200,000 entries per move; a dense board does not suit unbounded sparse
coordinates. YAML may temporarily retain source, parser objects and normalized
pairs together. Release parse intermediates after successful loading. Do not
claim a memory ceiling or timing guarantee without measurement. Ordinary safe
loading plus explicit validation is the starting approach; a streaming parser or
compact coordinate encoding needs evidence of an actual budget problem first.

Python's standard library has no YAML parser, while DEVNOTES currently says
standard library only. Proposed direction is a maintained safe YAML dependency,
subject to resolving that constraint; no package/version is chosen here. A custom
YAML parser would create a substantial maintenance burden and incompatible subset
risk. JSON or a restricted input language changes the requested contract and
cannot silently substitute for YAML. Safe parsing alone is insufficient: scalar
coercions, duplicate mapping keys, aliases and schema validation need explicit
handling and tests against the eventually chosen parser.

## Open contracts

The request confirms clear structural failure before movement but explicitly
leaves detailed invalid-value and duplicate policies undecided. The sample shows
one valid shape; it does not settle the following contracts. Questions have been
raised with the user; dependent choices remain open, not approved by silence.

| Decision | Proposed contract and consequence | Example requiring a decision |
|---|---|---|
| Schema and scalar values | Require exactly `pose` and `occupied`; pose has exactly `x`, `y`, `heading`; occupied is a sequence of two-item sequences. Require integers excluding bool, heading 0–3; allow negative/unbounded coordinates. Reject missing/extra fields. | `occupied: null`, `occupied: [[1]]` are structural errors; `x: true`, `x: 1.0`, `heading: 4` need value policy. Is missing `occupied` an error or empty? Should `occuped: []` be rejected? |
| Duplicate cells and occupied start | Recommend deduplicating coordinate entries and allowing a start on an occupied cell under entry-only blocking; neither was confirmed previously. | Start (0,0,1), occupied [[0,0],[0,0]]: accept and F leaves for (1,0), or reject before movement? Duplicate rejection requires detecting duplicates before set conversion. |
| YAML mapping and language policy | Recommend one document, reject repeated mapping keys, custom tags, merge keys and aliases; allow ordinary comments and block/flow collections. Exact parser behavior must be checked. | Two `pose:` keys must not silently replace a pose under this proposal. `occupied: *cells` would be rejected; is alias support needed? |
| Dependency constraint | Recommend allowing a maintained safe YAML parser and updating DEVNOTES in implementation. | Full YAML parsing conflicts with current standard-library-only operations. If that constraint is retained, input scope must be revisited before loader work. |

The strict YAML validation boundary is new. It does not promise comprehensive
validation of all malformed legacy direct API inputs. The occupied-start and
cell-duplicate decisions should apply consistently to direct and YAML inputs.
Exact loader name and error wrapping are reversible proposed defaults. No hard
performance budget was supplied; measure representative 200,000-cell input before
claiming suitability for a particular memory or latency limit.

## Acceptance and validation

These expected results follow from the heading convention; feature checks remain
planned. Conditional rows must be finalized when their contracts are answered.

| Input | Expected result |
|---|---|
| Load `examples/start.yaml`, then F | Pose starts (0,0,0), occupied {(0,1),(2,3)}; result ((0,0,0), [False]) |
| Same loaded input, FRF | ((1,0,1), [False, True, True]) |
| Pose (0,0,1), occupied {(1,0)}, FRF | ((0,-1,2), [False, True, True]) |
| Same direct inputs, FFL | ((0,0,0), [False, False, True]) |
| Pose (0,0,0), occupied {(0,-1)}, LLF | ((0,0,2), [True, True, False]) |
| Pose (0,0,1), occupied {(0,0)}, F | ((1,0,1), [True]) if entry-only starting occupancy is accepted |
| Pose (0,0,1), occupied {(1,0)}, F? | ValueError; no returned result |
| Omitted or empty direct occupancy | Existing movement and return behavior |
| Empty YAML, non-mapping root, pose sequence, or malformed final coordinate pair | Clear load error; no configuration returned and command iterator never advanced |
| Invalid values, duplicate cells/keys, unknown fields, aliases or extra YAML documents | Expected rejection/normalization finalized from open contracts; errors precede commands |
| Valid input with 200,000 distinct cells, including negative coordinates | Exact normalized membership; free and blocked moves correct; one load, no file I/O or collection rebuilding per command |

Future tests should cover free moves in all headings, iterable ownership and
caller mutation isolation, syntax/read errors, and the complete agreed schema.
Use a command iterator with observable consumption to prove failed loading cannot
start execution. Measure load duration, peak memory and retained memory separately
from repeated lookup/movement timing using the selected parser and prepared data;
record runtime/parser and dataset. No numeric threshold or benchmark result is
invented here. The current three-test baseline verifies only D1. Prior evidence
and completed acceptance remain unchanged and do not review this revision.
