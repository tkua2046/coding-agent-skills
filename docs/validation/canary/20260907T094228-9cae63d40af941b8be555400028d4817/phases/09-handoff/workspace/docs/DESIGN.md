# Design: whole-order reservation

D2 is implemented in S1. Independent [document review](../reviews/design-current.json)
and [code review](../reviews/code-current.json) both report `ready` with no findings.
Human review and acceptance remain pending; the next action is owner review.
See the [current handoff and check evidence](PLAN.md) and the preserved
[D2 proposal](DESIGN.d2-proposal.md) for the earlier phase status.

S1 implements [REQUEST.md](REQUEST.md) by checking all items against the current
batch-local stock before deducting any item. A rejected order leaves that stock
unchanged, and later orders continue.

This is a local, reversible change with two existing interfaces and no external
state, so one compact amendment and one combined design/plan review are sufficient.
The original requirements in [ORIGINAL.md](ORIGINAL.md) and [REQUEST.md](REQUEST.md)
remain intact; the target behavior and decisive examples are in [SPEC.md](SPEC.md).

## Decision and consequences

Keep `inventory.reserve(stock, orders)` and `batch.execute(stock, text)` unchanged.
The engine continues to copy stock once and trusts validated input. For each order,
compare every quantity with the remaining stock; deduct all items only if every
comparison succeeds. Append exactly one result using the existing keys and order.
Equality succeeds; an empty order succeeds without mutation. Insufficiency is a
normal `accepted=False` outcome, not an exception. No input is mutated.

Preflight followed by deduction is sufficient because SKUs are unique per order
and execution is single-process in memory. It avoids partial deduction and rollback
bookkeeping without a per-order stock copy. Both passes are linear in order size;
no transaction framework, dependency, persistence or concurrency handling is needed.
Existing JSON decoding and validation remain at the adapter boundary, including
validation of the entire payload before engine execution. No new validation policy
is introduced for the direct API.

At the planning baseline, inspection confirmed that `inventory.py` deducted
unconditionally and always accepted; `batch.py` delegates after `command_codec.py` validation. The baseline tests
covered success and selected validation failures but did not establish shortage
rejection or order-input immutability. See the preserved
[planning baseline](PLAN.s1-author.md#verified-planning-baseline--2026-09-07);
current implementation evidence is in the [handoff](PLAN.md).
There are no unresolved material contract decisions.

## Accepted design D1 (historical, preserved)
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.

D2 supersedes only D1's caller guarantee of sufficient inventory. All other accepted
decisions continue to apply. D1's accepted status does not imply review of D2.
