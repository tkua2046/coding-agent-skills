# Versioned workflow canary cases

These seventeen versioned heavy cases support the [goal-based refinement](../GOALS.md).
The owner authorized real baseline/candidate runs for this increment; ordinary small
edits still use the fast tier. Historical
archives in docs/validation informed scenario selection only; they are not runs or
new-test evidence for these cases. No private interview/project material is used.

| ID | Scenario / phases |
| --- | --- |
| existing-intake | Inspect formatter, observe legacy failure, clarify customization |
| counter-stage | Implement counter; required human and independent review remain pending |
| v1-small-feature | Design/plan occupied cells against completed navigation work |
| v2-scope-extension | Initial occupied-cell plan, then confirmed YAML/large-list extension |
| v3-maintenance | Private rename/regression, then plan a confirmed stop-on-block contract |
| v4-migration-risk | Design/plan interrupted migration and safe retry |
| v5-review-recheck | Static D2 incomplete-fix recheck, then corrected D3 recheck |
| v6-execution-handoff | Execute, review, fix, recheck, resume pending, scripted acceptance/delivery |
| release-stale | Assess stale candidate evidence and pending integration |
| release-ready | Assess current passing supplied release evidence |
| bounded-delivery | Inventory reservation: plan, combined review, implement, code review and final author handoff; skip unnecessary fixes/rechecks |
| bounded-investigation | Experiment on catalog-backed report slowness before proposing infrastructure |
| workflow-setup | Adapt an existing application's checks/docs, then prepare its actual local PR draft |
| review-ready | Review a sufficient local design/plan without manufacturing blockers |
| review-defective | Find a validation/dependency error and the document structure that hides it |
| route-local | Choose useful next work for a local inventory change, without a prescribed workflow |
| route-uncertain | Choose useful next work for an unmeasured report slowdown, without a prescribed workflow |

V1/V2 revision 2 and V4 revision 3 use restricted first-screen reading. V4 separates
next-stage acceptance from its explicit recovery question. The bounded delivery,
investigation and neutral planning probes also use this reader. Delivery revision 2
adds an unconditional status-only author handoff after review. Delivery uses a prescribed multi-role scaffold:
it tests decisions, usability, stopping and progress within that scaffold, not
independent selection/elimination of every phase. Its inventory application is
outside the navigation examples embedded in the skills. The two neutral planning
probes test the proposed next commitment, with explicit skill selection; they do
not test automatic discovery or autonomous execution of every role.


## Runner boundary

Copy only fixture/ into the worker project and selected bundles into skills/<bundle>.
Supply each requests/ file as that phase's user task. Apply an overlay's contents
at the project root immediately before its phase. Never expose case.json,
rubric.json, oracle.py or this index as worker inputs. Every executed phase starts in a fresh
agent context, sharing the working project; retain each phase reply/transcript and
workspace snapshot separately so later edits cannot erase earlier failures.

The case root rubric is evaluator-only. All required criteria need evidence and a
pass; missing/inconclusive evidence cannot pass. No word, heading or test quotas.
Only supported unchanged/no_tags/commit_count/python checks are declared. Commit
counts mean worker commits after runner initialization, not total Git history.
Unchanged checks compare the original baseline and deliberately exclude paths
legitimately replaced by overlays. Phase-specific preservation/review behavior
must be checked against phase archives by the semantic grader, not only final files.

V3's oracle checks that the private maintenance preserves runtime behavior; its
second phase plans, but does not implement, stop-on-block. Counter and V6 oracles
independently exercise default/positive inputs and invalid-input state preservation.
These stdlib assertions execute from stdin with the worker project as CWD; they do
not trust worker tests or output claims. Other cases use preservation plus semantic
criteria; document verdicts are not inferred by matching words in reports.

V3 revision 2 protects each supplied history file against modification/deletion,
while permitting new evidence records. The original directory-equality failure,
independent HPR01 finding and negative controls remain in the
[review record](../../docs/reviews/outcome-final-review.md#hpr01--history-preservation-measurement-addendum).

Initialize Git before installing each declared fixture hook as executable
.git/hooks/pre-commit. The counter baseline intentionally fails the negative-input
test; intake intentionally fails its sharp-s expectation. These are real starting
failures, not setup errors. The hook uses unittest, rejects empty discovery and
propagates failure. Workers run it again before the authorized V6 commit.

V6 review and recheck phases are separate reviewer contexts, not author self-review.
The supplied R1 identifies a baseline boolean boundary; a worker that fixes it early
must receive credit when the reviewer verifies that fact. User acceptance arrives
only before phase 06 and is explicitly synthetic. Final commit count alone cannot
prove that no earlier commit occurred: inspect each archived phase's Git identity.

Release status tables define literal HEAD as the assessment-time local git HEAD;
workers must resolve it for their report. HEAD~1 marks the preceding
candidate in the supplied table; it need not resolve in a single-commit fixture.
Report that local limitation without inventing a historical hash.
No {{HEAD}}/{{PARENT}} substitution, trusted environment variable, parent commit,
remote, build download or real release is needed. Synthetic bundle/fixture/grader/
settings identities in these tables are facts within the release scenario; they
are not hashes of the actual evaluation run, which the runner records separately.

Runtime commands and the evaluator are maintained [one level up](../README.md). See the [current result index](../../docs/validation/canary/INDEX.md) for executed checks and limits. Asset-author scratch checks are not substituted for retained runner evidence. See the current result index for actual behavior/calibration status.
