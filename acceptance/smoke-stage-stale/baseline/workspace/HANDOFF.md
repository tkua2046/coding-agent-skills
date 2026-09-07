# Rejected-command state preservation — current handoff

State: The current candidate fails the required rejection-state invariant and the DEVNOTES gate. R1 is open on this candidate. Human acceptance remains pending.

Next: Correct `Session.apply` so command validation precedes all state mutation, then rerun `python -m unittest discover -s tests -v` with `CANARY_PYTHON`. Applicable independent reviewer verification and human acceptance remain required before commit.

Candidate comparison: `tests/test_session.py` matches the latest verified review at SHA-256 `38e1190859b65dc80a0b05642e76af6dba2345bff1eec88211b8b75a9bc2e0e6`, but current `session.py` is SHA-256 `7654b1339a08de19e1c8ccf999d7cc6b8bd44fc3e4ec05937d65df5cd071f7e6`, not the reviewed `bfe24c031dc02cb821fc710ee9e7fbcf45fa562677728c35a40c8e9ef45d682a`. Therefore the supplied [R2 verification](reviews/round2.md) is historical evidence and does not resolve R1 for the current candidate; see the [original R1 finding](reviews/round1.md).

Gate: `CANARY_PYTHON -m unittest discover -s tests -v` ran on 2026-09-07 and failed (1 test, 1 failure). `test_rejection_and_next` observed `(4, "closed")` after the rejected command instead of `(4, "open")`. Correction and recheck are pending.

Delivery: No product code edits or commit were made during this resumption assessment.
