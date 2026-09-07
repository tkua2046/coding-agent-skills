# Navigation design: occupied-cell amendment to D1

Status: D1 remains accepted; this amendment is proposed, with design review
pending. Add caller-supplied fixed occupied cells while preserving pose on a
blocked forward command and continuing the run. Use a per-run occupancy snapshot
and check the forward destination before assigning pose. The consequence is a
failed-command outcome rather than an exception for a blocked move. Next: review
this amendment and the [plan](PLAN.md); implementation is a later task.

This is one local extension with no new dependency or independent design lifecycle.
The [confirmed request](OCCUPIED_REQUEST.md) and
[specification addendum](OCCUPIED_SPEC.md) define scope and acceptance.

## Proposed amendment

Extend the public interface to `run(pose, commands, occupied=())`, retaining all
two-argument calls. Accept a finite iterable of integer `(x, y)` tuples and copy
it into a set once per run. This keeps ownership local, deduplicates cells, and
prevents subsequent caller mutation from changing the fixed snapshot. Expected
lookup cost is constant per forward command, with construction time and storage
linear in the supplied cells. Scanning the supplied collection for each move
would avoid the copy but repeat work and leave mutable caller state live.

For `F`, compute the candidate with the existing `_target`; test only its `(x, y)`.
If occupied, append `False` and leave the entire pose untouched. Otherwise assign
the candidate and append `True`. Process the next command in either case. `L`
and `R` still turn in place successfully, regardless of occupancy. Unknown
commands still raise `ValueError`; blocking does not change that error contract.
No global state, routing, board bounds, persistence, or configuration is added.

The optional argument, snapshot policy, and treatment of a starting cell listed
as occupied are proposed defaults, not additional confirmed user requirements.
The destination-only rule permits departure from such a starting cell; it does
not add initial-pose rejection. Input validation beyond the documented valid
integer-pair domain remains outside this change, consistent with the existing
pose API. No unresolved choice prevents drafting the plan; these defaults remain
subject to the pending review.

## Acceptance and validation

From `(0, 0, 1)`, commands `FRF`, occupied `{(1, 0)}` must return
`((0, -1, 2), [False, True, True])`: east is blocked, right turns south, and the
next forward succeeds. A single blocked `F` must return the original position
and heading with `[False]`. Omitted or empty occupancy preserves existing
results. See the [addendum](OCCUPIED_SPEC.md) for additional boundary examples.

Inspection found that `run` currently assigns `_target(pose)` unconditionally
and appends `True` after every recognized command. The existing three tests pass
but do not exercise occupancy; [baseline evidence](evidence/occupied-baseline.md)
records the actual check and its limits. Proposed verification belongs with the
single delivery stage in the plan. No occupied-cell implementation or design
review has been performed in this phase.

## Accepted design D1 (preserved)

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.
