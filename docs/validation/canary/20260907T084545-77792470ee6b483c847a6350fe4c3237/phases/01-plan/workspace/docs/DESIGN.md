# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Occupied-cell amendment D2

Status: proposed, not implemented or reviewed. D1 above remains accepted.
Requirements: [current spec](SPEC.md), sourced from
[the confirmed request](OCCUPIED_REQUEST.md).

Outcome: a blocked F returns False for that command, leaves the entire pose
unchanged, and allows later commands to run. Main choice: snapshot caller-supplied
cells into a local immutable set and check the target before updating pose.
This adds collection storage but keeps occupancy fixed throughout a run.
Scope: optional occupancy with existing two-argument calls preserved; no routing,
persistence, moving obstacles or configuration files. For example, an eastward
blocked F followed by LF yields [False, True, True] and (0, 1, north) from the
origin. Next step: [planned S1](PLAN.md), with these proposed decisions assessed
before implementation.

### Current code and public interface

[`navigator.py`](../navigator.py) keeps pose and outcomes local to `run`.
`_target` computes a candidate pose via `DIRECTIONS`; today every recognized
command appends True, and unknown commands raise ValueError.

Proposed signature: `run(pose, commands, occupied=())`, accepting a finite
iterable of `(x, y)` integer tuples. Return shape stays `(final_pose, outcomes)`.
Omitted or empty occupancy preserves existing behavior. No changes to heading
encoding, movement distances or unbounded coordinates are needed.

### Decisions and consequences

| Decision | Reason / alternative | Consequence | Example |
|---|---|---|---|
| Copy occupancy to a local `frozenset` at run entry | A borrowed mutable collection could change mid-session; repeated list scans cost more per move | Fixed snapshot, duplicate collapse, expected constant-time lookup; O(n) ingestion and O(u) storage for u unique cells | `[(1, 0), (1, 0)]` blocks the same cell once; caller data is not mutated |
| Test candidate coordinates before assigning pose; append False only for blocked F | Failure is a command result, so an exception or early return would break the confirmed continuation contract | Both position and heading remain unchanged; later commands execute normally | Blocked F then L still turns successfully |
| Keep D1 turns and unknown-command errors | Occupancy affects entry by F only | L/R succeed in place; unknown commands still raise ValueError, including after a blocked F | `F?` against a blocked target raises ValueError on `?` |

Proposed defaults, not user confirmations: an initially occupied position is
allowed because occupancy restricts entry, not starting state; turns and leaving
that cell work. Coordinates use the grid's existing integer tuple convention.
Malformed occupancy, infinite iterables and new pose validation are outside the
supported input contract; no new validation/error API is proposed. These defaults
need assessment with D2 but do not require additional machinery or scope.

### Acceptance and failure behavior

These expected results are derived from north=(0, 1), east=(1, 0), and L reducing
heading modulo four; they have not been verified against feature code.

| Pose / commands / occupied | Expected return or error |
|---|---|
| `(0, 0, 1)` / `F` / `{(1, 0)}` | `((0, 0, 1), [False])` |
| `(0, 0, 1)` / `FLF` / `{(1, 0)}` | `((0, 1, 0), [False, True, True])` |
| `(0, 0, 1)` / `FFR` / `{(1, 0)}` | `((0, 0, 2), [False, False, True])` |
| `(0, 0, 0)` / `RF` / omitted or empty | `((1, 0, 1), [True, True])` |
| `(0, 0, 1)` / `LF` / `{(0, 0)}` | `((0, 1, 0), [True, True])` under the proposed starting-cell default |
| `(0, 0, 1)` / `F?` / `{(1, 0)}` | ValueError on `?`; no normal return |

### Validation and remaining questions

Baseline inspection and successful existing checks are recorded in
[the evidence](evidence/occupied-baseline.md). Existing tests cover one turn/move
sequence, left wrap and an unknown command; they do not verify occupancy.
S1 should exercise the examples above, all movement directions including negative
coordinates, snapshot isolation from caller mutation during command iteration,
duplicate cells and separate runs with different occupancy. Check one outcome per
recognized command and no caller collection mutation.

No confirmed requirement is unresolved. Public API and edge-case defaults remain
proposals pending implementation review. Snapshot construction requires finite
input and memory proportional to unique cells; no large-data guarantee is added.
