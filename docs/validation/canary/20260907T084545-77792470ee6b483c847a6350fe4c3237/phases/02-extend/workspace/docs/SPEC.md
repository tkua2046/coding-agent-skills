# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed extension: occupied cells (pending implementation)

Authority: [original request](ORIGINAL.md) and preserved
[confirmed occupied-cell request](OCCUPIED_REQUEST.md). The paragraph above
describes the implemented baseline; the following behavior is required next.

- Callers can supply fixed occupied cells.
- F into an occupied cell reports failure, preserving position and heading.
  The session continues accepting subsequent commands.
- Turns still work. Free forward moves retain existing behavior.
- Routing, persistence, moving obstacles and configuration files are out of scope.

Acceptance: starting at (0, 0, east), with (1, 0) occupied, F fails and leaves
(0, 0, east). A following L succeeds, then F succeeds to (0, 1, north).
The combined outcomes are [False, True, True].

The optional argument, collection ownership and edge-case defaults are proposed
engineering decisions in [the design](DESIGN.md#occupied-cell-amendment-d2);
they are not additional confirmed user requirements.

## Confirmed extension: YAML startup (pending implementation)

Authority: [preserved YAML request](YAML_REQUEST.md) and
[example input](../examples/start.yaml). This subsequent request supersedes the
configuration-file exclusion above; other movement requirements remain in force.

- Load the starting pose and about 200,000 occupied cells from YAML once into
  memory, then query occupancy during movement.
- Invalid structure must fail clearly before any movement.
- The supplied example uses `pose` with `x`, `y`, `heading` and an `occupied`
  sequence of coordinate pairs.

Acceptance: the example's north-facing pose `(0, 0, 0)` with `(0, 1)` occupied
makes F fail unchanged; L then F reaches `(-1, 0, 3)`. Outcomes: `[False, True, True]`.
A structurally malformed final occupied entry must fail loading before any command,
even if earlier entries are valid.

Detailed invalid-value and duplicate policies are explicitly undecided in the
source request. Required/extra fields, initial overlap, YAML document features,
loader interface and error details are [open design proposals](DESIGN.md#validation-and-remaining-questions),
not additional confirmed requirements. No implementation or dependency addition
is authorized in this documentation phase.
