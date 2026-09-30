# Current evaluation contracts

**Requirements → real case criteria → known-output scoring checks.** The four
[skill specifications](../docs/OUTPUT_REQUIREMENTS_PROPOSAL.md) define the product.
Case `rubric.json` files contain the executable scoring instructions; `goals`
links each criterion back to a specification row. A link or ID alone is not a test.

**Partial migration:** the skill cards specify operation-scoped P1 dimensions,
1–5 anchors, limited P0 boundaries and nonblocking P2 preferences. Readability is
the last step of the same task. `v1-small-feature`, `v3-maintenance` and
`bounded-delivery` and the newer focused cases described below use that executable
contract; the remaining legacy cases retain their binary rules. Definition review, scorer qualification and actual worker results
remain separate; [validation](../docs/VALIDATION.md) records completed trials and
limitations. See the [current contract](../docs/specs/evaluation.md).

The new `smoke-code-review-required-tests` uses that priority contract for a
focused policy contrast: correct code still needs the explicitly required durable
regressions before approval. It is paired with the ordinary code/test-review case; its
automatic scorer qualification is not established.

`smoke-version-prepared` checks the complementary preparation state: the correct
version and notes already exist, so no second bump is due. Its P1 criteria assess
policy-based metadata and useful, proportionate delivery; protected scope and
the hard deadline remain P0. Seven case-scoped scorer controls cover sufficient
and cosmetic-equivalent outputs, a second bump, lost history, an unauthorized
commit, and separate target/hard-cap overruns. They qualify only the readiness
boundary; [validation](../docs/VALIDATION.md) records actual qualification and
worker evidence separately.

`bounded-delivery` rubric v7 makes review evidence attribution explicit within its
existing P1 review criterion. Six scoped scorer controls contrast attributed prior
checks, direct/indirect/supplied source inspection, unsupported inspection claims,
borrowed execution and incomplete capture. They exercise the scorer, not the skill.
Original worker outputs and historical grades retain their original rules.

## Independently testable operations

**An operation takes fixed prerequisites and produces one useful result.** A
multi-round test still checks continuity, but cannot substitute for a single-round
test. Each case below has its own concrete `rubric.json`; related acceptance
criteria stay together rather than becoming a test for every sentence or tool call.
“Existing” and “new” describe definitions, not passing model results. Current
[execution status](../docs/VALIDATION.md) distinguishes fixture checks, scorer
calibration and skill trials.

| Skill / responsibility | Independent cases | Coverage boundary |
|---|---|---|
| Design: clarify or investigate | Existing `smoke-intake-preserve`, `smoke-intake-conflict`, `existing-intake`, `bounded-investigation` | Preserve settled facts; resolve consequential uncertainty. Heavy cases here already perform one operation. |
| Design: draft / amend | New `smoke-design-new`; existing `smoke-design-local`, `smoke-transfer-design` | New design versus local amendment; full validation/recovery must survive concise output. |
| Design: initial review | Existing `smoke-design-review-ready`; new `smoke-design-review-defective` | Accept sufficient work; catch a real validation defect with counterexample and minimal correction. |
| Design: recheck | New `smoke-design-recheck-partial`, `smoke-design-recheck-complete` | Frozen revision plus original finding; verify whole pose/continuation contract. |
| Plan: create | Existing `smoke-plan-delivery`, `smoke-plan-preview-import` | Observable next outcome, available dependencies and decisive acceptance. |
| Plan: maintain | Existing `smoke-plan-maintenance`; new `smoke-plan-amend` | Private edits need no rewrite; changed public contract amends pending work without falsifying completed history. Accepted design is supplied. |
| Plan: initial review | Existing `smoke-plan-review-ready`; new `smoke-plan-review-defective` | Reject acceptance that defers a required invariant; do not demand prose code/test inventories. |
| Plan: recheck | New `smoke-plan-recheck-partial`, `smoke-plan-recheck-complete` | Distinguish prerequisite wording from actual ordering/availability plus compatibility. |
| Stage: implement | Existing `counter-stage` | Real behavior and gates; this single-operation heavy case does not need duplication. |
| Stage: initial code review | New `smoke-code-review-ready`, `smoke-code-review-defective` | Inspect real state transitions and test limits; passing cursor-only tests cannot hide selection mutation. |
| Stage: fix a finding | New `smoke-fix-finding` | Full-state repair and regression, valid-command compatibility, actual gate; author verification is not independent closure. |
| Stage: recheck | Existing `smoke-review-partial`; new `smoke-code-recheck-complete` | Incomplete repair stays open; complete repair closes against identified content. |
| Stage: resume / handoff | Existing `smoke-stage-resume`, `smoke-stage-stale`, `smoke-handoff-opening` | Reuse applicable evidence; reject stale readiness; expose remaining action. |
| Workflow: inspect / repair checks | Existing `smoke-setup-evidence`, `smoke-setup-child-evidence`, `smoke-setup-baseline` | Observe actual execution and preserve effective tools. |
| Workflow: installed hook | New `smoke-setup-hook` | Verify real installed delegation, including failing/empty suites when only docs are staged. |
| Workflow: coverage | New `smoke-setup-coverage` | Application-only branches/missing lines/current report; preserve gate and existing threshold policy. Prepared coverage is a fixture prerequisite. |
| Workflow: document ownership | New `smoke-doc-ownership` | README users, root DEVNOTES contributors, CHANGELOG completed impact, AGENTS constraints; retained linked history. |
| Workflow: PR draft | Existing `smoke-pr-scope`, `smoke-transfer-pr` | Complete intended diff, actual validation and honest readiness. |
| Workflow: version / notes | `smoke-version-notes`, `smoke-version-prepared` | Select the policy-based target from a released baseline, or reuse already prepared metadata; preserve history without executing a release. |
| Workflow: release readiness | Existing `release-ready`, `release-stale` | Current versus stale acceptance; already independent assessments. |
| Workflow: retry decision | New `smoke-release-retry-matching`, `smoke-release-retry-conflicting`, `smoke-release-retry-unknown` | One frozen offline observation each; assess identity/status. These do not test live observation acquisition. |

