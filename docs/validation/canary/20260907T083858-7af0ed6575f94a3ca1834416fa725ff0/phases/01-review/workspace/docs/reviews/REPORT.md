# Combined design and plan review

Verdict: **ready**. D1/P1 describe a usable, bounded next increment. No material blockers or unresolved decisions.

Reviewed scope/version: the supplied `docs/DESIGN.md` **D1** and `docs/PLAN.md` **P1**, against `docs/ORIGINAL.md` (confirmed 4 September 2026) and the current fixture, on 7 September 2026. Single-context review using both supplied skills; no separate agent review or human acceptance is claimed.

Next action: assign the implementation separately and deliver P1's single increment with its regressions and usage update. No additional document approval round is needed.

## Evidence and usability

- D1:14–22 and P1:10–12 retain whole-file validation before filtering. This matches `inventory.py:20–42` and protects against an omitted in-stock duplicate or malformed later row. Reusing `write_export` (`inventory.py:45–60`) preserves JSON encoding and the replace/cleanup boundary.
- D1:26–37 and P1:17–25 cover default order, equality, no matches, error code 2, destination-byte preservation and explicit expected records. The supplied CSV confirms the stated B2/A1/C3 and A1/C3 examples. Existing `qa/check_inventory.py` covers normalization, malformed records, default CLI behavior and replacement failure; P1 adds feature regressions alongside code.
- P1:21–22 names the established gate. Static inspection of `DEVNOTES.md`, `quality.ini` and `tools/check.py:11–22` confirms discovery uses `qa/check_*.py` and rejects an empty suite. The planned check is grounded in the actual configuration.
- Both documents put the outcome and next action first. One increment is proportionate to the small in-memory extension; linked requirements and decisive examples make the behavior and implementation boundary quick to understand.

## Optional wording finding

**R1 — nonblocking, accepted with interpretation.** P1:18 says “empty input”; ORIGINAL:9 and D1:27 specify a **header-only file**. A zero-byte CSV instead fails the existing header check (`inventory.py:25–26`). Reading P1 literally could produce an incorrect acceptance test. Treat D1's header-only definition as authoritative; optionally replace “empty input” with “header-only input.” Verify any wording change against that distinction, and retain header validation during implementation. No document revision is required for readiness.

Checks performed: static file inspection only, including fixture `AGENTS.md`, both review skill operations, requirements, design, plan, application, example data, README, contributor notes, test source and check configuration. No application commands or tests were run; runtime correctness and future acceptance remain unverified. Only this report was added; no prior reports were present.
