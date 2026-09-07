# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment

Status: proposed design for the [confirmed extension](SPEC.md#confirmed-occupied-cell-extension--pending-implementation),
now extended by the [YAML amendment](#yaml-loading-amendment); implementation has
not begun. Keep D1 and add a local occupied-coordinate lookup.
A blocked F yields False without changing pose; remaining commands execute.
Existing two-argument callers retain their behavior. Next step: the single pending
[implementation plan](PLAN.md#pending-stage-s1). Occupancy alone needs no dependency;
YAML introduces a parser decision that remains open. Amendment reviews are pending.

### Interface and state

Propose `run(pose, commands, occupied=())`, accepting a finite iterable of integer
coordinate pairs represented as `(x, y)` tuples. Snapshot ordinary iterables once
at entry; reuse a loader-produced immutable coordinate set without copying it.
Duplicate collapse is proposed, pending the YAML policy below. This supplies expected constant-time lookup
per F at O(n) construction time and O(u) space for u unique cells. Scanning the
caller's collection on every move is simpler in storage but costs O(n) per F and
can observe caller mutation; the snapshot fits fixed occupancy and local ownership.
Never mutate the caller's collection or retain it globally. A caller may retain
and reuse an immutable loaded configuration across runs.

Inspect `_target(pose)`'s candidate coordinates before assigning pose. Occupancy
compares `(x, y)`, independent of heading. Only a blocked F appends False; turns
and successful translations append True. Unknown commands still raise ValueError,
including after a blocked move. Each valid command has exactly one outcome.

The baseline does not validate pose inputs. This amendment assumes valid poses
and coordinate tuples and adds no coercion or specified malformed-occupancy error
contract for direct Python calls. YAML inputs require the separate validation
boundary below. The target-only rule proposes allowing a starting pose on an occupied cell:
turning and departure to a free cell remain possible. These are proposed boundary
choices; the YAML questions below now block finalizing the affected contract.
Infinite iterables, concurrency and dynamic occupancy remain outside this design.

### Acceptance and validation

Hand-derived examples (north increases y; east increases x):

| Initial pose / occupied / commands | Expected result |
|---|---|
| `(0, 0, 1)` / `{(1, 0)}` / `F` | `((0, 0, 1), [False])` |
| `(0, 0, 1)` / `{(1, 0)}` / `FRF` | `((0, -1, 2), [False, True, True])` |
| `(0, 0, 1)` / `{(1, 0)}` / `FFL` | `((0, 0, 0), [False, False, True])` |
| `(0, 0, 0)` / `{(0, 0)}` / `RF` | `((1, 0, 1), [True, True])` |
| `(0, 0, 3)` / `{(-1, 0)}` / `F` | `((0, 0, 3), [False])` |
| `(0, 0, 1)` / `{(1, 0)}` / `F?` | `ValueError`; no normal result |

Verify omitted and empty occupancy preserve baseline behavior, empty commands
return the starting pose with no outcomes, and blocking works in every heading.
Check duplicate and iterable input, caller collection preservation, and separate
runs with different occupancy to guard against state leakage.

Inspection found that `_target` already computes a candidate without mutation;
`run` currently assigns it unconditionally and appends True for every valid command.
The three existing tests cover basic movement, left wrap and unknown commands,
but no obstacle behavior. They passed in the prior occupied-cell phase; see
[preserved baseline evidence](evidence/occupied-baseline.md). All extension checks above
remain proposed. D1's historical acceptance does not cover this amendment.

## YAML loading amendment

Status: proposed, not implemented or reviewed. The [confirmed YAML scope](SPEC.md#confirmed-yaml-extension--pending-implementation)
requires complete validation before movement and an in-memory lookup suitable for
about 200,000 cells. Retain D1 and blocked-move semantics. Propose a separate loader
that publishes an immutable pose/occupancy configuration only after validation.
This adds parser and peak-memory costs; it avoids parsing or scanning cells during
movement. Next: resolve the contract questions below, then execute the revised
pending plan in a separately authorized implementation phase. No parser has been
selected, installed or exercised here.

### Loading boundary and representation

Proposed public shape: `load_start(path)` returns an object with `pose` and
`occupied`; callers use `run(config.pose, commands, config.occupied)`. Commands
remain supplied separately. A file loader fits the supplied example and keeps
filesystem/parser concerns outside movement. A new CLI or implicit path overload
on `run` changes the entry contract and is not assumed. Existing two-argument
Python callers keep their behavior, including unknown-command ValueError.

Read one YAML document, parse data only (no object construction), validate the
entire root, pose and every occupied entry, and only then return the configuration.
Do not consume commands, begin movement, or publish a partial configuration while
loading. A malformed final occupied entry must fail just as an invalid first entry
does, even with empty commands. File/parse errors also prevent movement. Propose a
loader-specific ValueError subtype with source path and a field path such as
`occupied[199999]: expected two integer coordinates`; syntax errors should include
line/column when available. Exact exception/message API is provisional; errors
must identify the problem without dumping a 200,000-cell document.

Use `(x, y)` tuples in a `frozenset` owned by the loaded configuration, and an
immutable pose tuple. Construction takes expected O(n) time and O(u) retained
space for n entries and u unique cells; each attempted forward move performs one
expected O(1) membership lookup. Reuse this set in `run` rather than rebuilding
200,000 entries per call. An ordinary mutable iterable is still snapshotted once
for direct callers. Turns never query occupancy. Loading is explicit and once per
configuration, not cached globally; the caller controls its lifetime and reloads.

A list scan costs O(n) per F, which makes movement depend on file size. A dense
grid needs bounds absent from D1 and wastes space for sparse coordinates. A hash
set fits this requirement without a spatial index. A conventional YAML parser may
temporarily retain the source, a full parsed tree, and the normalized set together;
release transient structures after validation. Actual peak memory, parse time and
parser capabilities are unmeasured. The fixture contains two cells, not a scale
benchmark. Before finalizing the loader, measure 200,000 unique cells using the
approved parser and runtime. Streaming/event parsing is a fallback only if measured
peak memory exceeds the agreed budget; it complicates diagnostics and full-input
validation. Do not claim a memory or latency guarantee without a target budget.

### Contract questions and proposed defaults

These choices remain open; examples distinguish the alternatives. No response
has been recorded in this phase. Resolve the relevant questions before implementing
dependent YAML behavior; independent occupancy work can proceed later.

| Question | Proposed default and consequence | Example needing a decision |
|---|---|---|
| Required fields and unknown keys? | Require exactly `pose` and `occupied`, exactly `x`, `y`, `heading` in pose, and a sequence of length-two sequences for occupied. Reject missing/null/extra fields to expose typos; accepting extras would improve extensibility. | `occupied: []` is valid; omitted `occupied`, `occupied: null`, or extra `occuped: []` fails under this proposal. |
| Invalid scalar values/coercion? | Require actual integers, excluding booleans; x/y remain unbounded and heading is 0–3. No string/float coercion or heading wrapping. YAML scalar resolution must match the chosen parser/version. | Reject `x: "2"`, `x: true`, `x: 2.0`, `heading: 4`; allow `x: -2`. |
| Duplicate cells, duplicate mapping keys, and occupied start? | Collapse repeated cells, reject repeated mapping keys rather than silently choose a value, and retain target-only blocking so an occupied start may turn/depart. These are distinct policies. | `occupied: [[0,1], [0,1]]` yields one cell; repeated `x` keys fail; pose `(0,0,0)` with occupied `[[0,0]]` and `RF` reaches `(1,0,1)`. |
| YAML dialect/features and dependency permission? | Prefer a maintained data-only YAML parser with clear errors and duplicate-key handling. DEVNOTES currently requires standard library only, so dependency policy must be resolved before selecting a library. Do not write a partial YAML parser and call it full YAML support. | Are anchors/aliases and merge keys supported or rejected? Propose one document and no custom tags/merge keys; `---` introducing a second document fails. Parser/version behavior needs verification. |
| Entry point and error API? | Separate path loader and a loader-specific ValueError subtype, no new CLI; later document encoding and file-error wrapping. | Should users call `load_start("examples/start.yaml")`, or expect a command-line invocation? Existing README only documents a Python function. |
| Resource acceptance target? | Test approximately 200,000 unique cells plus repeated movement, recording load time and peak memory separately from lookup time; do not impose an arbitrary cap. | What memory ceiling and startup latency on which target runtime must a 200,000-cell file meet? Alias expansion or unusually large inputs also need a parser/resource policy if supported. |

### Acceptance and evidence

Confirmed outcomes (tests remain proposed):

| Input / action | Expected result |
|---|---|
| Load supplied `examples/start.yaml`, then `FRF` | Pose starts `(0,0,0)`; `(0,1)` blocks F, R faces east, F reaches `(1,0,1)`; outcomes `[False, True, True]`. |
| Same example, then `F` | `((0,0,0), [False])`; full pose preserved. |
| Valid prefix followed by a cell `[2]`, or root `[]`, or `pose: []` | Clear structural load failure; no configuration published and no command consumed or movement performed. |
| Valid configuration reused for several command batches | No file reread, reparse, or occupancy rebuild; each run starts from its supplied pose and has its own outcomes. |
| About 200,000 unique cells and many F commands | One load/build, correct blocked/free results, fixed lookup independent of cell count; record memory/time evidence without assuming a pass threshold. |

After policy resolution, add acceptance for the conditional examples in the
question table, including duplicate keys and parser-specific scalar/tag behavior.
Keep direct Python compatibility and all occupied-cell acceptance above. Validate
the final-entry failure with an observable command iterator to prove no commands
were consumed. Verify immutable reuse by inspection/instrumentation rather than
a brittle timing-only unit assertion.

Fresh-context inspection and the existing three-test baseline are recorded in
[YAML phase evidence](evidence/yaml-baseline.md). They establish only current D1
behavior. Scale, loader, occupancy and parser claims remain proposed; historical
S0 acceptance and prior reports are preserved. Design and plan reviews remain pending.