The 19 additions derive from the retained inventory, session, rover and release
fixtures, with narrower requests and independently supplied prerequisites. Existing
fixtures remain unchanged. Each new rubric checks the concrete outcome, scope and
evidence, a usable opening, and complete-trace effort. A short output is not a speed
result; no universal deadline is invented. Scoring control availability is separate
from case availability: `calibrate --case` reports missing contrasts before model
execution. Do not mistake JSON validity for calibrated judgment.

Retain `v5-review-recheck` and `plan-review-recheck` for continuity across actual
rounds; `v6-execution-handoff` and `bounded-delivery` for review/fix/convergence and
authorized commit; `workflow-setup` for combined setup/PR; `local-release-execution`
for tag/build/artifact/publication and observation acquisition; transfer tasks for
whole-deliverable behavior and accumulated workflow cost. Those integration-only
boundaries remain explicit, not silently relabeled as atomic coverage. Automatic
impact selection still conservatively selects by skill bundle, not operation.

## What each requirement is tested against

These are representative direct checks, not a claim that one case covers every
possible failure. Full mappings are in the rubrics. Existing criteria were retained
and case/rubric versions advanced; historical results keep their original meaning.

| Goal | Case and decisive distinction |
|---|---|
| A1 — contract | `smoke-intake-preserve/conflict`: preserve settled defaults; expose a real incompatible promise |
| A2 — usable design/intake | `smoke-design-local`: current decision/example first versus buried behind history |
| A3 — adequate reasoning | `smoke-transfer-design`: supported interruption/retry guarantee versus unsupported safety claim |
| A4 — local amendment | `v1-small-feature` → `v2-scope-extension`: preserve original movement/history and real later YAML scope |
| A5 — design review | `smoke-design-review-ready`: independent D1 review; `v5-review-recheck`: partial fix stays open; complete new revision closes with evidence |
| A6 — design effort | Design/intake/review traces: stop at sufficient output; reject needless reloading/rewriting |
| B1 — next outcome | `smoke-plan-preview-import`: preview is next; confirmation comes later |
| B2 — dependencies | `smoke-plan-delivery`: exporter support must be available before client adoption |
| B3 — acceptance | Same case: preserve old CSV client and verify JSON behavior within delivery stages |
| B4 — plan maintenance | `smoke-plan-maintenance` / `v3-maintenance`: private edits leave plan stable; public changes amend affected work |
| B5 — plan review | `smoke-plan-review-ready`: independent P1 review against accepted D1; `plan-review-recheck`: added prerequisite wording is insufficient; corrected order plus compatibility resolves it |
| B6 — planning effort | Plan/recheck traces: no prose test inventory or repeated policy/review cycles |
| C1 — working behavior | `counter-stage`, complete transfer cases: independently checked behavior and meaningful assertions |
| C2 — real checks | Counter and unchanged/stale resume cases: current observed execution, no inferred pass |
| C3 — review closure | `smoke-review-partial` / `v6-execution-handoff`: whole invariant, actual reviewer, identified revision |
| C4 — continuation | Handoff/resume cases: current output, check state, remaining review and next action are clear |
| C5 — execution effort | Stage traces: mandatory/changed-input checks are valid; unchanged reassurance loops are waste |
| D1 — usable setup | `workflow-setup`: installed hook actually runs tests and propagates failures/empty discovery |
| D2 — coverage | Same case: current application lines/branches and missing lines; no invented threshold |
| D3 — document owners | Same case: user usage, contributor commands, completed change notes and agent rules have clear owners |
| D4 — whole PR | `smoke-pr-scope`: retain required CSV; identify unrelated preview and actual readiness |
| D5 — lifecycle | Ready/stale assessment plus `local-release-execution`: exact version/tag/artifact and distinct retry states |
| D6 — workflow effort | Setup/PR/release traces: reuse adequate tools and evidence; no needless rebuild or republish |

