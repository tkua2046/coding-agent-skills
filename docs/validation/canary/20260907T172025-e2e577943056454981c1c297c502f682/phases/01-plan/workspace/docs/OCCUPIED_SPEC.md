# Occupied-cell specification addendum

Status: requested behavior confirmed by [OCCUPIED_REQUEST](OCCUPIED_REQUEST.md);
API defaults below are proposed and await design review. This addendum describes
the intended extension to [current behavior](SPEC.md), not shipped behavior.
[Original requirements](ORIGINAL.md) and historical reports remain unchanged.

Confirmed behavior: callers supply fixed occupied cells. Forward movement into
one returns a failed per-command outcome and preserves both position and heading.
The run continues accepting commands; turns remain successful. Unknown commands
retain the original `ValueError` behavior. Routing, persistence, moving obstacles,
and configuration files are excluded.

Proposed API defaults: `run(pose, commands, occupied=())` accepts a finite iterable
of integer coordinate tuples. Omission and an empty iterable mean no occupied
cells. Occupancy is snapshotted at run entry; duplicate cells have no additional
effect. Only forward destinations are checked, so a pose may start in a listed
cell and leave it. Invalid occupancy inputs are outside the supported domain;
this amendment does not specify a new validation/error API.

## Acceptance examples

Outcomes follow command order; every recognized command contributes one boolean.

| Pose; commands; occupied cells | Expected return or error |
|---|---|
| `(0, 0, 1)`; `F`; `{(1, 0)}` | `((0, 0, 1), [False])` |
| `(0, 0, 1)`; `FRF`; `{(1, 0)}` | `((0, -1, 2), [False, True, True])` |
| `(0, 0, 1)`; `FFL`; `{(1, 0)}` | `((0, 0, 0), [False, False, True])` |
| `(0, 0, 0)`; `RF`; omitted or empty | `((1, 0, 1), [True, True])` |
| `(0, 0, 0)`; `F`; `{(0, 0)}` | `((0, 1, 0), [True])` under the proposed starting-cell default |
| `(0, 0, 1)`; `F?`; `{(1, 0)}` | `ValueError` at `?`; the blocked move does not terminate command processing |
| `(2, 3, 3)`; empty commands; any valid occupancy | `((2, 3, 3), [])` |

Also verify north/east/south/west destinations `(0, 1)`, `(1, 0)`, `(0, -1)`,
`(-1, 0)` from the origin: blocking the relevant destination preserves its
initial heading. For snapshot ownership, mutating the caller's collection during
command iteration must not alter that run's blocked destinations; a later call
uses its own supplied snapshot. Iterable and duplicate inputs must obey the same
membership behavior as a set. These checks are planned, not executed.
