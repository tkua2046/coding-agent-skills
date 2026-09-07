# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed occupied-cell extension

The following target behavior comes from [the confirmed request](OCCUPIED_REQUEST.md).
Delivery status is in [the plan](PLAN.md#delivery-status); this section does not
claim the extension is implemented.

A caller may supply fixed occupied cells. F targeting an occupied cell returns a
failure outcome for that command and preserves both position and heading. The
remaining commands are still processed. L/R continue to turn in place. Successful
commands return success outcomes, with one outcome per processed valid command.
No routing, persistence, moving obstacles or configuration file is added.

The proposed API and input conventions are in [the design](DESIGN.md). The
[original request](ORIGINAL.md) and [pre-extension spec](history/spec-before-occupied.md)
remain preserved sources.
