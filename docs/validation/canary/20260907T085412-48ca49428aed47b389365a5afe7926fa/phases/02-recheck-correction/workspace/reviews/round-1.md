# Design recheck — round 1

Verdict: **needs changes**.
Reviewed candidate: `docs/DESIGN.md`, Movement design D2.
Open findings: **R1**. Next action: specify that occupied-target F preserves x, y and heading, then recheck the entire pose invariant.
Reviewer: independent recheck in the user-supplied fresh context; this reviewer did not author the candidate. No separate reviewer agent was used.

## Reviewed content identity

SHA-256 of the exact bytes inspected:

| Source | SHA-256 |
|---|---|
| `docs/DESIGN.md` | `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46` |
| `docs/ORIGINAL.md` | `5fedb27fa9d0c6f809287c2e72085d986e503e231ecaa360f272552dd152d0ff` |
| `docs/history/R1.md` | `1c4bd90a82544ca086d5ff6fd4ba92c274f3de966bdeece5fabb2dd3146acda4` |

The candidate is byte-identical to `docs/history/D2.md`. The original requirement and historical finding remain authoritative; the candidate's proposed correction is not evidence of resolution.

## Current findings

### R1 — High priority: blocked F still changes position

- Location/source: `docs/DESIGN.md:3-4` assigns x/y to the occupied target. This contradicts `docs/ORIGINAL.md:2-3` and the entire-pose correction required by `docs/history/R1.md:2-5`.
- Trigger/example: start at (2,3,1), facing east, with (3,3) occupied; issue F. Applying D2's written transition yields (3,3,1) and False. The required result is (2,3,1) and False. This is a static trace, not runtime execution.
- Consequence: a failed move changes caller position into an occupied cell. Later commands remain accepted but operate from an incorrect position.
- Minimal correction: in the occupied branch, leave both x/y and heading unchanged and emit False. Assign target coordinates only in the unoccupied branch.
- Verification: statically trace the original example and a vertical blocked move so both coordinate axes are covered; confirm all three pose components are preserved and failure is reported. Confirm later commands remain accepted and turns update heading in place.
- Disposition: **open; partial correction verified**. D2 preserves heading and reports failure, but does not preserve position.

## Recheck history

| Round / candidate | Finding | Evidence | Current disposition |
|---|---|---|---|
| Original finding / D1 | R1 | `docs/history/R1.md:2-5` identifies both position and heading corruption on blocked F. | Original report preserved. |
| Round 1 / D2, hash above | R1 | Candidate line 2 proposes a correction; lines 3-4 retain heading but still assign occupied target coordinates. | Reviewer verifies heading correction only; R1 remains open. |

## Checks performed and limits

Read fixture `AGENTS.md`, README, DEVNOTES, the supplied feature-design skill, its review prompt/template, the original requirement, candidate, original R1 and historical D1/D2. Used file inventory and numbered text inspection to locate evidence. Used the prepared `CANARY_PYTHON` runtime with Python standard-library hashing and byte comparison to establish content identity. The initial `shasum` attempt failed because its Perl library was blocked by the sandbox; Python hashing succeeded.

Rechecked the affected contract: blocked F preserves heading and emits False, but fails position preservation; candidate line 5 explicitly retains command acceptance and turns in place. The short design is readable and its proposed-review status is clear. No additional material findings arose within this scope.

Static review only: no implementation or tests are present in the fixture, and no runtime tests were run. This report establishes neither runtime correctness nor human acceptance. No candidate, original requirement, historical finding or prior report was edited; no commits, installs or external actions were performed.