## How scoring is checked

[Known outputs](graders/calibration.json) pair useful results with concrete defects,
including correct-but-buried design, short-but-unsafe design, private-edit replanning,
premature/obsolete review closure, misleading coverage and false release claims.
Separate effort controls keep final quality fixed while changing the work trace.
They include a necessary extra review, valid compaction resumption, redundant loops,
missing completion, a supplied deadline exceeded after a draft was saved, and
reader/grader time excluded from worker time.

All 19 added independent operations now have complete authored, case-bound control
sets. Supported controls assess the full rubric. Negative controls select their
affected criterion, retaining other judgments only where separately justified;
together they cover every required pass/fail contrast. The remaining 15 sets have
definition review, not model calibration or worker acceptance. Actual worker runs
still receive the full case rubric.
This uses existing criterion subsets without reducing worker acceptance or adding
a scoring mechanism. Combined scope/effort interactions remain only partly tested.
The shared [cost acceptance](../docs/specs/evaluation.md#efficiency-and-context)
now distinguishes incidental navigation from material avoidable work relative to
the task. Small repetitions can accumulate into a material burden; hard deadlines,
unnecessary full review/gate cycles, costly replay and duplicated maintenance remain
failures. There is no universal command or time allowance. Original disagreements
and their prior rule versions remain in the run record.

Each new control copies the selected **actual case criteria** and declares every
expected criterion status. Fast checks reject drift between those copies and the
case. A blind scoring invocation sees task/evidence/criteria, never the expected
answers; it must give literal supporting evidence. A mismatch needs diagnosis,
not an automatic change of the answer key. Correct scoring of authored examples
does not establish real worker quality, human usability or stable speed.

Named groups: `specifications-output`, `specifications-effort`,
`specifications-lifecycle`, `specifications-input-contract` (source-aligned design
and counter controls), plus `specifications-release-recheck` (corrected release
criterion scope and preserved artifact citations) and `specifications-history-recheck`
(original-versus-candidate history evidence). [Commands and evidence rules](README.md#change-a-case-or-grading-rule).
The two new case fixtures also have deterministic positive/negative oracle controls;
those verify executable inputs/checks, not semantic grading.

`calibrate --case CASE` checks all linked controls for that case and their required-criterion contrasts; a passing record supports only that case. The separate design/plan review controls each distinguish supported review, invented blocker/verification, buried verdict and needless repeat work. Other incomplete case sets stop with their missing criteria. Diagnostic groups and full release calibration retain their distinct scopes.

## Scope and remaining evidence

Actual design and repair outcomes exposed two extra template obligations that the
original skill/task contracts did not require. Their opening criteria now require
next actions only for real pending work/decisions/dependencies, and an additional
repair example only when the explanation otherwise leaves behavior unclear. Clear,
self-contained completion need not add boilerplate. Four focused scoring controls
pair those actual outputs with separately specified hidden-decision/review blockers.
The original failed worker grades stay intact; a new rubric or a diagnostic score
does not turn them into fresh worker passes. Under the historical rule, coverage
setup required its command, observed measurement and material gap in the handoff.
The prospective contract assesses whether those essentials are accessible and
accurate; it does not require repeating a command already clear in DEVNOTES.
A real measurement defect or unusable setup remains substantive.

The existing runner enforces supplied task deadlines;
without a justified target/comparison, a process pass is not a latency win.
Prospective local-task budgets in the specification await case migration and
must not be applied retrospectively or generalized to every workflow.
Required reviews/gates and real YAML/recovery requirements remain valid costs.

The release case creates tags only inside its disposable fixture and uses an
offline publication adapter. It cannot certify hosted release behavior.
Natural-language skill discovery, production-scale transfer and human acceptance
remain outside these checks. See [actual run status](../docs/VALIDATION.md).
