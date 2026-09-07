# Navigator design

Current goal: support caller-supplied fixed occupied cells while retaining D1.
Status: occupied-cell amendment proposed; implementation has not started.
Use a per-run immutable occupancy snapshot and check the destination before
changing pose. A blocked F produces False with no pose change; later commands run.
This adds storage proportional to occupied cells and preserves existing two-argument
calls. Next step: the single pending outcome in [the plan](PLAN.md).

Sources: [original](ORIGINAL.md), [confirmed request](OCCUPIED_REQUEST.md),
[current specification](SPEC.md). Baseline checks: [evidence](evidence/occupied-baseline.md).

## Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment

Inspection: `navigator.run(pose, commands)` currently assigns `_target(pose)` on
every F and appends True for every recognized command. The three existing tests
exercise movement, a left turn wrapping to west, and unknown-command rejection;
none exercises occupancy. Keep the direction lookup and turn logic.

Propose `run(pose, commands, occupied=())`, accepting an iterable of integer
coordinate pairs represented as `(x, y)` tuples. Snapshot it as a frozenset at
entry, owned by that invocation. This consumes a supplied iterable once, ignores
duplicates, prevents later caller collection changes from affecting the run, and
provides expected constant-time membership checks. Direct membership in the
caller's collection would avoid a copy but could change during execution and
would be linear for lists. No dependency or new session abstraction is needed.

For F, compute the candidate pose using the existing translation, then test only
its `(x, y)` against occupancy. If occupied, append False and retain the entire
old pose; otherwise adopt the candidate and append True. Turns append True and
do not consult occupancy. Each recognized command yields exactly one boolean in
order. Unknown commands continue to raise ValueError, including after a blocked
move, rather than returning a partial result.

Proposed input convention: occupancy constrains entry by F, so an initial pose on
an occupied cell is allowed; turns and leaving for a free cell still work.
Occupancy may include any integer coordinates, including negative ones. As with
the existing pose API, this change does not introduce a comprehensive validation
contract for malformed inputs. These are design assumptions, not confirmed new
requirements; no blocker was found for the stated valid-input use case.

### Acceptance and validation

These expected results are derived from the heading convention, not a new
implementation. All occupied-cell checks below remain proposed.

| Input | Expected result |
|---|---|
| Pose (0, 0, 1), occupied {(1, 0)}, F | ((0, 0, 1), [False]) |
| Same pose and occupancy, FRF | ((0, -1, 2), [False, True, True]) |
| Same pose and occupancy, FFL | ((0, 0, 0), [False, False, True]) |
| Pose (0, 0, 0), occupied {(0, -1)}, LLF | ((0, 0, 2), [True, True, False]) |
| Pose (0, 0, 1), occupied {(0, 0)}, F | ((1, 0, 1), [True]) under the proposed entry-only convention |
| Pose (0, 0, 1), occupied {(1, 0)}, F? | ValueError; no returned final result |
| Existing calls with omitted or empty occupancy | Same poses and outcomes as baseline |

Extend the standard-library suite to cover these invariants, free moves in all
headings, iterable/duplicate occupancy and isolation from caller mutation during
command iteration. Preserve existing regression checks. This phase verifies only
the baseline; feature acceptance requires implementation and the planned checks.
