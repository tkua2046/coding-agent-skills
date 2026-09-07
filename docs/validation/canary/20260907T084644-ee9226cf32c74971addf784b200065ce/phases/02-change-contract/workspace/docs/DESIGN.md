# Navigator design

Status: D1 and D2 were accepted previously; D3 records the confirmed
[stop request](STOP_REQUEST.md), with implementation and validation pending.
Goal: stop a batch on its first blocked forward move and return only attempted
outcomes. Preserve the pose at the failure and earlier successful work. This changes
public continuation behavior and can shorten the outcome list. Next: implement the
navigator change before exposing outcomes in the pending text adapter.

Sections: [retained decisions](#accepted-design-d1), [historical D2](#accepted-design-d2-historical),
[current amendment](#d3-stop-on-block), [validation](#validation-and-status).

## Accepted design D1
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Accepted design D2 (historical)

Accepted D2: use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].

This is the previously accepted behavior, preserved with its
[review record](history/d2-review.md). D3 supersedes continuation and this example;
the occupancy lookup and pose-preservation decisions remain in force.

## D3: stop on block

**Decision →** Append the blocked command's False outcome and end batch execution
immediately, returning the current pose and accumulated outcomes.
**Reason →** The subsequent user confirmation supersedes D2 continuation.
**Consequence →** Commands after the failure have no effects or outcomes; even an
unknown command in that suffix is unattempted. Earlier successful commands remain
effective. The `run(pose, commands, occupied=())` interface and return shape are
unchanged, but callers must accept a shorter outcome list. The text adapter must
display only returned outcomes. **Example →** From `(0, 0, 0)`, `FRF` with
`{(0, 1)}` returns `((0, 0, 0), [False])`.

Continuing after failure was the accepted alternative in D2; it no longer satisfies
the confirmed contract. Rolling back the entire batch would discard valid earlier
commands and does not preserve the pose immediately before the blocked move.
For example, `RFFL` from `(0, 0, 0)` with `{(2, 0)}` returns
`((1, 0, 1), [True, True, False])`.

State and the occupied-coordinate set remain local to each call. Check the target
before assigning pose, so failure preserves both position and heading. Successful
movement, turns, and errors on attempted unknown commands retain their rules.

## Validation and status

The authoritative [acceptance examples](SPEC.md#acceptance) cover immediate failure,
failure after prior successes, westward negative coordinates, successful/empty
batches, and attempted versus unattempted unknown commands. Update the obsolete
continuation regression and verify these behaviors during implementation. Adapter
integration must show one failure for the decisive FRF case and omit suffix results.

Inspection verified that `navigator.py` still continues after blockage and the
existing FRF test expects D2 behavior; no text adapter exists in this fixture.
No runtime behavior was changed or tested in this planning phase. No unresolved
decision blocks D3; adapter presentation details remain for its stage. Prior
[maintenance evidence](MAINTENANCE.md) concerns its captured candidate and does not
verify or approve D3. No routing, persistence, or configuration scope is added.
