# Current design: stop on blocked forward movement

A blocked F ends the batch with its failure included in the returned outcomes.
Keep the pose immediately before that F and preserve earlier successful changes.
Checking the occupied target before assigning pose still protects position and
heading; end command processing after recording False. For (0,0,0), FRF and
occupied {(0,1)}, return ((0,0,0), [False]). Neither R nor the last F is attempted.

Decision: accepted public behavior in the [stop request](STOP_REQUEST.md).
The [current contract and acceptance examples](SPEC.md) define the result;
[delivery status and pending work](PLAN.md) remain planning only.

The result shape stays the same, but callers must now handle fewer outcomes than
input commands. Continuing after failure was accepted previously; it would now
violate the confirmed stop behavior. Outcomes describe only the attempted prefix,
including its terminal failure, rather than providing placeholders for the suffix.
The pending text adapter must reflect that prefix. An unknown command still raises
ValueError if reached, but a suffix after a blocked F is never processed.

No batch rollback is introduced: RFFL from (0,0,0) with {(2,0)} occupied retains
(1,0,1) and returns [True, True, False]. A later invocation is independent and may
turn and move from the returned pose. There is no persistent or external state to
recover. Fixed caller-supplied occupied coordinates remain a set checked before
movement; turns and unbounded coordinates are unchanged. No routing, persistence,
moving obstacles or configuration file is added.

Verified baseline: navigator.py continues after blocked F, and existing obstacle
tests assert continuation. The proposed implementation must change that behavior
and those expectations; validation uses the contract examples, including a failure
after successful commands and an unattempted suffix. No unresolved decision blocks
this local change.

## Preserved decisions and sources

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

D1 remains accepted. D2's occupied-set approach remains accepted; its continuation
behavior is superseded. Preserve the [original design](history/design-before-stop.md),
[D2 acceptance record](history/d2-review.md), [original request](ORIGINAL.md), and
[occupied-cell request](OCCUPIED_REQUEST.md) as historical sources.
