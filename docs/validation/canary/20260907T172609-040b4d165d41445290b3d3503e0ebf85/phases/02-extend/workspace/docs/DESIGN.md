# YAML startup and occupied-cell extension to D1

Load and validate the complete YAML starting pose and occupied cells before
consuming movement commands, then retain occupancy as an immutable hash set of
coordinate pairs. About 200,000 cells justify expected constant-time membership
per forward move rather than scanning a list. This costs O(n) retained memory and
O(n) expected construction time; YAML parsing also creates temporary objects, so
peak startup memory exceeds the retained set. For [examples/start.yaml](../examples/start.yaml),
FFRF must produce (1, 0, 1) and [False, False, True, True]. A malformed last cell
must instead fail startup with its location, before even the first command is read.

Parser selection and exact value/duplicate rules remain unresolved; the proposed
contract and examples are in [SPEC](SPEC.md#proposed-yaml-contract-and-open-questions).
A maintained YAML parser is proposed, but conflicts with DEVNOTES' current
standard-library-only policy. Resolve that dependency boundary before implementing
YAML loading; no parser has been installed, selected or experimentally verified.

Decision: YAML loading, scale and early structural failure are
[confirmed](YAML_REQUEST.md); interface, representation and validation details
below are proposals. Preserve D1's accepted local state, direction lookup,
unbounded coordinates and ValueError for unknown commands. Sources:
[original](ORIGINAL.md), [occupied request](OCCUPIED_REQUEST.md), [target spec](SPEC.md).
Delivery and review status: [plan](PLAN.md#delivery-status). Historical text:
[before YAML](history/pre-yaml-documents.md), [accepted D1](history/pre-occupied-documents.md).

## Startup boundary and ownership

Propose a separate `load_start(path)` operation returning a validated immutable
starting configuration (pose plus occupancy), followed by
`run(config.pose, commands, config.occupied)`. Retain existing two-argument calls
and the proposed optional third occupied argument for programmatic users.
Commands stay caller-supplied; no CLI, YAML command field or hot reload is required.
The path-based loader reads exactly once per explicit load. Its result can be
reused for movement calls without rereading YAML or rebuilding occupancy. Pose is
local to each run; movement never modifies the saved starting configuration.

Build a private frozenset during startup and publish the configuration only after
the entire document passes validation. Reuse this immutable set in `run`; copy
other finite caller-supplied occupied iterables once before commands. This avoids
an O(n) copy on each run of a loaded map while isolating mutable caller inputs.
No global cache or shared mutable session is needed. The load-once guarantee is
per explicit configuration load, not an implicit process-wide cache.

A list would require O(n) membership for each move; a dense grid would conflict
with unbounded sparse coordinates. The hash set gives expected O(1) membership,
not a worst-case latency guarantee. Parsing and checking every input record,
including duplicates, takes work proportional to file input size. Release the
parsed YAML tree after successful conversion; do not retain both representations.
Streaming construction is deferred unless measured startup memory requires it.
No concrete memory or time budget was supplied, so 200,000-cell acceptance must
record measurements rather than claim an unmeasured bound.

## Validation, dependency and recovery

Use a maintained parser in a mode that does not construct arbitrary Python
objects, then separately validate the application schema. Safe parsing alone does
not enforce required fields, strict integers or duplicate-key policy. Confirm the
chosen parser can detect duplicate mapping keys before values are overwritten,
and specify its scalar/alias behavior through tests. Do not substitute JSON-only
loading or a handwritten YAML subset: the supplied example uses YAML block maps
and sequences, and silently narrowing YAML would change the input contract.
If standard-library-only remains required, parsing scope/approach remains blocked.
External guarantees have not been researched; this phase uses fixture evidence only.

Structural errors must include a useful field/index (for example
`occupied[199999]: expected [x, y]`); syntax errors should include file and line/
column when available. Propose ValueError for syntax/schema failures, keeping
file I/O failures distinguishable. Even an empty command stream must not suppress
configuration validation. No command iteration, pose activation or partial
configuration return occurs until startup succeeds. Parse/I/O/validation failure
leaves no new active configuration; an already loaded configuration remains usable.
Fixing the file and explicitly retrying load is safe because no movement or
persistent writes have happened. This is startup atomicity, not rollback of an
entire command stream: a later unknown command retains existing ValueError behavior.

## Movement and compatibility

Keep `run(pose, commands, occupied=())` and its return shape. Check only the
candidate forward destination from `_target`; collision appends False and
preserves the complete pose. Turns succeed and later commands continue. Repeated
blocked F commands still fail; turning and moving into a free cell allows progress.
By the existing proposed destination-only default, an occupied starting cell is
allowed and can be left, but re-entry fails. The YAML contract must explicitly
confirm or revise that default; it is not historically accepted validation behavior.

Strict startup validation applies to YAML. Do not silently impose new validation
on existing direct pose/command callers. Direct occupied iterables still support
integer pairs and proposed duplicate collapse; malformed direct occupancy remains
outside that proposed contract. Independent runs do not leak occupancy.

## Evidence and acceptance

Inspection shows `navigator.py` still adopts each forward target unconditionally;
its three tests cover turns/movement and unknown commands only. It has no loader,
occupancy index or dependency configuration. The supplied YAML is inspected as
text, not parsed with a newly installed library. Use the [spec examples](SPEC.md#acceptance-examples)
for behavior and failures. Verify immutable reuse, one-shot iterable snapshotting,
mutation isolation, and a representative 200,000-cell load followed by repeated
blocked/free moves without further I/O or full-map traversal. Baseline results
and pending checks live only in the plan.
