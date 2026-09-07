# Occupied-cell specification addendum

Status: request behavior confirmed; interface and boundary interpretations proposed
for review. This addendum extends [SPEC.md](SPEC.md) while preserving the verbatim
[original request](ORIGINAL.md) and [occupied-cell request](OCCUPIED_REQUEST.md).

Fixed caller-supplied occupied cells block forward destinations. A blocked forward
command reports failure and leaves both position and heading unchanged. The same
run continues accepting commands, and turns still work. Routing, persistence,
moving obstacles, and configuration files are outside scope.

Proposed contract details from [D1.1](DESIGN.md#occupied-cell-amendment-d11):
`run(pose, commands, occupied=())` accepts an iterable of integer coordinate tuples,
snapshots occupancy at entry, and keeps the existing return shape. Each recognized
command contributes one Boolean: blocked `F` is `False`; successful `F`, `L`, and
`R` are `True`. Omitted or empty occupancy preserves existing behavior. Occupancy
does not reject the starting pose. These choices are not claimed as reviewed.

## Acceptance examples

Headings remain north=0, east=1, south=2, west=3. These expected values are derived
from grid directions, not from an implementation of the amendment.

| Initial pose | Commands | Occupied cells | Expected result |
|---|---|---|---|
| `(0, 0, 1)` | `F` | `{(1, 0)}` | `((0, 0, 1), [False])`: position and heading unchanged |
| `(0, 0, 1)` | `FFRF` | `{(1, 0)}` | `((0, -1, 2), [False, False, True, True])`: repeated blocking followed by recovery |
| `(0, 0, 1)` | `FLF` | `{(1, 0)}` | `((0, 1, 0), [False, True, True])`: left turn also remains usable |
| `(0, 0, 0)` | `RF` | omitted or empty | `((1, 0, 1), [True, True])`: backward compatibility |
| `(0, 0, 0)` | `F` | `{(0, 0)}` | `((0, 1, 0), [True])`: proposed starting-cell interpretation |
| `(0, 0, 1)` | empty | `{(1, 0)}` | `((0, 0, 1), [])` |
| `(0, 0, 1)` | `F?` | `{(1, 0)}` | Raises `ValueError("unknown command")`; no normal result returned |

Caller collections must not be modified. Duplicates have no extra effect; negative
and distant coordinates retain the unbounded grid semantics. A mutation to the
caller collection during command iteration must not change the entry snapshot.
No custom error behavior for malformed occupied entries is specified. Review of
these proposed details and of the design/plan remains pending.
