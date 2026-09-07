# Current specification

Status: occupied cells and YAML initialization confirmed; implementation pending.
Sources: [original request](ORIGINAL.md), [occupied-cell request](OCCUPIED_REQUEST.md),
and [YAML request](YAML_REQUEST.md). Original source documents remain unchanged.
The YAML request supersedes the earlier exclusion of configuration-file input.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances
one cell unless its destination is occupied. Callers may supply fixed occupied
cells. An F into an occupied cell reports failure, preserves both position and
heading, and allows subsequent commands to execute. L/R still turn in place.
Return the final pose and per-command success. Unknown commands raise ValueError.
No routing, moving obstacles, or persistence of movement state is requested.

Load the starting pose and about 200,000 occupied cells from YAML once into memory,
then query that in-memory occupancy during movement. Invalid structure must fail
clearly before any movement. The supplied [example](../examples/start.yaml) has a
root mapping, a `pose` mapping containing `x`, `y`, `heading`, and an `occupied`
sequence of two-coordinate sequences. Commands are not present in that example.

For example, starting at (0, 0, 1) with (1, 0) occupied, F leaves the pose at
(0, 0, 1) and reports False. Continuing with LF turns north and moves to (0, 1, 0),
reporting True for each of those commands. Loaded from the example YAML, `FRF`
should return `((1, 0, 1), [False, True, True])`.

Detailed invalid-value and duplicate policies are expressly unresolved in the
YAML request. Proposed schema, API, dependency, ownership, and initial-occupancy
choices are in [the design](DESIGN.md#open-contract-decisions); these are not
additional user-confirmed requirements. Current code still has unconditional
forward movement and no YAML loading. See the [fresh baseline](evidence/yaml-baseline.md).
