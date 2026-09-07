# Design recheck — round 1

Verdict: **needs changes**.
Reviewed candidate: `docs/DESIGN.md`, Movement design D2, SHA-256 `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46`.
Open findings: **R1** (original finding against D1). Next action: revise the occupied-target branch to preserve x, y and heading, then recheck the full invariant.
Reviewer: fresh-context static self-review using the supplied feature-design skill; no separate reviewer agent was used.

## Current findings

### R1 — Material: blocked F still corrupts position

- Location/source: [candidate lines 3–4](../docs/DESIGN.md#L3), [original requirement lines 2–3](../docs/ORIGINAL.md#L2), and [original R1 lines 2–5](../docs/history/R1.md#L2).
- Trigger/example: start at `(2,3,1)` facing east with `(3,3)` occupied, then attempt `F`. D2 assigns the target x/y and retains heading, yielding `(3,3,1)` and `False`. The required result is `(2,3,1)` and `False`.
- Consequence: unsuccessful movement changes caller position into the occupied cell. Preserving heading alone does not preserve the required entire pose.
- Minimal correction: for an occupied target, leave x, y and heading unchanged and emit `False`; continue accepting later commands.
- Verification: statically trace the example and confirm the occupied branch preserves every pose component for any blocked `F`, reports failure, and permits subsequent commands. Confirm turns still update heading in place.
- Disposition: **open**. The author labels D2 a proposed correction awaiting review, not a verified fix. The reviewer verifies only the heading portion is corrected; the position portion remains unresolved.

## Checks performed and evidence

Read fixture `AGENTS.md`, `README.md`, `DEVNOTES.md`, the supplied feature-design skill, its review prompt/template, the original requirement, candidate, and historical D1, D2 and R1. Compared the affected invariant by static inspection and traced the original R1 example; no runtime implementation is supplied or tested.

Candidate line 4 preserves heading and reports `False`; line 5 explicitly accepts later commands and keeps turns in place. Those portions match the original requirement. Candidate line 3 explicitly assigns occupied target coordinates, so R1 remains material. The short document makes its proposed outcome and transition easy to locate; no additional material reading-cost issue was found.

Content identities were calculated with Python standard-library SHA-256 through `CANARY_PYTHON`:

| Input | SHA-256 |
|---|---|
| `docs/ORIGINAL.md` | `5fedb27fa9d0c6f809287c2e72085d986e503e231ecaa360f272552dd152d0ff` |
| `docs/history/R1.md` | `1c4bd90a82544ca086d5ff6fd4ba92c274f3de966bdeece5fabb2dd3146acda4` |

The initial `shasum` attempt failed because its Perl library was blocked by the sandbox; Python hashing succeeded. Line-numbered source inspection used `nl -ba`. No tests, installs, commits or external actions were performed. Static review does not establish runtime correctness or human approval.

## Recheck history

| Round / candidate | Finding ID | Observation and evidence | Current disposition |
|---|---|---|---|
| Original R1 / D1 | R1 | Historical finding identifies changes to both position and heading on blocked movement; entire pose must be preserved. | Original report preserved unchanged |
| Round 1 / D2, hash above | R1 | D2 lines 3–4 retain heading but still assign occupied target x/y. Original example still fails position preservation. | Open; partial correction verified |

The candidate, original requirement, original finding and prior revisions remain unchanged. The verification described under R1 is the next check after a candidate correction, not a claim that such a correction exists.
