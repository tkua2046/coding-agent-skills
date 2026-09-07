# Combined design and plan review

**Verdict: ready.** D1 and P1 are usable together for the proposed local increment. No material blockers or unresolved decisions.

**Reviewed scope/version:** `docs/DESIGN.md` D1 and `docs/PLAN.md` P1, as supplied, against `docs/ORIGINAL.md` (confirmed 4 September 2026), the existing exporter, tests, fixture and check configuration. Single-context review (self-review classification under the supplied skills); no separate reviewer or human approval is claimed.

**Next action:** In the separately assigned implementation task, deliver the flag, regressions and help/README update together, then run the configured gate and report actual results. No additional document-review round is needed.

## Evidence and findings

- **Behavior and feasibility:** D1:14–22 preserves `load_inventory`'s complete validation before selection (`inventory.py:20–42`) and reuses the existing JSON replacement/cleanup boundary (`inventory.py:45–60`). Optional selection in the CLI preserves default behavior, normalized records, order and encoding. D1:26–37 covers equality, no matches, header-only input, invalid omitted rows, destination preservation and exported counts. Its supplied CSV expectations match the fixture.
- **Delivery and checks:** P1:3–26 defines one coherent increment with regressions and documentation, explicit expected records and destination bytes. The baseline suite covers normalization, invalid rows, CLI failures and replacement failure. P1 names the actual gate: `tools/check.py:11–22` reads `quality.ini`'s `qa/` and `check_*.py` discovery and rejects zero discovered tests. The prepared-interpreter command is documented in `DEVNOTES.md:3–6`.
- **Reading cost:** Both opening sections communicate the behavior, validation choice and next action quickly. Detail is proportional to this small extension; acceptance remains behavioral rather than a duplicated implementation inventory.

### F1 — Optional: clarify “empty input”

**Location:** P1:18. A developer reading this bullet alone could interpret a zero-byte file as a successful empty export. The request:9 and D1:27 specify a header-only file; `inventory.py:25–26` rejects a missing header. **Minimal correction:** replace “empty input” with “header-only input.” **Verification:** statically compare the revised bullet with those sources; a future regression should include the required header. **Disposition:** accepted nonblocking wording ambiguity because P1 explicitly adopts D1 and the existing validation boundary.

**Checks performed:** Static file inspection only, using both supplied review operations and fixture `AGENTS.md`. No application commands or tests were run; this verdict establishes document readiness, not runtime correctness or human acceptance. No prior reports were present.
