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
No routing, persistence or moving obstacles are added. The earlier exclusion of
configuration files is superseded by the YAML request below; the original source
text remains unchanged.

The proposed API and input conventions are in [the design](DESIGN.md). The
[original request](ORIGINAL.md) and [pre-extension spec](history/spec-before-occupied.md)
remain preserved sources.

## Confirmed YAML extension

The [YAML request](YAML_REQUEST.md) requires loading the starting pose and about
200,000 occupied cells from YAML once into memory for queries during movement.
Invalid structure must fail clearly before any movement. The supplied
[example](../examples/start.yaml) has a `pose` mapping with `x`, `y`, and `heading`
and an `occupied` sequence of coordinate pairs. With that input, command `F`
must fail at `(0, 0, 0)` because `(0, 1)` is occupied; `R` followed by `F` can
then reach `(1, 0, 1)`.

Detailed invalid-value and duplicate policies are explicitly unchosen in the
request. The [design's contract questions](DESIGN.md#unresolved-contract-questions)
record proposals, including the parser-policy conflict, without treating them
as confirmed requirements. Loading configuration does not add saving, hot reload,
routing, moving obstacles, or commands embedded in YAML. Existing direct callers
and navigation behavior remain in scope for compatibility.
