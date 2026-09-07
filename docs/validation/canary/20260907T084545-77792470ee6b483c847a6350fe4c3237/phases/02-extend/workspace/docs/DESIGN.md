# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment D2

Status: proposed, amended for YAML; not implemented or reviewed. D1 above remains
accepted. Requirements: [current spec](SPEC.md), [occupied-cell source](OCCUPIED_REQUEST.md)
and [subsequent YAML source](YAML_REQUEST.md); shape example: [start.yaml](../examples/start.yaml).

Outcome: load the starting pose and about 200,000 occupied cells once; reject
invalid structure clearly before movement. A blocked F returns False, preserves
the whole pose and allows later commands. Main choice: fully validate input before
publishing a configuration with an immutable coordinate set, reused for movement.
Expected lookup is O(1); loading is O(n), with significant temporary parser memory.
The example file followed by FLF yields `((−1, 0, 3), [False, True, True])`.
YAML input supersedes the earlier configuration-file exclusion. Routing, output
persistence and moving obstacles remain outside scope. Next: resolve the contract
questions below and assess this amendment before the pending [plan](PLAN.md).

Outline: [interface](#current-code-and-public-interface),
[choices](#decisions-and-consequences), [acceptance](#acceptance-and-failure-behavior),
[validation and questions](#validation-and-remaining-questions).

### Current code and public interface

[`navigator.py`](../navigator.py) currently exposes only `run(pose, commands)`.
F always moves via `_target`; recognized commands append True; unknown commands
raise ValueError. No occupancy or input validation exists yet. README and DEVNOTES
continue to describe this implemented, standard-library-only baseline.

Proposed interfaces: preserve `run(pose, commands, occupied=())` from the earlier
D2 proposal and add `load_start(path)` returning a validated configuration with
`pose` and `occupied`. A caller loads once, then supplies those values to `run`;
commands remain caller-supplied, outside the YAML document. No CLI is implied.
These interface names and the path-based entry point are proposals, not confirmed
requirements. Return shape from `run` stays `(final_pose, outcomes)`.

The example establishes a root mapping with `pose: {x, y, heading}` and an
`occupied` sequence of two-element coordinate sequences. Proposed strict schema:
require both root fields and all pose fields, disallow extra fields, require
integers excluding booleans, and constrain heading to 0–3. Empty `occupied: []`
is valid. Missing/null fields, wrong container shapes and wrong cell lengths
fail before any command is consumed. Value, duplicate and unknown-key policies
remain open below; the example alone does not settle them.

### Decisions and consequences

| Decision | Reason / alternative | Consequence | Example |
|---|---|---|---|
| Parse and validate the entire configuration before returning it or iterating commands | Lazy per-move validation could discover bad data after changing pose | No partially usable configuration escapes; even invalid data late in the file prevents movement | A malformed final cell prevents an earlier free F from running |
| Build one `frozenset` of coordinate tuples at load time; retain it for membership queries | Scanning 200,000 entries for every F costs O(n) per query; reparsing/rebuilding per move defeats load-once | Expected O(1) membership, O(n) build time, O(u) retained storage for u unique cells; immutable data can be shared across runs, with pose/outcomes local to each run | Repeated F into `(0, 1)` queries the same set without file reads |
| Reuse validated immutable occupancy in `run`; snapshot other finite caller iterables once at entry | Always copying the loaded collection would add avoidable ingestion; borrowing mutable lists permits changes during a session | Existing two-argument calls work; direct mutable input cannot change occupancy mid-run. YAML structural guarantees belong to the loader, not arbitrary direct Python calls | Changing the source list during command iteration cannot unblock its snapshotted cell |
| Use a maintained YAML parser in safe/data-only mode, followed by explicit schema validation; package/version still undecided | Python has no standard-library YAML parser; a handwritten subset risks rejecting valid YAML or misinterpreting scalars | Future dependency and DEVNOTES policy changes are needed; no dependency is selected, installed or imported in this phase. Safe parsing alone does not validate schema | A custom object tag fails at load time; a safely parsed scalar root also fails |
| Convert loader failures to a clear proposed `ValueError` contract with file and field/index context, retaining cause | Raw parser exceptions or downstream tuple-unpack errors obscure the bad input | Read, syntax and structure errors stop loading; parser line/column should be included when available, exact wording need not be frozen | `start.yaml: occupied[199999]: expected two coordinates` |
| Test candidate coordinates before assigning pose; append False only for blocked F | An exception or early return would break confirmed continuation | Position and heading remain unchanged; later commands run normally | Blocked F then L still turns |
| Keep D1 turns and unknown-command errors | Occupancy restricts forward entry only | L/R succeed in place; unknown commands still raise ValueError, including after a blocked F | `F?` against a blocked target raises on `?` |

Loading is a startup boundary, not a cache or reload service. Editing/removing the
file after a successful load cannot affect that configuration. Intermediate YAML
lists/maps and mutable builders must be released after normalization; peak memory
can exceed the retained set substantially. About 200,000 cells is a sizing target,
not a confirmed maximum. Streaming parsing, custom indexes and hard size limits
are not justified yet; measure before adding them. Hash lookup is expected, not
worst-case, constant time.

### Acceptance and failure behavior

Hand-derived expectations below are proposed checks, not feature execution results.
Headings are north=0, east=1, south=2, west=3.

| Input / commands | Expected result or failure |
|---|---|
| Load `examples/start.yaml`; run `FLF` | First F is blocked at `(0, 1)`; L faces west; F reaches `(-1, 0, 3)` with `[False, True, True]` |
| `(0, 0, 1)` / `FLF` / `{(1, 0)}` | `((0, 1, 0), [False, True, True])`, retaining original occupied acceptance |
| `(0, 0, 1)` / `FFR` / `{(1, 0)}` | `((0, 0, 2), [False, False, True])` |
| `(0, 0, 0)` / `RF` / omitted or empty occupancy | `((1, 0, 1), [True, True])` |
| `(0, 0, 1)` / `F?` / `{(1, 0)}` | ValueError on `?`; no normal return |
| Empty file, scalar root, `pose: []`, or `occupied: [[0, 1, 2]]` | Clear loader error with source/context; no configuration returned and no commands consumed |
| Valid prefix followed by malformed YAML or a final cell `[2]`; commands start with F | Entire load fails before F, regardless of whether that cell would be queried |
| Valid empty occupancy plus a negative-coordinate pose | Load succeeds under proposed strict schema; unbounded-grid movement retained |
| 200,000 unique cells `[(i, 1) for i in range(200000)]`, pose `(0, 0, 0)`, commands `FFRF` | `((1, 0, 1), [False, False, True, True])`; configuration retained once and no parsing/building during movement |

Conditional cases require contract answers: duplicate `[[0, 1], [0, 1]]` either
loads as one occupied cell or fails at the second entry; an occupied starting cell
either fails loading or allows turns and departure. If allowed, `(0, 0, 1)` /
`LF` / `{(0, 0)}` returns `((0, 1, 0), [True, True])`.

### Validation and remaining questions

Verified: current code inspection and all three existing tests pass in this fresh
context; see [YAML baseline](evidence/yaml-baseline.md). Preserve the earlier
[occupied baseline](evidence/occupied-baseline.md) and historical S0 record.
Neither baseline verifies occupancy, YAML, memory use or performance.

Proposed verification includes the acceptance rows, all movement directions,
negative coordinates, caller-mutation isolation and independent run state. Use
an observable command iterator to prove failed loading consumes no commands.
Measure startup time and peak/retained memory for a generated 200,000-cell fixture,
then time repeated free/blocked queries separately. Verify no I/O or set rebuilding
in movement, without a brittle timing threshold. Record runtime/parser versions
and input size; no latency or memory budget has been supplied.

Contract questions remain open; recommendations are not confirmations:

- **Duplicates:** recommend collapsing occupied duplicates for set semantics;
  rejecting them instead catches authoring mistakes. `[[0, 1], [0, 1]]` distinguishes
  these choices. Duplicate mapping keys such as two `pose.x` entries are different:
  recommend rejection before a parser silently overwrites one value.
- **Starting cell:** retain the earlier proposed allowance, or reject overlap?
  With pose `(0, 0, 0)` and occupied `[[0, 0]]`, allowance permits turns/departure;
  rejection prevents any commands.
- **Values and schema flexibility:** recommend strict integer types, heading 0–3,
  required fields and no extra keys. Should `x: true`, `x: "2"`, `heading: north`,
  `heading: 4`, missing `occupied`, or extra `commands: F` fail or be normalized?
  Coercion/defaulting must not be silently inferred from the example.
- **YAML document features:** recommend exactly one document, rejecting duplicate
  mapping keys and merge keys. Should anchors/aliases be accepted as equivalent
  data or rejected? For example, two cells referencing `&cell [0, 1]` interact with
  the duplicate policy. Reject cyclic/nonconforming structures clearly. Parser
  selection must demonstrate agreed behavior; safe mode alone is insufficient.
- **Integration and errors:** does a library `load_start(path)` meet the input
  contract, or is a CLI required? Should a missing file raise the proposed contextual
  ValueError or preserve OSError? These choices affect callers and usage examples.

Resolve dependent policies before implementing their acceptance checks. Dependency
selection and measurable resource budgets remain engineering follow-ups; this
phase has neither installed a parser nor performed a design/plan review.
