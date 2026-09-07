# Combined design and plan review

Verdict: **needs changes**. D1/P1's proposed first increment is not usable against the confirmed requirements.

Reviewed scope/version: D1 (`docs/DESIGN.md`) and P1 (`docs/PLAN.md`), as supplied on 2026-09-07, against `docs/ORIGINAL.md`, `inventory.py`, `qa/check_inventory.py`, `examples/stock.csv`, README, DEVNOTES, `quality.ini` and `tools/check.py`. Reviewer: single-context review (self-review classification; no separate agent review).

Checks performed: static file inspection using the supplied feature-design and implementation-plan review operations and fixture AGENTS.md. No application commands or tests executed; runtime correctness and human acceptance are unverified. The documented gate, `"${CANARY_PYTHON:-python3}" tools/check.py`, exists, discovers `qa/check_*.py` through `quality.ini`, and rejects zero discovered tests.

Open findings: R1–R3. Next action: correct the validation decision and first-stage acceptance together, and put that outcome first. Implementation remains a separately assigned task; no additional approval round is required by this review.

## Findings

### R1 — High: filtering bypasses mandatory whole-input validation

**Location:** [D1 lines 86–94](../DESIGN.md#L86); [request lines 11–18](../ORIGINAL.md#L11); `inventory.py:20–42,71–75`.

With the standard header, `A1,Widget,1,2` followed by ` A1 ,Again,9,2` would discard the second row before checking its duplicate SKU. Likewise, `B2,,9,2` or `B2,Widget,9,2,extra` would evade required label/shape checks. D1 would then replace the destination successfully despite invalid input; an atomic writer cannot correct skipped validation.

**Minimal correction:** call the existing full `load_inventory` first in both modes, then optionally select validated records with `quantity <= reorder_at` before calling the unchanged writer. This preserves normalization, order and the all-or-nothing boundary within the stated small in-memory scope.

**Verification:** statically confirm validation precedes selection for every row. In the later implementation, the examples above must exit 2 and preserve existing destination bytes in flag mode; retain malformed-number coverage too. **Disposition: open.**

### R2 — High: Stage 1 acceptance defers a required dependency

**Location:** [P1 lines 86–95](../PLAN.md#L86); request lines 9–18.

Stage 1 is declared ready for use after testing only selected-row errors; whole-input validation and omitted-row regressions are postponed to Stage 2. Thus the duplicate example in R1 can meet Stage 1's stated acceptance while violating the required export contract. Existing tests exercise the default loader and cannot establish the new flag's behavior.

**Minimal correction:** move Stage 2's validation and regression outcomes into Stage 1, yielding one coherent increment with code, tests, CLI help and README. Require flag-mode errors anywhere to preserve the destination, alongside default compatibility, equality, header-only input and no matches. Keep the existing configured gate and explicit expected outputs.

**Verification:** the revised first-stage acceptance must reject R1's examples before any usable delivery; later execute the documented gate with those regressions included. **Disposition: open.**

### R3 — Medium: the actionable contract and next step are buried

**Location:** D1 lines 3–84 versus 86–98; P1 lines 3–84 versus 86–96.

A developer opening either document sees several screens of CSV, helper and temporary-file mechanics before learning the proposed behavior or deliverable. This makes the crucial validation choice and Stage 1 dependency hard to find quickly and leaves routine implementation detail dominating the plan.

**Minimal correction:** lead D1 with the corrected behavior, validation boundary and decisive examples; lead P1 with the single next outcome and acceptance. Remove redundant mechanics or move useful background below those decisions. No new document or expanded workflow is needed.

**Verification:** the opening screen of each document should identify the flag behavior, full-input validation requirement and next delivery/acceptance action without searching through maintenance notes. **Disposition: open.**
