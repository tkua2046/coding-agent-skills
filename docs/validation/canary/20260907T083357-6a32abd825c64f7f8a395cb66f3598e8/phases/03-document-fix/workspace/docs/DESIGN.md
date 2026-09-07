# Accepted design D1
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.

## D2 proposed: whole-order rejection

Outcome: reject an insufficient order without changing batch stock, then continue
with later orders. Status: planned, awaiting independent review; no implementation
has been changed. [REQUEST.md](REQUEST.md) is the extension authority; D1 above is
preserved history, with only its sufficient-inventory precondition superseded.

Main decision: check all items against current remaining stock before deducting any
item. This avoids rollback and keeps the existing stock copy and APIs. Next step:
independent review of this design and [PLAN.md](PLAN.md), then one implementation
increment. The original 15-minute allowance covers the whole task, including reviews;
it is not a separate budget for each phase.

### Existing behavior and compatibility

Inspection confirms `inventory.reserve(stock, orders)` copies stock once, subtracts
each item unconditionally and returns `(remaining, outcomes)` with all outcomes
accepted. `batch.execute(stock, text)` decodes the entire JSON batch before calling
the engine. `command_codec.decode` owns validation. Both APIs and return shapes stay
unchanged; no new validation is proposed for the trusted Python engine.

The current contract and the extension are recorded in [SPEC.md](SPEC.md). Input
stock, orders and nested item lists remain untouched. Counts remain integers, and
valid nonnegative input stock must remain nonnegative throughout processing.

### Decisions and consequences

| Decision | Reason / alternative | Consequence | Example |
|---|---|---|---|
| Preflight every item, then deduct only if all are sufficient | Validated SKUs are unique per order; subtract-and-rollback adds unnecessary mutable recovery state | Two passes for an accepted order, linear total item work; no per-order stock copy | Enough `a` but too little `b` leaves both unchanged |
| Compare against batch-local remaining stock in input order | Earlier successes consume inventory; comparing against original stock would over-accept | Rejection affects only that order and does not halt the batch | Two requests for the last unit yield `True`, then `False` |
| Keep insufficiency as an ordinary `accepted=False` outcome | The request distinguishes stock rejection from malformed JSON | Existing validation exceptions and validation-before-execution remain unchanged | Unknown SKU still raises; known SKU with too little stock returns `False` |

An empty order passes the all-items check and is accepted. Exact exhaustion is
accepted. Additional allocation structures, persistence, concurrency and transaction
frameworks are out of scope. No unresolved contract decisions were found.

### Decisive acceptance

Run the following batch through both `reserve` and `execute` (JSON-encode the same
orders for the latter). Start with `{"a": 4, "b": 1}`:

| Order | Items | Accepted | Remaining after order |
|---|---|---|---|
| `reject` | `[["a",3],["b",2]]` | `False` | `{"a":4,"b":1}` |
| `later` | `[["a",4],["b",1]]` | `True` | `{"a":0,"b":0}` |
| `empty` | `[]` | `True` | `{"a":0,"b":0}` |

Expected return: `({"a":0,"b":0}, [{"order_id":"reject","accepted":False},
{"order_id":"later","accepted":True}, {"order_id":"empty","accepted":True}])`.
The first order must not spend its three available `a` units because `b` is short;
the second spends all four `a` and the one `b`. This catches partial deduction,
stopping after rejection, incorrect result order and rejecting exact exhaustion.

Also check sequential depletion: stock `{"a":2}`, orders requesting 1, 2, then 1
unit yield acceptances `True, False, True` and final `{"a":0}`. This distinguishes
current remaining stock from original stock and preserves prior successful work.
Check an insufficient single item at zero stock, empty order on empty stock, and an
empty batch. Assert caller stock and the entire nested orders structure equal deep
snapshots afterward, with integer stock values and actual boolean outcomes.

Keep existing adapter validation checks and cover malformed shapes, duplicate IDs,
unknown/duplicate SKUs and nonpositive/noninteger quantities, including booleans.
A malformed later order must still raise before any execution, preserving stock.
These are compatibility checks of existing policy, not new rejection rules.

### Verified baseline and limits

On 2026-09-07, both `"$CANARY_PYTHON" -m unittest discover -s tests -v` and
`"$CANARY_PYTHON" hooks/pre-commit` passed all six existing tests. The supplied
hook also rejects empty discovery. Existing tests cover successful reservation,
empty batch and selected validation errors, but not shortage rejection or nested
order immutability. A read-only probe of the decisive batch currently returned
`{"a":-3,"b":-2}` with all three outcomes `True`, confirming the missing behavior.
These results establish the baseline only; proposed acceptance has not passed.
