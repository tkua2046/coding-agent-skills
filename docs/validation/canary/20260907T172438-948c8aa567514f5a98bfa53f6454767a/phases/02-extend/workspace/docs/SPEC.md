# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed extension: occupied cells (pending implementation)
Authority: [confirmed request](OCCUPIED_REQUEST.md); the [original request](ORIGINAL.md)
remains unchanged. Callers can supply fixed occupied cells. F into an occupied
cell returns a failure outcome and preserves both position and heading. Processing
continues with the next command. L/R still turn in place. No routing, persistence,
moving obstacles, or configuration file is included.

The existing final-pose/per-command-success return contract continues: a blocked
F contributes False; successful moves and turns contribute True. Unknown commands
still raise ValueError. With no occupied cells, existing behavior is preserved.
The proposed API and acceptance examples are in [the design](DESIGN.md).

## Confirmed extension: YAML startup (pending implementation)
Authority: [subsequent request](YAML_REQUEST.md), with shape illustrated by
[start.yaml](../examples/start.yaml). Load starting pose and about 200,000 occupied
cells from YAML once into memory for movement queries. Invalid structure must fail
clearly before any movement. This supersedes the earlier configuration-file
exclusion; the original source requests are preserved.

Detailed invalid-value and duplicate policies have not been chosen. Parser/dependency
policy, schema details, occupied-start behavior and invocation proposals remain
[open in the design](DESIGN.md#open-contracts), not confirmed requirements. The
occupied-cell outcomes and original movement contract above continue to apply.
