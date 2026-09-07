# Preserved D2 artifacts

Captured before the planning revision for [STOP_REQUEST](../STOP_REQUEST.md).
These are the prior document texts, retained as historical context for the
[D2 acceptance record](d2-review.md), not a new review or execution claim.

## Prior SPEC.md

```markdown
# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.
Occupied forward targets report False, preserving pose; the batch continues.
```

## Prior DESIGN.md

```markdown
# Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].
```

## Prior PLAN.md

```markdown
# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

Complete: occupied cells with preserved pose and batch continuation (D2).
Pending: expose batch outcomes in the text adapter; dependency: agreed batch
contract. Acceptance: FRF with (0,1) occupied displays failure then two successes.
Check the navigator suite and proposed adapter integration test before review.
```
