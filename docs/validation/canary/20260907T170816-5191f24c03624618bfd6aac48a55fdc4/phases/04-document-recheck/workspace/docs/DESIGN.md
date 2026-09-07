# Design: whole-order inventory rejection

Status: proposed amendment, ready for independent document review; implementation
has not begun. [REQUEST.md](REQUEST.md) is the unchanged feature authority;
[SPEC.md](SPEC.md) records the target behavior. This local, in-memory change needs
one compact design amendment and one implementation outcome, reviewed together.

Decision: check every item against the current batch-local remaining stock before
deducting anything for that order. If any item is short, append `accepted=False`
without changing stock; otherwise deduct all items and append `accepted=True`.
Continue in input order. An empty order passes the check and changes nothing.
Next: independent reviewer assesses this amendment and [PLAN.md](PLAN.md), then
the implementer delivers S1 and its regression checks.

## Rationale and compatibility

Inspection: `inventory.reserve` copies stock once but currently deducts each item
unconditionally. `batch.execute` first calls `command_codec.decode`, which validates
the complete JSON batch before invoking the engine. Keep these responsibilities
and both public signatures and return shapes. The engine continues to trust valid
inputs; add no validation policy or dependency.

A preflight pass followed by deduction is sufficient because SKUs within an order
are unique, counts are positive integers, and there are no concurrent writers.
It prevents partial deductions even when the short item is last. Deducting and
rolling back would require restoration bookkeeping without a benefit here.
Keep the single stock copy, no mutation of caller stock or nested orders, integer
counts, and one boolean outcome per order. With nonnegative initial stock, remaining
stock stays nonnegative. Shortage is an ordinary rejected outcome, not an exception.
JSON validation errors retain existing behavior before any reservation executes.
Persistence, concurrency, transaction frameworks and remote infrastructure remain
outside scope. There are no unresolved behavioral decisions.

## Decisive acceptance

Use initial stock `{"a":3,"b":1}` and the following sequential orders. Run the
same scenario through `reserve` and through `execute` with equivalent JSON:

| Order ID | Items | Accepted | Remaining stock afterward |
| --- | --- | --- | --- |
| reject | `[["a",2],["b",2]]` | `False` | `{"a":3,"b":1}` |
| take | `[["a",3],["b",1]]` | `True` | `{"a":0,"b":0}` |
| later | `[["a",1]]` | `False` | `{"a":0,"b":0}` |
| empty | `[]` | `True` | `{"a":0,"b":0}` |

Expect final stock `{"a":0,"b":0}` and outcomes with these exact IDs and booleans
in this order. Also check `reject` alone leaves all quantities unchanged: this
makes partial deduction observable directly. Compare caller stock and nested orders
to independent pre-call snapshots, and verify returned counts remain integers.
Retain empty-batch behavior and existing JSON validation tests. Preserve rejection
of malformed shapes, duplicate IDs/SKUs, unknown SKUs, and nonpositive/noninteger
quantities; representative missing regression coverage belongs in S1 without
changing the validator's policy.

## Verified baseline and limits

On 2026-09-07, both existing unittest discovery and the repository gate passed
all six tests (exit 0). They do not cover shortages, empty orders, or nested-order
immutability. A read-only mixed-order probe reproduced negative stock and all-true
outcomes, confirming the requested behavior is absent. Commands and raw output:
[planning evidence](evidence/planning-baseline.md). These are baseline results,
not feature acceptance or an independent review.

## Preserved accepted design D1 (historical)

The caller-sufficiency assumption below is superseded by the requested amendment;
the boundary, ownership and immutability decisions remain in force.

The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
