# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment D1.1

Status: proposed amendment; design review pending. D1 acceptance above remains
historical and does not cover this amendment.

Goal: callers can supply fixed occupied cells. Main choice: take a per-run set
snapshot and reject a forward target before changing pose. A blocked command
returns `False`; subsequent commands still run. Existing two-argument calls remain
compatible. For example, from `(0, 0, 1)` with `(1, 0)` occupied, `FRF` ends at
`(0, -1, 2)` with `[False, True, True]`.

Scope: movement blocking only; no routing, persistence, moving obstacles, or file
configuration. Next step: review this amendment and the [plan](PLAN.md), then
implement in a later task. Sources: [confirmed request](OCCUPIED_REQUEST.md) and
[specification addendum](OCCUPIED_SPEC.md).

### Current behavior and proposed interface

`navigator.run(pose, commands)` currently uses `_target` to commit every forward
move and appends `True` for each recognized command. `_target` and `DIRECTIONS`
already provide the candidate pose; they need no replacement. Turns update only
heading; unknown commands raise `ValueError("unknown command")`.

Proposed interface: `run(pose, commands, occupied=())`, accepting an iterable of
integer `(x, y)` tuples. Copy these into a local `frozenset` once before processing
commands. Pose, outcomes, and occupancy remain local to the run. The return shape
stays `(final_pose, outcomes)`. These interface details are proposed design choices,
not additional confirmed wording from the request.

### Decisions and consequences

| Decision | Reason / alternative | Consequence | Example |
|---|---|---|---|
| Snapshot coordinate tuples into a local `frozenset` | Repeated list scanning grows with the occupied collection; retaining a caller-owned mutable set would weaken fixed occupancy | O(n) construction and storage, expected O(1) membership per forward command; no mutation of caller input | Duplicate `(1, 0)` entries behave as one cell |
| Check candidate `(x, y)` before assigning pose | Reverting a committed move adds unnecessary state handling | Blocked forward preserves all three pose fields, appends `False`, and continues | `(0, 0, 1)`, `F`, occupied `{(1, 0)}` returns `((0, 0, 1), [False])` |
| Default occupancy is empty; turns bypass occupancy | Preserve D1 behavior and the explicit turn requirement | Existing callers retain results; only blocked forward commands produce `False` | A blocked `F` followed by `R` still rotates south |
| Occupancy constrains forward destinations only | Rejecting a supplied starting pose would introduce an unrequested restriction | A run may start on an occupied coordinate and leave it; this interpretation needs review | `(0, 0, 0)`, `F`, occupied `{(0, 0)}` reaches `(0, 1, 0)` |

### Acceptance, validation, and remaining decisions

The [addendum](OCCUPIED_SPEC.md#acceptance-examples) gives independently derived
examples for blocking, continuation, turns, and compatibility. Unknown commands
still raise rather than becoming failed movement outcomes. No new validation
contract is proposed for malformed poses or occupied entries; supported occupancy
entries are integer coordinate tuples. Native iterable/hashability errors may
occur while building the snapshot, before command consumption.

Existing tests pass, but none exercise occupancy; see [baseline evidence](evidence/occupied-baseline.md).
Implementation must add the decisive cases and run the complete standard-library
test suite. Review should assess the optional interface, snapshot choice, and
starting-cell interpretation. There is no unresolved confirmed-requirement blocker
to drafting the plan; these design choices remain proposed until reviewed.
