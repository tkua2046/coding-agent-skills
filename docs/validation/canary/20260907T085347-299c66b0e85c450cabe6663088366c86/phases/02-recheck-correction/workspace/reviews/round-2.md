# Round 2: movement design recheck

Verdict: **ready** for the supplied document-behavior scope. Candidate: `docs/DESIGN.md`, **D3**, SHA-256 `7a363127eefebcba5b6c5c6e41eac2e896dca7092b342a8393c9ea2a219ebc93` (285 bytes).
Open findings: **none**. **R1 is reviewer verified as resolved by static inspection.** Next action: retain this review with the candidate; no further design correction is required on the supplied evidence.

Reviewer: **fresh-context self-review**, reassessed directly against the original requirement. A separate independent reviewer was requested, but the agent service failed to start it with “no thread with id.” No separate-agent review occurred in this round; this report does not claim that level of independence, human approval, or runtime correctness.

## Reviewed scope and checks performed

Read fixture `AGENTS.md`, the supplied `skills/feature-design/SKILL.md`, review prompt and template, README, DEVNOTES, the exact candidate, original requirement, original R1, historical D1/D2, and [round 1](round-1.md). Used line-numbered source inspection, comparison of the changed occupied branch, and manual transition traces below. Computed byte counts and SHA-256 identities with the prepared `CANARY_PYTHON` standard library.

| Source | SHA-256 |
|---|---|
| `docs/ORIGINAL.md` | `5fedb27fa9d0c6f809287c2e72085d986e503e231ecaa360f272552dd152d0ff` |
| `docs/history/R1.md` | `1c4bd90a82544ca086d5ff6fd4ba92c274f3de966bdeece5fabb2dd3146acda4` |
| `docs/history/D1.md` | `f1776e48729f301ef86708d22388f08f4a87a15935d42415f4c42e007ebb3f15` |
| `docs/history/D2.md` | `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46` |
| `reviews/round-1.md` | `7c966a0249809cff0b1c9652cff0f5d6163f10a0a26e51fdf51f37b94ba28e28` |

## Finding dispositions

### R1 — Originally high priority: blocked movement corrupts the pose

- Original round/source: [original R1](../docs/history/R1.md), lines 2–5, raised against D1; [round 1](round-1.md) kept R1 open against D2 because coordinates still changed. Those original concerns and dispositions remain preserved in their reports.
- Current location: [D3](../docs/DESIGN.md), line 3, compared with [original requirement](../docs/ORIGINAL.md), lines 2–3.
- Trigger/example: starting at `(2,3,1)` facing east with `(3,3)` occupied, issue `F`. D1 changed coordinates and heading; D2 still moved into the occupied cell despite reporting failure. D3 calculates the target but explicitly leaves `x`, `y`, and heading unchanged and emits `False`, yielding the required `(2,3,1), False`.
- Consequence of the original defect: caller pose was corrupted after failed movement, affecting subsequent commands. D3 removes the specified mutation from the occupied branch.
- Minimal correction requested: preserve the entire pose and report failure in the occupied branch; assign the target only in the successful branch. D3 line 3 now states this correction explicitly.
- Verification performed: traced the original east-facing example and a second case with initial pose `(2,3,h)`, where `h` faces an occupied adjacent target `(2,4)`. D3 yields `(2,3,h), False`, preserving `y` as well as `x` and heading. This second case uses a symbolic heading because the fixture supplies no numeric encoding for that direction. Checked later-command acceptance and turn behavior in line 4, as detailed below.
- Author claim: D3 line 2 says “author-proposed correction to R1; awaiting review.” This is a proposal, not evidence of acceptance.
- Current disposition: **reviewer verified — resolved at the design-text level**, based on line 3 and the full invariant recheck, rather than the author's status label. No remaining correction or decision is required for R1.

## Full affected invariant

| Required behavior | D3 evidence and static assessment |
|---|---|
| Blocked `F` preserves `x` and `y` | Line 3 explicitly leaves both unchanged; both coordinate-changing target examples preserve the starting coordinates. Satisfied. |
| Blocked `F` preserves heading | Line 3 explicitly leaves heading unchanged in the same branch. Satisfied. |
| Blocked `F` reports failure | The occupied branch emits `False`. Satisfied. |
| Later commands remain accepted | Line 4 explicitly continues acceptance. A command following either failed trace is accepted from the preserved pose. Satisfied. |
| Turns update heading in place | Line 4 says turns affect heading in place. A subsequent turn changes heading while retaining `(2,3)`. Satisfied; no particular turn encoding is assumed. |

The successful branch still assigns the target and emits `True`; the occupied-branch correction supplies no new evidence against that unaffected decision. The four-line candidate exposes its status and decisive transition on the first screen. Terms and examples are adequate for this bounded fixture; no material reading-cost issue or new finding was identified. There are no outstanding nonblocking suggestions or assumptions requiring a decision within the supplied requirement.

## Recheck history

| Round / candidate | Finding ID | Observation and evidence | Disposition in that round |
|---|---|---|---|
| Original / D1 | R1 | D1 line 2 changes coordinates and heading on blocked movement. | Open; original report preserved |
| Round 1 / D2, SHA-256 `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46` | R1 | D2 lines 3–4 preserve heading but still assign occupied target coordinates. | Open; partial correction verified; prior report preserved |
| Round 2 / D3, identity above | R1 | D3 line 3 preserves all three pose components and emits failure; line 4 retains continuation and turns in place. | Reviewer verified as resolved by static inspection |

## Evidence limits and next action

This is a review of documented behavior only, as explicitly scoped by the original requirement. Manual traces are deductions from prose, not executable tests. No runtime implementation is supplied and the fixture has no `tests` directory; the DEVNOTES unittest command was not run. No runtime correctness, human acceptance, or separate-reviewer independence is established. No packages were installed, and no commits or external actions were performed.

Retain D3 and this report as the reviewed snapshot. Preserve the candidate, original requirement, historical revisions/findings, and round 1 unchanged. If implementation is later introduced, runtime verification would be separate work; it is not a blocker for this document-only verdict.
