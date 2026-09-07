# Whole-order inventory rejection

Proposed D2: check every requested quantity against the current remaining stock
before deducting any item in an order. If any quantity exceeds availability, append
`accepted=False` and leave that order's stock unchanged; continue with later orders.
Otherwise deduct every item and append `accepted=True`. This keeps the existing
batch-local copy and avoids rollback bookkeeping. It adds one read pass per order,
with linear total work and no additional stock snapshot per order.

For stock `{"a":3,"b":1}`, an order requesting `a:2,b:2` must fail without
consuming `a`; a following order requesting `a:3,b:1` must succeed, leaving both
at zero. A subsequent `a:1` fails, and an empty order succeeds. The ordered
acceptance flags are `[False, True, False, True]`.

Decision status: proposed for the independent document review that follows this
planning phase. Requirements: [requested extension](REQUEST.md) and preserved
[original requirements](ORIGINAL.md). Next outcome and evidence: [PLAN.md](PLAN.md).
No material decision remains unresolved.

## Compatibility and boundaries

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` signatures
and their `(remaining, outcomes)` return structure. Return one outcome containing
the original `order_id` and a boolean `accepted` per order, in input order. Evaluate
each order against remaining stock after earlier successful orders, not the original
stock. Equality is sufficient; integer subtraction preserves integer counts and
nonnegative stock for validated inputs. Empty orders are accepted; empty batches
still return a copied stock dictionary and no outcomes.

Retain the single initial stock copy and do not mutate stock, orders, or nested item
lists. `command_codec.decode` continues to validate the whole JSON batch before
the engine runs. Preserve its existing errors and validation policies; insufficient
stock is an ordinary rejected outcome, not a validation exception. The engine
continues to trust input shapes, positive integer quantities, and known unique SKUs.
Uniqueness makes the per-item availability check sufficient without aggregation.

The only atomicity promised is rejection for insufficient stock in this
single-process in-memory utility. Persistence, concurrency, transaction frameworks,
and remote infrastructure remain out of scope.

## Decisive acceptance

- Run the four-order example above through both APIs, checking exact remaining
  stock and ordered outcome dictionaries. Repeat with the insufficient item first
  to show rejection does not depend on item order.
- Compare caller stock and a deep copy of all orders after mixed success/rejection;
  confirm the returned stock is a separate dictionary and counts remain integers.
- Preserve empty-batch behavior and accept an empty order even with empty stock.
- Keep existing successful reservation and JSON validation behavior. Cover malformed
  JSON, invalid shapes, duplicate IDs, unknown/duplicate SKUs, and nonpositive or
  noninteger quantities (including booleans) without introducing new policy.

## Preserved accepted design (historical)

The following D1 text is retained verbatim. D2 supersedes only the sufficient-stock
caller responsibility and unconditional acceptance behavior.

# Accepted design D1
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
