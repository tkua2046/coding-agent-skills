# Navigation behavior

This target contract includes the confirmed [occupied-cell](OCCUPIED_REQUEST.md)
and [YAML startup](YAML_REQUEST.md) requests. Delivery status is in the
[plan](PLAN.md#delivery-status). The [original request](ORIGINAL.md),
[pre-occupied specification](history/pre-occupied-documents.md) and
[pre-YAML proposals](history/pre-yaml-documents.md) remain preserved.

The grid is unbounded, with integer coordinates and headings 0, 1, 2, 3 for
north, east, south, west. Return the final pose and one Boolean success outcome
per processed valid command. L/R turn in place and succeed. Unknown commands
raise ValueError. F into a fixed occupied cell reports False, preserving position
and heading; commands continue. F into a free cell advances and succeeds.
Omitting occupied cells in existing programmatic calls preserves their behavior.

Load the starting pose and about 200,000 occupied cells from YAML once into memory
for movement queries. Invalid structure must fail clearly before any movement.
Commands remain supplied by the caller. Configuration loading is now in scope;
routing, persistence of movement, moving obstacles and board boundaries remain out.

## Proposed YAML contract and open questions

The example establishes `pose` with `x`, `y`, `heading`, and `occupied` as a
sequence of coordinate pairs. The exact rules below are proposals, not confirmed
invalid-value or duplicate policies. Resolve these questions before loader
implementation; parser-specific behavior must not decide the contract accidentally.

| Question | Proposed rule and concrete consequence |
|---|---|
| Required fields, empty input and unknown fields? | Exactly one mapping document with required `pose` and `occupied`; pose requires exactly `x`, `y`, `heading`. Reject missing/null fields, extra keys and multiple documents. `occupied: []` is valid; `occupied: null`, omitted occupied, or `pose: [0, 0, 0]` fails. Rejecting extra keys catches `occpuied` but limits future metadata. |
| Scalar values and headings? | Require integers excluding booleans; coordinates may be negative, heading must be 0–3. Reject `x: true`, `x: 1.0`, `x: "1"` and `heading: 4` rather than coercing or wrapping. This preserves an integer grid while preventing parser coercions from silently choosing a pose. |
| Repeated cells and duplicate mapping keys? | Collapse repeated `[0, 1]` cells because occupancy is membership; reject repeated `heading` or other mapping keys to avoid silent last-value wins. Rejecting repeated cells instead would detect possible input mistakes at the cost of disallowing redundant maps. |
| Occupied starting cell? | Preserve the prior proposed destination-only rule: starting at occupied `[0, 0]` allows turning and departure, but re-entry fails. Rejecting this start would add a distinct validity constraint. |
| YAML features and loader interface? | Propose `load_start(path)` returning immutable pose/occupancy, one explicit load reusable across runs. Accept ordinary block/flow collections as in the fixture; reject custom tags, aliases/anchors and merge keys initially for a simple explicit document. Confirm this YAML feature boundary and any file-size/resource limits; none are established by the request. |
| Error contract? | Propose ValueError with field/index for schema errors and file/line where available for syntax errors; retain distinguishable I/O failures. `[2, 3, 4]` at occupied index 9 reports `occupied[9]: expected [x, y]`. Confirm whether callers require a dedicated configuration exception. |

A maintained YAML dependency is proposed by the design; DEVNOTES currently says
standard library only. Dependency policy and parser selection remain unresolved.

## Proposed programmatic defaults

Use `run(pose, commands, occupied=())`; consume a finite iterable of integer pairs
once before commands, isolating mutable inputs. Reuse validated immutable occupancy
without copying on subsequent runs. Duplicate cells have no additional effect.
Do not extend YAML's strict validation to legacy pose/command callers implicitly.

## Acceptance examples

| Initial pose | Occupied cells | Commands | Final pose | Outcomes |
|---|---|---|---|---|
| (0, 0, 0) | omitted or empty | RF | (1, 0, 1) | [True, True] |
| (0, 0, 0) | {(0, 1)} | FFRF | (1, 0, 1) | [False, False, True, True] |
| (0, 0, 0) | {(0, 1)} | FL | (0, 0, 3) | [False, True] |
| (0, 0, 0) | {(0, 0)} (proposed valid start) | FRRF | (0, 1, 2) | [True, True, True, False] |
| (0, 0, 3) | {(-1, 0)} | F | (0, 0, 3) | [False] |
| (0, 0, 0) | {(0, 1)} | empty | (0, 0, 0) | [] |

Load `examples/start.yaml`, then FFRF → (1, 0, 1) with
[False, False, True, True]; the second occupied cell [2, 3] does not affect this path.
After a blocked F, an unknown command still raises ValueError. Independent runs
do not share mutable state.

Structural failure examples: non-mapping root, wrong pose shape, missing required
field or `occupied: [[0, 1], [2]]` → clear startup failure, no commands consumed
and no configuration returned. A malformed final entry in 200,000 records must
likewise prevent the first move. Fix that entry and retry load → normal movement.
Test syntax and file-read errors at the same startup boundary. Value, duplicate,
extra-key and YAML-feature examples in the table become acceptance once resolved.

Scale acceptance: load a representative 200,000 distinct-cell document once,
record startup time and peak/retained memory, then exercise many blocked/free
moves and reuse the configuration without file reads or occupancy rebuilding.
No numeric latency or memory threshold is yet specified.
