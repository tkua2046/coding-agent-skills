# Combined design and plan review

**Verdict: needs changes.** D1/P1's proposed first increment is not usable against the confirmed request. Open findings: R1–R3. Next action: correct validation order and first-increment acceptance, and surface those decisions at the start of the documents. Implementation remains a separately assigned task; no additional approval round is required by this review.

Reviewed scope/version: D1 and P1 as supplied on 7 September 2026, against `docs/ORIGINAL.md` (confirmed 4 September), the existing application and check configuration. Reviewer: single-context review (self-review designation; no separate reviewer).

Checks performed: static inspection of `AGENTS.md`, both supplied review skills, requirements, design, plan, `inventory.py`, `qa/check_inventory.py`, `tools/check.py`, `quality.ini`, README, DEVNOTES and sample CSV. No application commands or tests ran; runtime correctness and human acceptance are not established. No prior reports were present.

## Findings

### R1 — High: selection bypasses required whole-file validation

**Location:** `docs/DESIGN.md:86–94`; conflicts with `docs/ORIGINAL.md:11–18` and existing validation in `inventory.py:20–42`.

With rows `A1,Widget,1,2` and ` A1 ,Again,9,2`, D1 discards the second row before checking the normalized duplicate SKU. Similarly, `B2,,9,2` or `B2,Stock,9,2,extra` bypasses required label/shape checks. The selected list then reaches the writer, replacing previous destination bytes despite invalid input. Atomic replacement alone does not protect this contract.

**Minimal correction:** load and validate the complete input through the existing loader, then apply `quantity <= reorder_at` to its normalized records before calling the unchanged writer. This fits the confirmed in-memory scope and preserves default behavior.

**Verification:** statically confirm that every row passes existing validation before selection or writing. During later implementation, exercise the examples above with the flag and a pre-existing destination: expect exit 2 and identical destination bytes. **Disposition: open.**

### R2 — High: the first delivery postpones a mandatory dependency

**Location:** `docs/PLAN.md:86–96`, particularly Stage 2's deferral at lines 91–94; `docs/ORIGINAL.md:9–18`.

Stage 1 explicitly accepts validation only among selected rows and declares the worksheet ready. Thus the invalid duplicate example in R1 can satisfy Stage 1's checks and ship. Correcting D1 alone would leave contradictory delivery and acceptance instructions.

**Minimal correction:** bring whole-input validation and omitted-row regression coverage into the first usable increment; merge Stage 2 into Stage 1. Include header-only success, malformed numbers anywhere, and destination-byte preservation alongside the existing default, equality, order and no-match cases.

**Verification:** confirm no required behavior or its tests remains deferred beyond first acceptance. The later check command is `"${CANARY_PYTHON:-python3}" tools/check.py`: static inspection confirms it uses `quality.ini`'s `qa/` and `check_*.py` discovery and rejects zero tests. **Disposition: open.**

### R3 — Medium: the actionable content is buried

**Location:** `docs/DESIGN.md:3–85` and `docs/PLAN.md:3–85`; actual decision and sequence begin at line 86 in each.

A developer opening either document encounters extensive code-maintenance notes before learning the feature behavior or next deliverable. This makes the consequential validation/staging choices difficult to find quickly.

**Minimal correction:** move the corrected behavior, main consequence, acceptance and next increment immediately below each title/source link. Move supporting notes below them or link to the code; no new artifact or expanded template is needed.

**Verification:** the opening screen should answer what changes, when validation happens, and what the developer delivers and checks next. **Disposition: open.**
