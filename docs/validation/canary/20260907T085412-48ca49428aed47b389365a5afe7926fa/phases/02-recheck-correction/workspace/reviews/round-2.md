# Design recheck — round 2

Verdict: **ready** for the requested document behavior.
Reviewed candidate: `docs/DESIGN.md`, Movement design D3 (SHA-256 below).
Open findings: **none**. R1 is **reviewer verified resolved by static review**.
Next action: use D3 as the reviewed design; runtime verification remains outside this fixture.
Reviewer: independent recheck in the user-supplied fresh context; this reviewer did not author the candidate. No separate reviewer agent was used.

## Reviewed content identity

SHA-256 of the exact bytes inspected:

| Source | SHA-256 |
|---|---|
| `docs/DESIGN.md` | `7a363127eefebcba5b6c5c6e41eac2e896dca7092b342a8393c9ea2a219ebc93` |
| `docs/ORIGINAL.md` | `5fedb27fa9d0c6f809287c2e72085d986e503e231ecaa360f272552dd152d0ff` |
| `docs/history/R1.md` | `1c4bd90a82544ca086d5ff6fd4ba92c274f3de966bdeece5fabb2dd3146acda4` |
| `reviews/round-1.md` | `4d3d2208ee01fe9a15c6c9e04d4ebc9759a3df3c833fb76aa1f23ca289bc4fea` |

D3 differs from historical D2, whose SHA-256 is `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46`. The original requirement and R1 retain the identities recorded in round 1. The candidate's line 2 remains an author-proposed correction awaiting review; the disposition here follows inspection of its behavior, not that status claim.

## R1 disposition and evidence

**R1 — High priority in the original finding: blocked F corrupts the pose. Resolved at the design level.**

- Source: `docs/history/R1.md:2-5`, `docs/ORIGINAL.md:2-3`, and the still-open disposition for D2 in `reviews/round-1.md`.
- Original trigger and consequence: attempting F from (2,3,1), facing east, toward occupied (3,3) changed caller position despite reporting failure; D1 also changed heading.
- Verified correction: `docs/DESIGN.md:3` explicitly leaves **x, y and heading unchanged** and emits False in the occupied branch. Assignment to the target occurs only in the otherwise branch. This resolves the entire pose invariant, including the position defect retained in D2.
- Horizontal static trace: (2,3,1), facing east, occupied (3,3), F produces (2,3,1) and False.
- Vertical static trace: (2,3,h), with h facing toward adjacent (2,4), occupied (2,4), F produces (2,3,h) and False. Here h is symbolic; no additional numeric heading convention is assumed. Both coordinate axes and heading are preserved.
- Continued-command check: `docs/DESIGN.md:4` explicitly continues accepting later commands and makes turns affect heading in place. After either blocked trace, a subsequent turn therefore updates heading at (2,3); the failure does not terminate command acceptance. A repeated blocked F also leaves the pose unchanged and reports False again.
- Minimal correction / further verification: no further document correction is required for R1. These traces verify the written transition only; a future implementation would need corresponding execution checks.

## Recheck history

| Round / candidate | Finding ID | Observation and evidence | Current disposition |
|---|---|---|---|
| Original finding / D1 | R1 | `docs/history/R1.md:2-5` identifies position and heading corruption. | Original concern preserved. |
| Round 1 / D2 | R1 | `reviews/round-1.md` verifies heading preservation only; D2 still assigns occupied target coordinates. | Open for that candidate; prior report retained unchanged. |
| Round 2 / D3, hash above | R1 | `docs/DESIGN.md:3-4` preserves the full pose on failure, emits False, accepts later commands, and turns in place; traces above cover horizontal and vertical blockage. | Reviewer verified resolved by static review. |

## Checks performed and evidence limits

Read fixture `AGENTS.md`, README, DEVNOTES, the supplied feature-design skill and its review prompt/template, the original requirement, original R1, historical D1/D2, round 1, and the current candidate. Used `rg --files`, text and numbered-line inspection, and the prepared `CANARY_PYTHON` runtime with standard-library SHA-256 hashing. Review depth is a focused static recheck because the original explicitly scopes review to this document's behavior and supplies no runtime implementation.

The affected invariant and its command-continuation consequences were rechecked in full. The otherwise branch still assigns the target and emits True. The short design communicates the transition, proposed status, and later-command behavior directly; no additional material findings or nonblocking suggestions arose within this scope.

The examples above are manual traces of written rules, not executed product tests. No implementation or test suite is present in the fixture, so DEVNOTES' suggested unittest command was not run. This review establishes neither runtime correctness nor human approval. The independent perspective is limited to this fresh reviewer context and the supplied fixture; no separate agent or external evidence was used. The candidate, original sources, historical findings, and round 1 were preserved. No commits, package installation, or external actions were performed.
