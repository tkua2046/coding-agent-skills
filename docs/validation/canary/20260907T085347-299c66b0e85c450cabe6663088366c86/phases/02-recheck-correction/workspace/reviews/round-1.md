# Round 1: movement design recheck

Verdict: **needs changes**. Candidate: `docs/DESIGN.md`, D2, SHA-256 `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46` (307 bytes).
Open findings: **R1** (original finding retained). Next action: change the occupied branch to preserve both coordinates as well as heading, then recheck the entire pose invariant.

Reviewer: independent static reviewer in a separate fresh agent context (`/root/independent_recheck`), with primary-agent evidence verification and report assembly. No runtime or human acceptance is established.

## Reviewed scope and checks performed

Read the fixture's `AGENTS.md`, supplied feature-design skill, review prompt and template, README and DEVNOTES. Compared the exact candidate with `docs/ORIGINAL.md`, `docs/history/R1.md`, and historical D1/D2. Used line-numbered source inspection and a manual transition trace; computed byte counts and SHA-256 identities with the prepared `CANARY_PYTHON` standard library. The candidate is byte-identical to historical D2.

| Source | SHA-256 |
|---|---|
| `docs/ORIGINAL.md` | `5fedb27fa9d0c6f809287c2e72085d986e503e231ecaa360f272552dd152d0ff` |
| `docs/history/R1.md` | `1c4bd90a82544ca086d5ff6fd4ba92c274f3de966bdeece5fabb2dd3146acda4` |
| `docs/history/D1.md` | `f1776e48729f301ef86708d22388f08f4a87a15935d42415f4c42e007ebb3f15` |
| `docs/history/D2.md` | `74f4bc3b9dcacd4239a9a172f1d398f11d2a0b92d9947b0a34924f35109ada46` |

Static review only: no implementation or runtime tests, installs, commits, or external actions. An initial `shasum` attempt failed because the sandbox blocked its Perl dependency; Python hashing succeeded. `git status --short` emitted sandbox cache/config warnings, so content hashes are the review identity and preservation evidence.

## Findings

### R1 — High priority: blocked movement still changes position

- Location/source: [candidate lines 3–4](../docs/DESIGN.md) versus [original requirement lines 2–3](../docs/ORIGINAL.md); [original R1 lines 2–5](../docs/history/R1.md), first raised against D1.
- Trigger/example: start at `(2,3,1)` facing east with `(3,3)` occupied and issue `F`. Candidate line 3 says “If occupied, assign x/y to that target”; line 4 retains heading and emits `False`. The specified result is therefore `(3,3,1), False`, whereas the required result is `(2,3,1), False`.
- Consequence: failed movement corrupts caller position and places it at the occupied target. Accepting subsequent commands does not repair the corrupted starting state.
- Minimal correction: in the occupied branch, leave `x`, `y`, and heading unchanged and report `False`. Assign the target only for successful movement.
- Verification: statically trace the original R1 example and a blocked move that would change `y`; require the complete output pose to equal the input pose and failure to be reported. Check that later commands remain accepted and turns update heading without changing position. These are proposed correction checks, not executed runtime tests.
- Disposition: **open; partial correction verified**. The author calls D2 a proposed correction awaiting review (line 2). Heading preservation is verified in the text, but resolution of the full original concern is not.

## Full affected invariant

| Required behavior | Candidate evidence | Static assessment |
|---|---|---|
| Blocked `F` preserves `x` and `y` | Line 3 assigns the adjacent occupied target | Fails |
| Blocked `F` preserves heading | Line 4 retains original heading | Corrected |
| Blocked `F` reports failure | Line 4 emits `False` | Satisfied |
| Later commands remain accepted | Line 5 explicitly continues acceptance | Satisfied |
| Turns update heading in place | Line 5 states this behavior | Satisfied |

Reading cost is low: the five-line candidate exposes the status and transition directly, and terminology is adequate for this fixture. No separate material reading-cost issue was identified. The unaffected successful-movement branch does not need a new finding on the supplied evidence.

## Recheck history

| Round / candidate | Finding ID | Observation and evidence | Current disposition |
|---|---|---|---|
| Original review / D1 | R1 | Historical R1 records changes to both position and heading on failure; D1 line 2 specifies both mutations. | Original open finding preserved unchanged |
| Round 1 / D2, identity above | R1 | Candidate line 4 preserves heading; line 3 still overwrites position. Original example still violates full pose preservation. | Open; partial correction verified |

## Next action

Correct the occupied branch and recheck R1 against the complete original requirement. Preserve the original finding and this report as history; the candidate is not ready on current evidence.
