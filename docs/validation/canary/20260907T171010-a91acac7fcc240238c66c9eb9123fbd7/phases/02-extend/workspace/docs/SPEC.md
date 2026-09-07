# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.

## Confirmed occupied-cell extension (pending implementation)

Authority: [original request](ORIGINAL.md) and [confirmed extension](OCCUPIED_REQUEST.md).
The paragraph above describes the implemented baseline; this extension is confirmed
behavior to deliver, not a claim that the code already supports it.

The caller supplies fixed occupied cells. An F whose destination is occupied
returns failure for that command, preserves position and heading, and allows the
remaining commands to execute. L and R continue to turn in place successfully.
There is no routing, persistence, moving-obstacle support or configuration file.
Final pose and per-command outcomes remain the return contract; unknown commands
still raise ValueError.

For example, from (0, 0, 1), with occupied cell (1, 0), F returns
((0, 0, 1), [False]). With the same inputs, FRF returns
((0, -1, 2), [False, True, True]): the blocked eastward move does not prevent
turning south and moving. With no occupied cells, existing behavior is preserved.

The optional API argument, lookup representation and valid-input conventions are
proposed engineering choices in [the design amendment](DESIGN.md#occupied-cell-amendment),
not additional caller-confirmed requirements.

## Confirmed YAML extension (pending implementation)

Authority: [subsequent YAML request](YAML_REQUEST.md), with shape illustrated by
[examples/start.yaml](../examples/start.yaml). Starting pose and approximately
200,000 occupied cells are loaded from YAML once into memory and queried during
movement. Invalid structure must fail clearly before any movement.

This supersedes the earlier exclusion of configuration-file input above; the
original request text remains preserved. Blocked-forward behavior, turning,
unbounded coordinates, final pose/outcomes and unknown-command errors remain.
Detailed invalid-value and duplicate policies are explicitly unresolved. The
loader interface, exact schema/error rules, dependency and lookup choices in
[the revised design](DESIGN.md) remain proposed until settled; the sample alone
does not define all valid YAML inputs. No YAML implementation is present yet.
