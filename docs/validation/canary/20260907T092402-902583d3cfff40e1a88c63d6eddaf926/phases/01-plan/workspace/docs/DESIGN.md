# Atomic inventory reservation

Status: proposed design, grounded in inspected code and observed baseline; no implementation performed. Authority: [original request](REQUEST.md). Next step: the single implementation stage in [NEXT.md](NEXT.md).

Each order must either deduct every requested item or deduct nothing. Check all quantities against the current batch-local stock before applying that order's deductions. Keep both public APIs and the existing JSON validation boundary. The consequence is that an insufficient order becomes an ordinary rejected result, and subsequent orders still run against stock left by earlier accepted orders.

## Current behavior and scope

- [inventory.py](../inventory.py): `reserve(stock, orders)` copies stock, unconditionally deducts each order, and returns `(remaining, outcomes)` with every `accepted` set to `True`. Insufficient stock can become negative.
- [batch.py](../batch.py): `execute(stock, text)` decodes the entire batch before invoking `reserve`; it returns the same tuple.
- [command_codec.py](../command_codec.py): validates JSON structure, unique string order IDs, unique known SKUs per order, and strictly positive integer quantities (including rejection of booleans). Keep this behavior and existing errors.
- [tests/test_inventory.py](../tests/test_inventory.py): covers success, stock preservation, no orders, adapter success and three validation failures. It does not cover rejected orders, an order with no items, or nested order-input preservation.

The six existing tests pass. A read-only probe confirms both APIs currently return negative stock and all-true outcomes for the decisive mixed batch below. See [evidence](EVIDENCE.md).

## Decisions and invariants

**Check before deduction → avoids partial effects → rejected orders leave the current remaining stock exactly unchanged →** an order requesting available `a` followed by insufficient `b` cannot consume `a`. A deduct-and-rollback alternative introduces restoration logic unnecessarily; copying the whole stock per order also adds unnecessary work.

**Retain one batch-local stock copy → preserves caller ownership and sequential semantics → accepted deductions remain visible to later orders, while caller stock and nested order data remain unchanged →** a later order can use stock an earlier rejected order attempted to reserve, but cannot reuse quantities consumed by an accepted order.

**Keep validation in the adapter → preserves both existing contracts → direct Python callers continue to supply validated positive quantities and unique known SKUs; no new engine validation or error policy is proposed →** a boolean quantity still fails through `execute` before allocation. Invalid JSON/batches retain exceptions rather than becoming `accepted=False` outcomes. Insufficiency of otherwise valid quantities is not a validation error.

Return one outcome per input order in input order, preserving `order_id` and Boolean `accepted`. Exact availability succeeds. Empty orders succeed without changing stock, and an empty batch returns a stock copy and no outcomes. Integer stock arithmetic remains integer arithmetic; untouched SKUs retain their quantities. No locks, persistence, reservation retries, or concurrent transaction machinery are needed for this process-local utility.

The check/deduct approach assumes the existing reusable item lists; JSON already produces these, and the direct API's established examples use them. No new public input representation is introduced. Runtime work remains linear in stock-copy size plus total requested items, with up to two item traversals per accepted order.

## Decisive acceptance examples

Run the mixed example through both `reserve` and `execute` (JSON encoding the same orders). Begin with `stock = {"a": 4, "b": 2}`:

| Order | Items | Expected accepted | Expected remaining after order |
|---|---|---|---|
| first | `[["a", 1]]` | `True` | `{"a": 3, "b": 2}` |
| reject | `[["a", 2], ["b", 3]]` | `False` | `{"a": 3, "b": 2}` |
| later | `[["a", 3], ["b", 2]]` | `True` | `{"a": 0, "b": 0}` |
| empty | `[]` | `True` | `{"a": 0, "b": 0}` |

The final tuple must contain `{"a": 0, "b": 0}` and the ordered outcomes `[{"order_id": "first", "accepted": True}, {"order_id": "reject", "accepted": False}, {"order_id": "later", "accepted": True}, {"order_id": "empty", "accepted": True}]`. Original stock and all nested order data must equal snapshots from before the call. Check intermediate states with batch prefixes where needed to expose the failure boundary.

Also cover depletion: stock `{"a": 2}`, orders requesting `a:2`, then `a:1`, then no items yield flags `[True, False, True]` and final stock `{"a": 0}`. This catches checks against original stock instead of current remaining stock. No orders yield unchanged quantities and `[]` outcomes. Include an untouched SKU and integer-type assertions in regression coverage.

For compatibility, keep existing validation checks and cover representative uncovered rules: malformed JSON, non-list top level, invalid order shape/duplicate IDs, malformed item shape, and zero, negative or noninteger quantities. An invalid later order must still cause `execute` to raise rather than return partial outcomes; caller stock remains unchanged. Preserve current exception behavior without expanding validation requirements.

## Open questions and limits

No blocking product decision was found. Requirements are explicit about rejection, continuation, validated engine inputs, and scope. The internal check-before-deduction choice is proposed, not implemented or user-approved as a separate requirement. No stock-domain validation, streaming-input support, concurrency guarantee, or external-service behavior is added by this design.
