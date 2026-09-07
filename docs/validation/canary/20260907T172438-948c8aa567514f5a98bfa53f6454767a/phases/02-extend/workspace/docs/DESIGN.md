# Design: YAML startup and fixed occupied cells
Status: revised proposal; implementation and review are pending. The
[confirmed YAML request](YAML_REQUEST.md) adds starting pose and about 200,000
occupied cells loaded once into memory. Validate the complete input before any
movement, then use a fixed coordinate set for expected O(1) destination checks.
Keep D1's local pose, direction lookup, and per-command outcomes. YAML parsing adds
startup time and peak memory; it must never enter the movement loop. Next: resolve
[open contracts](#open-contracts), then deliver the [pending stage](PLAN.md).

This extends the existing design because startup ownership, validation, and scale
affect the same navigation feature. No implementation or dependency selection is
claimed. Sections below cover current evidence, interfaces, consequences, acceptance,
and open contracts; accepted D1 is preserved at the end.

## Authority and current evidence
The [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and [YAML request](YAML_REQUEST.md) remain source records; [SPEC](SPEC.md) owns
confirmed behavior. The earlier exclusion of configuration files is superseded by
YAML startup. Routing, persistence of changes, and moving obstacles remain outside scope.

`navigator.py` currently has only `run(pose, commands)` and no occupancy or loader.
[Fresh baseline evidence](evidence/yaml-baseline.md) verifies the three existing
movement/turn/error tests only. The example in [start.yaml](../examples/start.yaml)
shows a pose mapping and a list of coordinate pairs; it does not settle every
valid-value policy. Earlier [occupied-cell evidence](evidence/occupied-baseline.md)
and [S0 acceptance](history/completed.md) retain their original scope.

## Proposed interfaces and startup ownership
Retain `run(pose, commands, occupied=())` as the proposed compatible extension,
returning `(final_pose, outcomes)` and preserving two-argument callers. Add a
library loader, provisionally `load_start(path)`, returning the validated pose and
an immutable occupied-coordinate set. Commands remain caller-supplied. A CLI and
commands embedded in YAML are not currently requested.

The caller loads once before starting a run and may reuse that loaded configuration.
For arbitrary caller iterables, `run` takes one immutable snapshot before commands;
a loader-produced immutable set can be reused without another full copy. No
caller-owned mutable collection is retained or changed. Pose is local to each run;
there is no global cache, file watcher, reload, or shared mutable session.

Startup is an all-or-nothing boundary: read, safely parse, validate the entire
document, and normalize all cells before returning a usable configuration. Even a
malformed final cell prevents the first command from being consumed. Build locally;
on failure discard partial data and raise a clear configuration error. No partial
configuration or fallback to empty occupancy may escape. Replacing a bad file and
retrying is a new load, with no stale partial state.

Proposed structural schema: one YAML document whose root is a mapping, with `pose`
a mapping containing `x`, `y`, `heading`, and `occupied` a sequence of two-element
coordinate sequences. Thus `occupied: [[0, 1], [2]]` fails at `occupied[1]` before
movement. Scalar types, missing/extra keys and duplicate policies await confirmation
below. Validation applies even when there are no movement commands.

Use a maintained parser's safe data-only mode, never object construction or
arbitrary YAML tags. Safe parsing alone does not validate the application schema.
The parser choice must support the agreed duplicate-key and document policies;
default silent key overwrite is not sufficient if rejection is chosen. Wrap parse
and schema failures in a proposed configuration-specific ValueError subclass with
file and field/index context, e.g. `start.yaml: occupied[1]: expected two coordinates`.
Use parser line/column details when available; readable I/O failures must identify
the file. Keep unknown movement commands' existing ValueError behavior separate.
Exact public names and error text are reversible implementation defaults.

## Lookup, movement and scale consequences
Store occupied coordinates as an immutable hash set of integer tuples. For n input
cells and u distinct cells, conversion is O(n) expected work and O(u) retained
storage; membership is expected O(1), not a worst-case latency guarantee. Duplicates
may reduce retained size if deduplication is agreed. Scanning a 200,000-cell list
on every F repeats work; a bitmap would impose bounds or allocate for empty space
on this unbounded grid. An indexed database adds machinery despite the requirement
to load into memory once.

A conventional YAML parser may hold the text, parsed list graph, and normalized set
at the same time. Release text and parsed containers after validation and retain
only pose and lookup data. Do not claim low peak memory from the set alone. Measure
startup time, peak process memory, retained memory and repeated query cost with
about 200,000 distinct cells before accepting the implementation. No runtime or
memory budget has been supplied, and no scale benchmark has been performed. Start
with a conventional parser plus conversion; a streaming parser or compact encoding
needs measured pressure and a compatible YAML contract to justify its complexity.

F computes its candidate using the existing direction lookup. Only an unoccupied
candidate replaces pose. A blocked F appends False and continues; successful F and
L/R append True. Turns do not consult occupancy. Unknown commands still raise
ValueError. Headings remain 0=north, 1=east, 2=south, 3=west; coordinates are unbounded.
The earlier proposal to permit departure from an occupied start is retained as an
open proposal, not a confirmed requirement. Direct API callers' valid-input
assumption does not waive full validation at the YAML boundary.

## Acceptance and validation
These are proposed checks; conditional policies must be settled before implementing
the corresponding expectations.

| Input | Expected result |
| --- | --- |
| Load `examples/start.yaml`, run `FRF` | `((1, 0, 1), [False, True, True])`: north is blocked, then turn and move east |
| `run((0, 0, 1), "FFLF", {(1, 0)})` | `((0, 1, 0), [False, False, True, True])` |
| `run((0, 0, 0), "RF")`, or loaded empty occupancy | `((1, 0, 1), [True, True])`, preserving D1 |
| Root `[]`, `pose: []`, `occupied: {}`, or cell `[2]` | Clear structural error with location; no command consumed or pose changed |
| Syntax error, unreadable file, or malformed cell at index 199999 | Startup fails before movement; no partial configuration returned |
| Valid negative-coordinate cells | Matching destinations block just like positive coordinates |
| Load once, then run repeated commands with file access disabled | Same outcomes, no parsing, reads, or occupancy rebuild during movement |
| `run((0, 0, 1), "F?", {(1, 0)})` | ValueError on `?` after the blocked F |

Also check reusable loaded-state isolation, unchanged caller collections, one-shot
iterables, turn wrapping, and conditional duplicate/start policies. For scale use
about 200,000 distinct cells with known hit/miss destinations; test exact outcomes
and report startup/peak-memory/query measurements without inventing a pass budget.
Do not make hardware-sensitive timing assertions in ordinary unit tests. A final
invalid cell must fail before even advancing a command iterator, proving validation
is not interleaved with movement. YAML parser tests must include unsafe tags and
any agreed duplicate-key/alias/document rules. README will own implemented usage;
DEVNOTES will own dependency/setup and measurement instructions when implemented.

## Open contracts
The following recommendations remain proposals, not answers inferred from silence.

- **Dependency rule:** DEVNOTES currently says standard library only, which has no
  YAML parser. May a later implementation use a maintained parser? Recommend yes;
  retaining that rule requires an explicitly agreed restricted format or another
  agreed approach. A hand-written partial parser must not silently stand in for
  YAML. No package is selected or installed in this phase.
- **Values and schema strictness:** recommend required fields, no unknown keys,
  actual integers (excluding booleans), heading 0..3, and no coercion. Should
  `x: "1"`, `x: true`, `x: 1.0`, `heading: 4`, missing `occupied`, or misspelled
  `ocupied` fail, or be converted/defaulted? Strictness catches mistakes but rejects
  otherwise recoverable inputs. Empty `occupied: []` is the proposed valid empty case.
- **Duplicates and starting position:** recommend deduplicating repeated pairs;
  alternatively reject them to expose input mistakes. Should start `(0, 0)` with
  `occupied: [[0, 0], [0, 0]]` load and allow departure, or fail? Rejecting an occupied
  start changes the earlier destination-only proposal. Duplicate mapping keys are
  a different issue: recommend rejecting `pose: {x: 0, x: 9, y: 0, heading: 0}`
  rather than allowing parser-dependent selection.
- **YAML language scope:** recommend exactly one document, no custom tags, merge
  keys, or aliases in this simple schema. Should an alias pair such as `- &p [0, 1]`
  followed by `- *p` be accepted? This choice affects parser configuration and
  validation complexity; a second `---` document must not be silently ignored.
- **Invocation and scale target:** recommend an explicit library load followed by
  `run`, keeping commands outside YAML. Is a command-line entrypoint needed instead?
  Loading once per explicit configuration load permits reuse across runs; confirm if
  a different lifetime is intended. What startup-time/peak-memory limits and target
  machine apply to 200,000 cells? Correctness and load-once checks can be specified
  now, but resource acceptance cannot yet be assigned a numeric threshold.

## Accepted design D1 (preserved)
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.
