# Accepted design D3: stop a blocked batch

A blocked forward command preserves its incoming pose, emits False, and immediately
ends the batch, as confirmed in [STOP_REQUEST](STOP_REQUEST.md). Return only outcomes
for attempted commands. For (0,0,0), `FRF`, and occupied {(0,1)}, return (0,0,0) and
[False]. This replaces D2 continuation: callers can no longer expect one outcome
per supplied command or execution of a suffix after a block.

Keep local state and the occupied-set check before assigning pose. Successful
commands before a block remain applied; this is not rollback of the batch. For
`RFFL` with occupied {(2,0)}, starting at (0,0,0), return (1,0,1) and
[True, True, False]. Stop processing at the failed command, so even an unknown
command in the remaining suffix is unattempted. Attempted unknown commands still
raise ValueError. Turns and unblocked movement retain their behavior.

The returned pose remains usable for a later run. No stopped state persists between
runs; retrying a blocked F against the same occupied cells fails again, while a new
batch may turn and move away. Continuing after failure was the accepted D2 choice,
but would violate the newly confirmed batch boundary. There is no new routing,
persistence, moving obstacle, or configuration requirement.

Decision: accepted behavior from the confirmed stop request; implementation is
pending in [the delivery plan](PLAN.md). [Current contract and acceptance](SPEC.md)
derive from the [original](ORIGINAL.md), [occupied-cell](OCCUPIED_REQUEST.md), and
[stop](STOP_REQUEST.md) requests. Validation must distinguish a first-command block,
a block after successful movement/turns, an unattempted suffix, and a later run.

## Preserved accepted decisions and history

Accepted D1:
Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

Accepted D2 (historical continuation, superseded by D3): use a set for occupied coordinates; check before assigning pose.
A blocked F emits False and continues. For FRF with (0,1) occupied, finish at
(1,0,1) with [False, True, True].

The [prior document texts](history/d2-artifacts.md) and [D2 acceptance record](history/d2-review.md)
remain historical evidence; D1 and the D2 occupied-set/pose-preservation decisions
remain applicable.
