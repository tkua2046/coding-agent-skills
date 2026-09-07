# Next work: atomic inventory reservations

Status: proposed design and planned implementation; no production change made.
Authority: [original request](REQUEST.md). Next action: implement the single outcome below in a subsequent task.

Make each order all-or-nothing against the batch's current remaining stock. Check availability for every requested item before applying that order's deductions. A shortage produces `accepted=False`, changes no quantities, and does not stop later orders. Keep both public entrypoints and their existing contracts.

This is a local change with clear requirements and no persistence or cross-process coordination, so one combined design/plan note is sufficient. No blocking clarification was found in the fixture. For example, after an earlier success leaves `a=3,b=2`, an order requesting `a=2,b=3` must be rejected without consuming `a`; a later order requesting `a=3,b=2` must then succeed.

## Current behavior and design

- [inventory.py](../inventory.py) copies stock, deducts every item unconditionally, and marks every order accepted. Keep the batch-local copy and ordered result format `(remaining, outcomes)`, with each outcome containing `order_id` and boolean `accepted`.
- [batch.py](../batch.py) calls `decode` before `reserve`. Keep this delegation so both entrypoints acquire identical reservation behavior without duplicating allocation logic.
- [command_codec.py](../command_codec.py) validates the complete JSON batch before execution: list shape, exact order keys, unique string IDs, item lists/pairs, unique known string SKUs, and strictly positive integer quantities (excluding booleans). Short stock is a valid business rejection, not a validation error. Preserve existing validation and exceptions; do not add engine-side validation requirements.
- [tests/test_inventory.py](../tests/test_inventory.py) covers successful allocation, no orders, the adapter, and three validation failures. It does not yet establish shortage rejection, rollback of an order, continuation, or empty-order acceptance. Its input preservation assertion covers stock, not nested order contents.

For each order, determine whether every requested quantity is available in `remaining`, including deductions from prior successful orders. Only if that condition holds, deduct all items. Otherwise append the rejected outcome and continue with the same `remaining`. An empty item list satisfies the condition and is accepted. Equality is sufficient stock. Preserve integer arithmetic, input ordering, and caller-owned stock and order data; do not sort or mutate nested item lists.

The engine may rely on the request's validated positive quantities and unique known SKUs. Availability checking and deduction must consume the same item contents. Do not introduce a stricter public input contract as a side effect. There is no need for locks, transactions, dependencies, or an alternate adapter path in this one-process, batch-local utility.

Checking before deduction avoids partial writes and rollback bookkeeping. Copying all remaining stock for every order would also isolate failure, but adds work proportional to the inventory size per order without a requirement for it. Prefer work proportional to requested items, plus the existing initial stock copy. This is a design expectation, not a measured performance claim.

## Decisive acceptance

Run the following sequence through both `reserve(stock, orders)` and `execute(stock, json.dumps(orders))`, starting from `{"a":4,"b":2}`:

| Order ID | Items | Accepted | Remaining after order |
|---|---|---|---|
| `first` | `[["a",1]]` | `True` | `{"a":3,"b":2}` |
| `short` | `[["a",2],["b",3]]` | `False` | `{"a":3,"b":2}` |
| `later` | `[["a",3],["b",2]]` | `True` | `{"a":0,"b":0}` |
| `empty` | `[]` | `True` | `{"a":0,"b":0}` |

The final return must be `({"a":0,"b":0}, [{"order_id":"first","accepted":True}, {"order_id":"short","accepted":False}, {"order_id":"later","accepted":True}, {"order_id":"empty","accepted":True}])`. Expected values are hand-derived from the request. Assert deep equality of stock and orders with their pre-call copies.

Also establish these boundaries with focused tests:

- Earlier success counts: stock `a=3`, successive orders each requesting `a=2` yield acceptance `[True, False]` and final `a=1`. This catches checking against original stock.
- Insufficiency on the first item, including zero stock, rejects; insufficiency after a sufficient item leaves both unchanged. Unrequested SKUs remain unchanged.
- Empty orders are accepted, including with empty stock; no orders still returns an equal stock snapshot and no outcomes.
- Integer counts remain exact, including values above `2**53`; do not convert quantities or stock to floats.
- Preserve JSON rejection behavior for malformed JSON and every existing validation rule above, including zero/negative/fractional/boolean quantities. A later invalid order still fails decoding for the batch and leaves input stock unchanged, even if preceding orders are valid. Keep current exception behavior rather than introducing acceptance outcomes for invalid JSON.

## One implementation outcome

**Planned, no prerequisite stage:** update the reservation behavior in `inventory.py`, add focused regression/compatibility coverage in `tests/test_inventory.py`, and update the stale sufficient-stock sentence in `README.md`. The adapter and codec should continue to serve their current roles; change them only if a demonstrated compatibility issue requires it. This is one coherent proposed commit boundary: atomic reservation behavior, its tests, and its public description together.

Done means both public APIs satisfy the acceptance cases, existing validation and input contracts remain intact, and all contributor checks pass on the final implementation. The principal risks are partial deductions, checking original stock instead of remaining stock, and accidentally changing validation. No release, dependency installation, or infrastructure work belongs to this outcome.

Follow [contributor checks](../DEVNOTES.md): implement and test, run the complete local gate, review the resulting diff against this note, fix findings and rerun affected checks before handing off. The fixture specifies no independent human/agent approval or installed hook/CI gate. Record actual check results and review findings for that implementation snapshot; commit only if the subsequent task authorizes it.

```sh
PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
```

## Observed evidence and limits

Planning pass, 2026-09-07: the command above passed all six existing tests. A read-only Python probe using the four-order sequence above returned `{"a":-2,"b":-3}` with every order accepted through **both** entrypoints, instead of the expected `{"a":0,"b":0}` and `[True, False, True, True]`. Deep comparison confirmed unchanged caller inputs in that probe. These observations describe only the starting snapshot; the requested behavior and new acceptance checks remain unimplemented and unverified.

The assessment used only the fixture and supplied feature-design/implementation-plan skills. Original requirements and source documents were preserved. No prior reports were present in the fixture file listing; no performance, release, or earlier review claims are inferred.
