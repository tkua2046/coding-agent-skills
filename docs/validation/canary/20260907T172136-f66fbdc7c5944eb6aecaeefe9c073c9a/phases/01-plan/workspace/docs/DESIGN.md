# Design: whole-order reservation rejection

Status: proposed amendment D2; implementation and independent review pending.
Authority: [current request](REQUEST.md), [original requirements](ORIGINAL.md),
and [target contract and acceptance](SPEC.md). Next: one combined independent
design/plan review, then [S1](PLAN.md).

Reject an order if any item exceeds the stock remaining when that order starts.
Check all items before deducting any; on rejection append `accepted=False` and
continue with later orders. This local extension needs one implementation outcome
and a compact combined document review: state is in memory, interfaces are stable,
and there is no persistence or concurrency to coordinate.

## Decision and inspected implementation

`inventory.reserve` already copies stock once but unconditionally subtracts each
item and reports success. Keep that ownership and result shape. For each validated
order, first determine whether every quantity is available in the current copy;
deduct all items only if so. Empty orders succeed. Unique item SKUs make individual
availability checks sufficient; no aggregation or additional validation is needed.
Checking before mutation avoids partial deductions and rollback bookkeeping. It
requires at most two passes over an accepted order and no new state framework.

`batch.execute` calls `command_codec.decode` before invoking the engine. Keep both
APIs and the existing validation/error behavior. Neither stock nor nested order
inputs may be mutated; counts remain integers. The engine continues to trust the
validated-input contract. No new dependencies, persistence, concurrency, commit,
release or version change belongs to this work.

The decisive [example](SPEC.md#decisive-acceptance) accepts an initial order,
rejects a mixed order whose second item is short without deducting its first item,
then successfully consumes the exact remaining stock. This proves rejection is
local to the order and later processing continues against current stock.

## Evidence and limits

Planning inspection on 2026-09-07 covered the engine, adapter, decoder, existing
tests, README, DEVNOTES and installed gate. Both unittest discovery and the installed
pre-commit gate passed all 6 existing tests using `CANARY_PYTHON`. These tests do not
cover insufficient inventory or an order with no items; the existing empty test
covers an empty batch only. A read-only probe of the decisive example through both
APIs returned stock `{"a": -2, "b": -2}` and four successful outcomes, confirming
the requested behavior is absent. This is baseline evidence, not feature acceptance.
No material design questions remain; proposed checks and delivery are in the plan.

## Accepted design D1 (historical, preserved)

The sufficiency responsibility below is superseded by D2 once implemented; the
other decisions remain applicable.

The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
