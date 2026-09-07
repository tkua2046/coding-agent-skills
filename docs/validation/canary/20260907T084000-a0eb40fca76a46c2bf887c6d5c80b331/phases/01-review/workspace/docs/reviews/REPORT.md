# Combined design and plan review

Verdict: **needs changes** — the proposed next increment is not usable as written.
Reviewed scope/version: D1 and P1, supplied fixture snapshot, 7 September 2026; assessed against ORIGINAL.md, the existing exporter, tests and check configuration.
Reviewer: single-context self-review using the supplied feature-design and implementation-plan review operations; no separate reviewer.
Open findings: R1–R3. Next action: amend D1/P1 as below before the separately assigned implementation; no additional approval round is required by this review.

Checks performed: static inspection of AGENTS.md, the supplied review skills, docs/ORIGINAL.md, docs/DESIGN.md, docs/PLAN.md, inventory.py, qa/check_inventory.py, quality.ini, tools/check.py, DEVNOTES.md, README.md and examples/stock.csv. No application commands or tests ran; runtime correctness and human acceptance are unverified.

## Findings

### R1 — High: filtering bypasses required validation (open)

Location: [D1](../DESIGN.md), lines 86–94, against [ORIGINAL](../ORIGINAL.md), lines 11–19; existing validation is in inventory.py:20–42, before writing at :71–72.

With the standard header, `A1,Widget,1,2` followed by ` A1 ,Again,9,2` must fail for a duplicate normalized SKU. D1 discards the second row before checking duplicates, allowing success and replacement of the previous destination. Likewise, `B2,,9,2` or `B2,Widget,9,2,extra` would evade required label/shape checks. Keeping the atomic writer does not protect against accepting invalid input.

Minimal correction: use the existing complete `load_inventory` validation for both modes, then optionally filter validated records by `quantity <= reorder_at` before calling the unchanged writer. This fits the explicitly small, in-memory scope.

Verification: statically confirm validation precedes selection for every row. During later implementation, assert exit 2 and unchanged destination bytes for these omitted-row errors and malformed numbers, with and without the flag.

### R2 — High: Stage 1 acceptance defers a prerequisite (open)

Location: [P1](../PLAN.md), lines 86–96, against ORIGINAL.md:5–19.

P1 declares Stage 1 ready for local use after testing errors only among selected rows; whole-input validation and destination preservation for omitted-row errors arrive in optional later Stage 2. The duplicate example in R1 could therefore satisfy Stage 1's stated acceptance while violating the requested export contract. Correcting D1 alone leaves this delivery boundary misleading.

Minimal correction: move whole-input validation and its regression cases into Stage 1, preferably combining these small stages. Stage 1 acceptance must include default behavior, selection/equality/order, header-only and no-match success, invalid input anywhere, and preservation of destination bytes on error, alongside CLI help and README updates. Any remaining consolidation may be optional only after that behavior is delivered.

Verification: trace those requirements to the first usable stage and its tests with explicit expected results. Keep the configured gate, `"${CANARY_PYTHON:-python3}" tools/check.py`, for later implementation: static inspection confirms it discovers `qa/check_*.py` through quality.ini and rejects zero tests. Existing tests cover baseline behavior but do not exercise the proposed flag.

### R3 — Medium: the first screen hides the decision and next stage (open)

Location: DESIGN.md:3–84 and PLAN.md:3–84; both actionable sections begin at line 86.

A developer selecting the next increment first encounters dozens of reader, writer and maintenance observations, including temporary-variable details, before discovering the selection semantics or delivery boundary. This prevents a quick understanding of the behavior and next action and makes the consequential choices in R1/R2 easy to miss.

Minimal correction: lead D1 with the corrected behavior, validation boundary and decisive examples; lead P1 with the next stage, dependencies and acceptance. Remove incidental code narration or move useful reference notes below those sections. Exact headings and formatting are optional.

Verification: the opening screen of each document should identify the intended outcome and major decision or next action without consulting its closing section.

The stated equality, sample ordering, no-match result, unchanged writer, documentation scope and configured check entrypoint are otherwise consistent with the request. These findings conclude the authorized static review; no implementation or additional review round was performed.
