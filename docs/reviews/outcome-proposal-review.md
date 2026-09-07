# Outcome proposal — independent review

**Verdict: needs changes. Open: OPR-01, OPR-02.** The direction is sound; tighten the outcome and iteration decisions before freezing the concrete evaluation contract. Neither finding requires another framework or case family.

Reviewed 7 September 2026 in a separate sidecar context. This is a proposal review, not implementation acceptance or human approval. The primary author is still preparing concrete cases; their absence is not a finding.

## Reviewed identity and scope

- Proposal: `docs/proposals/outcome-workflow.md`, SHA-256 `818ffdc494b07b60278a1ae6ca62382dba873ff89e7321af7e42fb8a1432fcee` (untracked at inspection).
- Tracked context: HEAD `b9087c56f2b136aff7c4b3495fffeccdfe760a28`: `AGENTS.md`, `DEVNOTES.md`, all four `skills/*/SKILL.md`, relevant review/write/execute/setup prompts and artifact templates, `evals/README.md`, and selected existing case requests/rubrics.
- Case index: `evals/cases/README.md`, SHA-256 `8f4972d4e5bc652519ac2d1a8cceb324c73a2a42c74081e518ec853efa0463b1`.
- Inspection was static. No behavioral trials, expensive canaries, product edits, commits, pushes, or external-source verification. Only this review file was written. Exact proposal quotations below bind findings even if the live proposal changes.

## Global judgment

Selecting depth before producing artifacts is the useful change. Combined local design/planning, bounded investigation, retained authorization, and material-only rechecks directly address the reported pains. Five complementary cases and three independent checkpoints are reasonable; their count alone is not needless machinery.

However, much of the proposed discipline already exists. The current planning skill says, “Code and tests own implementation detail.” Its review prompt says, “Do not require endless rounds or treat agent preferences as mandatory changes.” The design skill already says, “Scale detail to risk and available time.” Adding similar prose would not establish improvement. The useful experiment is whether agents actually omit unnecessary work while retaining consequential reasoning and checks.

The restricted reader is appropriately labeled a machine proxy. First-screen success cannot establish human reading effort, and passing behavior cases cannot establish that a ten-minute small-feature review has improved. The proposal should make those distinctions determine the outcome of this exercise, not merely appear in its limitations.

## Material findings

### OPR-01 — P2 — Passing cases does not decide whether the user's burden improved

- **Location / exact passage:** proposal line 32: “Report elapsed time and document/review churn as observations; no universal latency or productivity claim.” Line 36 asks, “does it reduce developer effort,” but supplies no disposition for unchanged or worse effort.
- **Trigger:** Both versions pass correctness and first-screen questions, while the candidate still takes ten minutes to review a small change, requires as much document synchronization, or shifts work into extra reviewer/reader calls.
- **Consequence:** A green result index can coexist with all the original workflow costs. The evaluation can reward proxy compliance without establishing the revision's stated outcome.
- **Minimal correction:** Predeclare a short comparison decision for the local-delivery pair: improved, unchanged, regressed, or inconclusive, with task-specific evidence for reading/next-action usability, review/fix effort, and document maintenance. Account for the whole delivery path and report evaluation-only overhead separately. An unchanged/inconclusive result supports retaining the baseline or withholding an improvement claim; it should not automatically trigger more instructions. Preserve correctness requirements and leave human usability acceptance pending until owner review. No universal time or word threshold is needed.
- **Verification:** Walk through a hypothetical pair with all semantic criteria passing but equal or worse review/churn cost. The frozen contract must produce an explicit non-improvement disposition, rather than equating case readiness with success of the revision.
- **Disposition:** Open.

### OPR-02 — P2 — Candidate-by-candidate limits leave the improvement loop unbounded

- **Location / exact passage:** proposal line 32: “Run each required case once per frozen candidate; a demonstrated failure permits a documented fix and affected rerun.” Line 36: “At three checkpoints (test contract, first paired results, final candidate), independently examine the whole workflow”.
- **Trigger:** Repeated revisions fix individual failures but introduce another failure or more process. Each revision qualifies for another affected run, and the final-candidate checkpoint keeps moving away.
- **Consequence:** The overnight improvement process can reproduce the user's endless-fix problem while satisfying the per-candidate rule. A global reassessment after the first pair and at the eventual end can miss prolonged local optimization between them.
- **Minimal correction:** Carry the existing run-budget policy into a cumulative iteration budget for this exercise, and trigger an additional global reassessment when the same material failure recurs or effort fails to improve. At that boundary, choose a simpler approach, retain the baseline, or report unresolved work; do not automatically append another general rule or rerun. This needs a recorded decision, not a scheduler or new runner subsystem.
- **Verification:** A hypothetical sequence of successive candidates with recurring failures must reach a named reassessment/stop condition before another automatic attempt. Preserve all attempts and distinguish unfinished work from acceptance.
- **Disposition:** Open. Existing `evals/README.md` already says “Set the budget before running”; this finding concerns cumulative candidate iteration and stalled progress, not missing invocation timeouts or permission to run trials.

## Suggestions — nonblocking

- **OPR-03 — Transfer beyond rehearsed examples.** Proposal line 15 uses “an occupied-cell extension” and “A settings migration”; both are already explicit examples in current drafting/planning prompts and existing cases. Prefer an unfamiliar small application for the planned `bounded-delivery` case, with ordinary requirements that do not prescribe a short note, stage count, or desired review verdict. This strengthens transfer evidence without adding a sixth case. Concrete cases may already address it.
- **OPR-04 — Make the short route survive the leaf prompts.** Line 9 permits “one short note and one review,” while current planning starts from a “reviewed design” and execution requests a “stage plan/current stage.” During implementation, remove or qualify incompatible defaults in the affected prompts/templates, and clarify that the combined review covers design/planning while the recorded code-review policy still applies. Verify the existing planned delivery case through completion; avoid adding a routing document or mandatory classification artifact.

**Next action:** Resolve OPR-01 and OPR-02 in the proposal or linked frozen case contract, recording their dispositions. Then proceed with the authorized baseline/candidate work. These findings call for two small decision rules, not another documentation layer.
