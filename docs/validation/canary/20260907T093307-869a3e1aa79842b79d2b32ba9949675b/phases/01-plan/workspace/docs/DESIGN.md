# Design: fixed occupied cells

Status: local extension proposed; D1 remains accepted. The
[confirmed request](OCCUPIED_REQUEST.md) requires blocked forward moves to fail
without changing the pose, while the session and turns continue. Add an optional
occupied-cell input and check destinations before replacing the pose. A copied
lookup keeps occupancy fixed during a run and preserves existing two-argument
calls. Next step: the single pending outcome in [the plan](PLAN.md).

## Accepted design D1 (preserved)

Keep state local to each run; no global session. A caller supplies pose and commands.
A direction lookup supports translation; turns only affect heading. Unbounded
coordinates avoid imposing a board size. Unknown commands are programmer errors.

## Proposed extension and consequences

Inspection of [navigator.py](../navigator.py) shows that `_target` already computes
a candidate pose without mutation; `run` currently accepts every F and appends
True for every recognized command. Keep that translation and turning design.
For F, inspect the candidate's (x, y) before updating pose. If occupied, append
False and continue; otherwise accept the candidate and append True. L/R continue
to report True. An unknown command still raises ValueError rather than returning
a failure outcome.

Proposed public interface: `run(pose, commands, occupied=())`, accepting an
iterable of integer coordinate tuples `(x, y)`. Omitting occupancy, or supplying
an empty iterable, preserves existing results. Copy the iterable once into a
local immutable set before processing commands; duplicates collapse, caller
collections are not mutated, and later changes to them cannot affect this run.
This costs O(k) setup time and storage with expected constant-time membership.
Scanning a caller collection on every move avoids a copy but repeats work and
allows caller mutations to change supposedly fixed occupancy. No dependency or
new session abstraction is needed.

These API details are design proposals, not confirmed source requirements.
The proposed input domain is coordinate tuples; bespoke validation, normalization,
and guarantees for malformed inputs are outside this extension. Because the
confirmed rule concerns moving *into* a cell, propose allowing an initial pose
on an occupied cell: turns and departure work, but re-entry is blocked. This
avoids adding an initialization rejection to the existing API.

## Acceptance and compatibility

These expected results are hand-derived requirements for future tests, not
results observed from an occupied-cell implementation. Headings are north=0,
east=1, south=2, west=3.

| Start / occupied cells / commands | Expected return or error | Purpose |
|---|---|---|
| `(0, 0, 1)` / `{(1, 0)}` / `F` | `((0, 0, 1), [False])` | Both position and heading survive failure. |
| `(0, 0, 1)` / `{(1, 0)}` / `FFLF` | `((0, 1, 0), [False, False, True, True])` | Repeated failure does not stop the session; turn and clear movement still work. |
| `(0, 0, 0)` / omitted or empty / `RF` | `((1, 0, 1), [True, True])` | Existing callers remain compatible. |
| `(0, 0, 3)` / `{(-1, 0)}` / `F` | `((0, 0, 3), [False])` | Negative coordinates remain valid. |
| `(0, 0, 1)` / `{(0, 0)}` / `FRRF` | `((1, 0, 3), [True, True, True, False])` | Proposed initial-occupancy rule permits departure but blocks re-entry. |
| `(0, 0, 1)` / `{(1, 0)}` / `F?` | `ValueError("unknown command")` | Blocking does not suppress later command errors. |

Also verify empty commands preserve the pose with no outcomes, occupancy uses
coordinates independently of heading, and the proposed copy handles duplicate
and one-pass input without mutating or retaining a live view of caller data.

## Validation and limits

[Baseline inspection and checks](evidence/occupied-baseline.md) verified only the
existing movement/turn/error behavior. Extend the standard unittest suite with
the acceptance cases and ownership checks above, then run the full repository
check in [DEVNOTES](../DEVNOTES.md). No feature code or new tests have been written
in this phase. No material feasibility unknown remains; the public API and edge
semantics above remain proposed for implementation review. Original requirements
and [historical acceptance](history/completed.md) are preserved.
