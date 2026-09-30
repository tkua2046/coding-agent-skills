# Requested extension
Some callers now submit orders that exceed available inventory. Make reservation
reject such an order as a whole: if any requested item is insufficient, return
accepted=False for that order and leave all stock quantities unchanged by it.
Continue with later orders against the current remaining stock. Successful orders
still deduct all their items and return accepted=True. Preserve both current APIs,
JSON validation, result order, input immutability and integer counts. An empty order
is accepted without changing stock. Input shapes, positive quantities and known unique
SKUs are already validated; do not add new validation policies.
This is a single-process in-memory utility. Persistence, concurrency, a transaction
framework and remote infrastructure are outside this feature. We need the feature
ready for human review within 15 minutes of agent execution, including necessary
document/code reviews. Agent-only review is authorized while working; human review
happens afterward. No commit, push, version advancement or release is requested.
