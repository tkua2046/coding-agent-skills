# Three current canaries before broader migration

Status: executable migration and offline gate passed; all three readiness control
sets qualified and all three real worker trials completed. The two scoped outputs
are usable by independent inspection but automatic scoring timed out. The full
workflow missed its 600s target at 894.839s. [Validation](../VALIDATION.md) owns the
current result and limits; this proposal preserves the decisions made before runs.

The existing cases cover useful failures, but their binary grading does not
implement the accepted priority contract. Migrate three existing cases through
the maintained runner, then test their scorer before running the frozen skills.

| Case | Requested outcome | Prospective target / hard stop |
|---|---|---|
| `v1-small-feature` | Amend obstacle design and pending plan; preserve settled movement/history; make decisions and acceptance easy to read. | 300 / 600 seconds total |
| `v3-maintenance` | Private helper/test maintenance leaves public decisions stable; a subsequent public stop-on-block change updates affected pending decisions. | 300 / 600 seconds per phase; 600 / 1200 total |
| `bounded-delivery` | Inventory feature from decisions through required independent reviews, necessary fixes, tests and final handoff. | 600 / 900 seconds total |

The first two budgets apply the existing specification's supplied-prerequisite
operation limits. The last keeps its original 900-second whole-workflow ceiling
and reserves the last five minutes beyond the ten-minute usable target for
material corrections. These are acceptance budgets, not observed speed promises.
Count all worker phases, including development reviewers and fixes; exclude the
separate evaluator reader/scorer and report their cost separately. Stop remaining
worker work at the declared hard limit; retain incomplete output and known fails.
The contractual clock is cumulative elapsed time of actual worker invocations
(CLI/model/tools/waits), with each next call capped by the remaining workflow and
phase allowance. Skipped phases consume no worker time. Record harness/evaluator
overhead separately; an earlier known deadline or core failure remains visible
if a later phase or evaluation cannot complete.

## Maintained contract

- Version the selected cases/rubrics. Preserve their pre-edit trees, grader,
  controls and runner in the ignored evidence archive before editing.
- Add `scoring: priority-v1` to the selected rubrics. Each criterion declares
  `id`, `priority`, `operation`, `goals`, `requirement`, and `evidence`; P1 also has
  concrete `anchors` for 1 through 5; P0 has an explicit `condition`.
- Keep the existing grade row (`id`, `status`, `reason`, exact cited `evidence`)
  and add `score` for priority rubrics. P1 uses 1–5 or null; 3 is sufficient.
  P0/P2 scores are null. Validate status/score agreement; P2 never blocks.
  A known core failure outranks missing evidence; missing evidence is not zero.
- Existing binary cases keep their historical interpretation. No new runner or
  parallel trial configuration. Extend existing case calibration with expected
  score ranges and a cosmetic-equivalence contrast; expected labels stay hidden.
- Freeze meaningful positive/negative/cosmetic controls for these exact cases.
  Controls test decision boundaries and time judgments, not prompt phrasing.
  Reference outcomes may be authored, but must be clearly labeled as such and
  never represented as actual worker runs. A compact high-score range check
  prevents interpreting an uncalibrated 4/5 as precise achievement.

## Delivery stages and acceptance

1. **Executable selected contracts:** reviewed case requirements, anchors,
   budget enforcement, numeric grading/calibration and backward compatibility.
   Focused tests catch invalid scores, cosmetic vetoes, missing evidence,
   stale control reuse and a hard-limit breach across worker phases.
2. **Scorer acceptance:** fresh Sol/medium scoring of known outcomes with exact
   evidence; real workers start only for cases whose declared controls pass.
   Preserve and diagnose failures; do not tune expectations to obtain green.
3. **Actual skill evidence:** one current Sol/medium run per eligible case.
   Inspect produced documents/code, actual checks and complete workflow cost;
   an independent reviewer checks substantive conclusions. Publish a short
   local result index with originals, limitations and unrun scope, then run the
   repository's required fast gate on stable files.

Definition-review corrections preserve V1's truthful check/review reporting as
P1, protect the supplied phase mutation boundaries, and judge V3's individual
phase targets as well as its total. Pure preferred formatting is advisory text,
not a mandatory extra grading row. The selected controls include an isolated
phase-target miss and an out-of-scope phase mutation as well as the full outcomes.

No skill changes are planned by this migration. An observed skill defect needs
a separate, explained correction and affected regression; no broad prompt
rewrite or full-suite release claim. No source commit/push, installation or tag.

## Prospective qualification after the first scorer campaign

Independent inspection found that several supplied usable outcomes plausibly
match the literal 5 anchors; the former expected upper bound of 4 is not a
reliable precision test. One handoff explanation also overstated evidence for
repairing stale status. Original ranges, judgments, disagreements and two scorer
timeouts remain retained; none becomes an original passing calibration.

These three case versions now explicitly qualify the readiness boundary only:
usable/cosmetic P1 scores must be 3–5; material defects stay 1–2, declared time
contrasts and P0 violations remain required, and missing evidence stays unknown.
Original 3–4 ranges remain diagnostic metadata. All inputs, rubric anchors and
substantive expectations stay in scope. A generic grader brevity refinement
reduces repeated explanation/quotation while preserving exact evidence checks.
Fresh calibration must pass before worker runs. Returned 4/5 scores are
descriptive and uncalibrated; they cannot establish superiority or full release
qualification. No new runner, record type or replay system is introduced.
