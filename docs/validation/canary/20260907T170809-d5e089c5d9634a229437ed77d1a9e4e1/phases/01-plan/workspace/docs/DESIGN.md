# Occupied-cell extension to D1

Add optional `occupied=()` to `run(pose, commands)` and snapshot the supplied
coordinate pairs into a frozen set once per run. Check the forward destination
before replacing the pose: an occupied target appends `False` and processing
continues. This preserves existing calls and prevents a failed move from partially
changing state. Snapshotting costs storage proportional to the distinct occupied
cells, but keeps occupancy fixed even if the caller changes its collection during
command iteration. For example, `run((0, 0, 0), "FFRF", occupied={(0, 1)})`
returns `((1, 0, 1), [False, False, True, True])`.

Decision: this interface and snapshot strategy are proposed implementation choices;
blocked-move behavior is confirmed by [the occupied request](OCCUPIED_REQUEST.md).
The [original requirements](ORIGINAL.md) and [current spec](SPEC.md) govern behavior.
See [the plan](PLAN.md) for execution status and the next delivery outcome.

## Accepted design D1 retained

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

The unchanged [D1 source](history/design-d1.md) is preserved for historical reference.

## Interface and state boundaries

- The proposed signature is `run(pose, commands, occupied=())`; both positional and
  keyword supply are supported. Omitted or empty occupancy preserves existing
  results, including the `(final_pose, outcomes)` return shape.
- Input is a finite iterable of hashable `(x, y)` integer-coordinate tuples.
  Duplicate cells have no additional effect. Coordinates remain unbounded.
  There is no new normalization or general input-validation layer; malformed
  occupancy is outside the supported contract. Snapshot construction happens
  before commands are consumed, so construction errors precede command execution.
- Caller collections are not modified. A fresh snapshot belongs to each call;
  retaining a live reference would let caller mutation violate fixed occupancy.
- Only entry into the forward destination is checked. An initial position listed
  as occupied is allowed: turning and moving out still work. This is a proposed
  convention consistent with the request's destination rule, not a new start-pose
  validation requirement.
- Occupied forward moves produce `False`; free forward moves and turns produce
  `True`. Unknown commands still raise `ValueError` and abort the call as before.
  Repeating a blocked forward move fails again without changing pose; turning can
  allow a subsequent forward move to succeed. No automatic rerouting occurs.

## Acceptance examples

These expected results follow the requested behavior and proposed conventions;
they are acceptance targets, not results from the current implementation.

| Input | Expected result |
|---|---|
| `run((0, 0, 0), "F", {(0, 1)})` | `((0, 0, 0), [False])` |
| `run((0, 0, 0), "FFRF", {(0, 1)})` | `((1, 0, 1), [False, False, True, True])` |
| `run((0, 0, 0), "LF", {(-1, 0)})` | `((0, 0, 3), [True, False])` |
| `run((0, 0, 0), "RF")`, also with empty occupancy | `((1, 0, 1), [True, True])` |
| `run((0, 0, 0), "RF", {(0, 0)})` | `((1, 0, 1), [True, True])` |
| `run((2, 3, 0), "", {(2, 4)})` | `((2, 3, 0), [])` |
| `run((0, 0, 0), "F?", {(0, 1)})` | Raises `ValueError` after the blocked command; blockage does not stop processing. |

Validation should also cover blocking in all four headings, a finite one-shot
occupancy iterable with duplicates, independent runs, and caller mutation during
command iteration to establish snapshot isolation. No external guarantees or
dependencies are needed; no material blocking decision remains for this local plan.
