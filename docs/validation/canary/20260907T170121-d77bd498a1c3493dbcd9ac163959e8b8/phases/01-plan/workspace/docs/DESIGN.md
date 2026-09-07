# Design: navigation with fixed occupied cells

Status: D1 remains accepted; the occupied-cell amendment below is proposed,
with design review pending. Requirements: [original](ORIGINAL.md),
[confirmed request](OCCUPIED_REQUEST.md), and [spec addendum](SPEC_OCCUPIED.md).

Add caller-supplied fixed occupied cells while preserving movement and turns.
Snapshot coordinate pairs per run and check the forward target before assigning
pose: a blocked move returns `False`, preserves position and heading, and lets
later commands run. This is a small local extension, suitable for one delivery
stage. Next: perform the requested amendment review and [plan review](PLAN.md);
implementation is deferred to a later task.

## Occupied-cell amendment (proposed)

Current `navigator.run(pose, commands)` calls `_target` for every `F`, changes pose,
and appends `True`. `_target` already computes the candidate pose without mutating
state. Retain that movement calculation and the existing turn/error branches.

Propose `run(pose, commands, occupied=())`, accepting an iterable of integer
coordinate tuples `(x, y)`. Existing two-argument calls retain their behavior and
return shape. Copy the coordinates to a local immutable set before processing
commands. This gives expected constant-time membership checks at a one-time
linear construction and storage cost; duplicates collapse naturally. Repeated
linear scans would avoid set storage but scale with both commands and occupied
cells. A snapshot also prevents caller collection edits during command iteration
from changing this run's obstacles. No new dependency or session abstraction is
needed.

On `F`, check only the candidate `(x, y)`, independent of heading. If occupied,
append `False` and keep the entire pose. Otherwise assign the candidate and
append `True`. Turns always append `True`. Unknown commands still raise
`ValueError("unknown command")`; they do not become ordinary movement failures.
All state remains local to the run and the caller's occupied collection is not
mutated.

Interface defaults and edge behavior are proposals, not additional confirmed
user requirements: an omitted collection is empty; an occupied starting cell
does not reject the run or prevent turning/leaving, because the rule checks entry
into the target cell. Valid integer coordinate tuples are the input contract;
new validation or specified errors for malformed occupancy are outside this
amendment. Review these choices with the amendment; no inspected-code uncertainty
blocks planning.

## Acceptance and validation

The [spec addendum](SPEC_OCCUPIED.md#acceptance-examples) owns concrete expected
outputs, including a blocked eastward move followed by turning and successful
movement. Verify unchanged heading on a blocked move, continuation, all heading
directions, empty/default compatibility, independent runs, and snapshot ownership.
Keep existing unknown-command behavior, including after a blocked command.

The [baseline evidence](evidence/occupied-baseline.md) records three passing
existing tests; none exercises occupancy. All occupied-cell checks and both
document reviews remain pending. No routing, persistence, moving obstacles,
configuration file, board bounds, or CLI is introduced.

## Accepted design D1 (preserved)

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.
