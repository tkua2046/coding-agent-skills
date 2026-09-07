# Next work: atomic inventory reservations

Status: proposed design and planned implementation; no production change made.
Authority: [original request](REQUEST.md). Repository guidance: [AGENTS.md](../AGENTS.md).

Next action: implement one coherent change in `inventory.reserve`, with regression
coverage through both public entrypoints and an updated usage note. Check every
item against the current batch-local inventory before deducting any item in that
order. An insufficient order returns `accepted=False` and changes no stock;
subsequent orders still run. For example, after an earlier success leaves
`a=3,b=2`, requesting `a=2,b=3` must reject without consuming `a`, allowing a later
request for `a=3,b=2` to succeed.

This is a local, understood change: the validated input contract and single-process
execution permit one combined design/plan with one implementation boundary.

## Design and compatibility

[inventory.py](../inventory.py) already owns a shallow copy of the stock dictionary
and returns `(remaining, outcomes)` in input order. It currently deducts every
quantity and always reports success. [batch.py](../batch.py) decodes the complete
JSON batch through [command_codec.py](../command_codec.py) before calling the same
engine; there is no second allocation implementation to change.

Proposed decision: preflight each order against `remaining`, then deduct all its
items only if all are affordable. Preserve earlier successful deductions, and
append exactly one outcome per order, including rejected and empty orders. Equality
is sufficient stock. The empty order passes the check and consumes nothing.
Preflight must use current remaining quantities, not the caller's initial stock.

The engine is given positive integer quantities and unique known SKUs, so each item
can be checked independently. Keep integer arithmetic, both public signatures,
the tuple/dictionary result shape, order IDs and ordering, and caller stock and
nested order input immutability. A shallow stock copy suffices for integer values;
do not mutate the orders. No new validation contract is needed at the engine.
Keep JSON validation and its exceptions intact, including full decoding before
allocation. Insufficient inventory is an ordinary rejection, not an exception.

Preflight is simpler than subtracting and rolling back, which creates a restoration
path for partial deductions. It also avoids copying the full inventory for every
order. Expected work remains linear in stock size plus total items and orders,
with the existing stock copy and outcomes as the principal storage. This is an
algorithmic assessment, not a measured performance claim. No locks, transactions,
dependencies, persistence, or cross-process guarantees are required by the request.

## Acceptance

Use the following hand-derived sequence through both `reserve(stock, orders)` and
`execute(stock, json.dumps(orders))`, starting with `{"a":4,"b":2}`:

| Order ID | Items | Accepted | Remaining after order |
|---|---|---|---|
| first | `[["a",1]]` | `True` | `{"a":3,"b":2}` |
| reject | `[["a",2],["b",3]]` | `False` | `{"a":3,"b":2}` |
| later | `[["a",3],["b",2]]` | `True` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

The returned stock is `{"a":0,"b":0}` and outcomes are, in that order,
`{"order_id":"first","accepted":True}`,
`{"order_id":"reject","accepted":False}`,
`{"order_id":"later","accepted":True}`,
`{"order_id":"empty","accepted":True}`. Intermediate states can be verified
with sequence prefixes. The second item's shortage must not consume the first
item; the third order proves that processing continues after rejection.

Also cover these distinct boundaries:

- With `{"a":3}`, consecutive orders requesting 2 and 2 yield acceptance
  `True, False` and remaining `{"a":1}`; this catches checking initial stock.
- With `{"a":0}`, a request for 1 rejects and leaves zero; an empty order still
  succeeds. No orders return an equal stock snapshot and an empty outcome list.
- Preserve caller stock and the full nested order structure for mixed outcomes;
  preserve integer result counts, including a quantity above `2**53` to expose any
  accidental float conversion.
- Retain successful-path and JSON validation regressions. Verify malformed JSON,
  non-list batches, invalid order shape/IDs, non-list items, malformed item pairs,
  unknown/duplicate SKUs, and nonpositive/noninteger quantities (including booleans)
  still fail as they do today. A valid order followed by invalid JSON order data
  fails validation for the batch and leaves caller stock unchanged.

## Implementation outcome and review boundary

One planned stage, with no dependency or unresolved contract blocker: change the
allocation decision in [inventory.py](../inventory.py), add behavior-based tests in
[tests/test_inventory.py](../tests/test_inventory.py) exercising both entrypoints,
and update [README.md](../README.md)'s statement that callers must ensure sufficient
stock. Keep these together as one intended implementation commit so the behavior,
regressions, and documentation can be reviewed together. No commit is authorized
or performed during this planning pass.

Done means all acceptance above holds, existing validation and public compatibility
remain intact, and the complete check in [DEVNOTES.md](../DEVNOTES.md) passes:

```sh
PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
```

For the subsequent implementation task: implement and test, run that gate, review
the resulting diff against this contract, fix findings and rerun affected checks,
then commit only within that task's authorization. The fixture specifies no
separate reviewer or human approval gate and represents no installed hooks or CI.
Record actual results and review findings against the implemented snapshot; this
planning note is not a code review or acceptance of future code.

## Verified baseline and limits

Observed during this planning pass on 2026-09-07 with the prepared runtime and
bytecode writes disabled:

- The documented unittest discovery command passed all 6 existing tests. They
  cover success, an empty batch, the adapter, and some validation; they do not
  establish shortage rejection or atomicity.
- An in-memory probe of the four-order acceptance sequence above returned
  `{'a': -2, 'b': -3}` and all four outcomes accepted through both entrypoints.
  Thus both currently violate the requested behavior. Caller stock and nested
  orders compared equal to a deep copy afterward.
- Source inspection confirms complete JSON decoding precedes engine execution.
  The expanded validation cases and new reservation acceptance are proposed
  checks, not reported passes. No performance benchmark was run.

No existing source, tests, configuration, or source documents were changed. This
handoff is the only new project artifact; no prior reports were present in the
fixture file listing. No external service or dependency installation was used.
