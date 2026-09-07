# Implementation plan

Status: original S1–S3 completed and preserved. C1/C2 are implemented, fast-verified and independently reviewed; heavy acceptance is deferred until release. Next action: feature PR delivery. Review policy: authorized autonomous work with independent-agent review; human review is not claimed.
Requirements: [SPEC](SPEC.md). Design: [DESIGN](DESIGN.md).

## Current increment

| Stage | Observable outcome | Dependency / boundary | Acceptance / state |
|---|---|---|---|
| C1 | Repeatable fixtures, grading, original records and release safeguard | Freeze old bundles before C2; runner and fixtures are one usable unit | Implemented; fast gate and independent recheck passed; heavy suite pending |
| C2 | Four skills guide proportionate plans and inspectable review closure | C1 supplies the future regression contract; no extra skills/framework | Implemented; portability/fast checks and static review passed; behavior evaluation deferred to release |

Delivery may combine C1/C2 in one reviewed feature PR. Commit/review policy: [DEVNOTES](../DEVNOTES.md). [Proposal](proposals/workflow-proposal.md) · [Current evidence](validation/canary/INDEX.md). The table owns outcomes/dependencies; implementation and tests own the detailed changes.

## Stages at a glance

| Stage | Observable result | Acceptance | Commit boundary |
|---|---|---|---|
| S1 | Four portable bundles, design and a runnable commit gate | Design/plan review; checker regressions; dependencies, hooks, Ruff and coverage all available | Add workflow skills, rationale and their working validation gate |
| S2 | Checks and templates behave correctly in isolated projects | Packaging regressions, Ruff, test/coverage hook trials, independent fresh-agent scenarios | Validate skills and fix observed workflow gaps |
| S3 | Usable repository entry documents and remote delivery | Documentation links, complete local gate, final independent review, push verification | Finalize usage and validation evidence |

## Execution details

S1 includes each SKILL.md, ten operation prompts, owned templates, local-discovery symlinks, and requirements/design/justification documents. Before its first commit, also deliver tools/check.py, meaningful checker tests, requirements-dev.txt, pyproject.toml, pre-commit configuration, and developer setup instructions; install their environment and run the complete gate. Zero tests fail that gate. The first two skill entrypoints were bootstrapped to make self-use possible; this fact is not retroactively described as an independent design process.

S2 uses the skills on this repository and isolated fixtures. Keep reviewers' inputs separate from expected results. Preserve actual findings before fixes and record the follow-up. Commit only coherent complete bundles, not empty scaffold directories. If a stage is already combined with another in a coherent initial commit, record that actual boundary rather than inventing earlier commits.

Required S2 cases: independently copied bundles; baseline/compatibility intake; a code stage with pending human review; copied Python hooks rejecting failures/no tests and an unchanged failing test when only a different passing test is staged; a documentation-only commit and passing control. For R6, run version/notes preparation and delivery fixtures with pending/failed PR checks, changed merged content, and verified merged content. Only the valid case may identify a tag-ready candidate, and no trial may imply an actual remote release.

S3 keeps README focused on using skills and DEVNOTES on maintaining them. CHANGELOG records delivered capabilities. Version starts at 0.1.0 as an unreleased library baseline; no tag or release is requested. An empty remote may receive the initial main commit directly; no artificial empty-base PR is needed.

## Commit gate and evidence

Use `.venv/bin/pre-commit run --all-files` after staging the intended files. The gate validates bundles and runs the full repository test suite with coverage plus Ruff. Tests and relevant reviews must apply to final content. Record raw command evidence separately and summarize actual results in VALIDATION; do not label a missing human review completed.

## Progress

- S1: complete locally. Design/plan findings resolved; four bundles and the working validation gate are implemented.
- S2: complete locally. Copied-bundle tests, real hook trials and fresh-agent behavior trials ran. Intake presentation and checker/evidence defects were fixed; targeted implementation reviews are complete with all material findings resolved.
- S3: complete. Initial commit `0ac5b7b` was pushed to main and its [GitHub CI](https://github.com/tkua2046/coding-agent-skills/actions/runs/34085252696) passed. Original commit-time checks and remote verification are retained in [VALIDATION](VALIDATION.md).

Actual commit boundary: S1/S2 and the S3 entry documents are combined into one coherent initial library commit so the first delivered tree includes usable skills, checks, reviewed design and the original validation evidence. This subsequent documentation commit records observed remote verification; it does not change the reviewed skills or checker. Earlier stages did not produce separate commits. Git history records the actual delivery; these stage names do not imply additional commits or PRs.
