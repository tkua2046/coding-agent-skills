# Occupied-cell specification addendum

The [original request](ORIGINAL.md), [current baseline specification](SPEC.md)
and [confirmed occupied-cell request](OCCUPIED_REQUEST.md) remain unchanged.
The occupied-cell behavior below is confirmed by that request; API and input
clarifications are proposed by the [design amendment](DESIGN.md), not new
confirmed user decisions. This addendum describes future behavior.

## Required behavior

Caller-supplied occupied cells are fixed for a run. A forward move into one
reports failure, preserves position and heading, and permits subsequent commands.
Turns still work. There is no routing, persistence, moving-obstacle support or
configuration file. Preserve the baseline unbounded grid, heading convention,
return shape and rejection of unknown commands.

## Proposed interface clarifications

- Add optional `occupied=()` after the existing pose and commands parameters;
  omitted and empty inputs both preserve existing behavior.
- Accept an iterable of `(x, y)` integer pairs, snapshot it once at entry and
  ignore duplicate pairs. Do not mutate the supplied iterable or retain state
  across calls. Malformed-input diagnostics are outside this extension.
- Check destinations only, including when the starting cell is occupied.
- Return `False` for blocked F and `True` for successful F, L and R. Unknown
  commands continue to raise `ValueError`, with no returned partial result.

## Acceptance examples

| Pose; occupied cells; commands | Expected result | Basis |
|---|---|---|
| `(0,0,0)`; `{(0,1)}`; `F` | `((0,0,0), [False])` | Block preserves full pose |
| `(0,0,0)`; `{(0,1)}`; `FFRF` | `((1,0,1), [False,False,True,True])` | Retry fails; turn and continuation succeed |
| `(0,0,0)`; `{(0,1)}`; `LR` | `((0,0,0), [True,True])` | Turns remain valid |
| `(0,0,3)`; `{(-1,0)}`; `F` | `((0,0,3), [False])` | Negative coordinates and heading preserved |
| `(0,0,0)`; omitted or empty; `RF` | `((1,0,1), [True,True])` | Compatibility |
| `(0,0,0)`; `{(0,0)}`; `FRRF` | `((0,1,2), [True,True,True,False])` | Proposed start-cell policy; return is blocked |
| `(0,0,0)`; `{(0,1)}`; `F?` | `ValueError` | Unknown-command compatibility after failure |
| `(2,3,0)`; any valid occupied input; empty commands | `((2,3,0), [])` | No commands leave pose unchanged |

Equivalent list, set and generator inputs must yield the same results, including
repeated blocked destinations and duplicates. Changes to caller storage after
entry must not alter membership during command consumption. A following call
without occupied cells must be unaffected by an earlier blocked call.
