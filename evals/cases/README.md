# Versioned workflow canary cases

These ten version-1 heavy cases are synthetic inputs for the reviewed workflow
validation proposal. Heavy worker/grader runs are deferred until release. Historical
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

## Runner boundary

Copy only fixture/ into the worker project and selected bundles into skills/<bundle>.
Supply each requests/ file as that phase's user task. Apply an overlay's contents
at the project root immediately before its phase. Never expose case.json,
rubric.json, oracle.py or this index as worker inputs. Every phase starts in a fresh
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

Runtime commands and the evaluator are maintained [one level up](../README.md). See the [current result index](../../docs/validation/canary/INDEX.md) for executed checks and limits. Asset-author scratch checks are not substituted for retained runner evidence. Heavy behavior/calibration runs remain pending.
