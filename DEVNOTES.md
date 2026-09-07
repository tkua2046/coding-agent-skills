# Developer notes

User entrypoint: [README](README.md). Decisions: [design](docs/DESIGN.md). Current outcomes: [plan](docs/IMPLEMENTATION_PLAN.md).

## Setup and normal checks

Use Python 3.12 and uv; preserve an existing environment.

```sh
uv venv --python python3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/pre-commit install --install-hooks
```

Stage intended files, then run the complete fast gate before committing:

```sh
.venv/bin/pre-commit run --all-files
```

Inspect and restage formatter changes. The commit hook also runs the gate. It includes bundle/document checks, Ruff, case validation and repository tests with tool coverage; no LLM calls. Coverage describes tooling, not skill quality. Use focused tests during a repair; do not rerun an identical suite separately when the gate already establishes the result.

## Ownership and evidence

`skills/` is canonical; `.agents/skills/` provides relative discovery links. Each skill must work when copied independently. README owns user instructions, this file owns contributor operations, CHANGELOG owns significant changes, and AGENTS owns repository constraints.

Retain original requirements, sources and findings. Preserve prior reviewed content through existing immutable Git links; capture otherwise unavailable content once. Raw evaluation records are not maintained source files. New runs and manual hook trials write into ignored `artifacts/`; never force-add them to the source branch. Before delivery, preserve cited runs and their dependencies, including failed attempts, in a separate evidence tree and commit the immutable links in [EVIDENCE](docs/EVIDENCE.md). A local ignored directory is working storage, not a delivered archive.

The [historical archive](docs/EVIDENCE.md#before-the-delivery-repair) keeps original bytes and path relationships. Ordinary tests work offline using their declared local fixtures. Fetch an archive only for historical inspection or a check that explicitly requires it. Keep the complete run collection together: deleting failed attempts or restoring only selected passes invalidates a release assessment.

## Choose tests by the changed behavior

Start from the [user-visible goals](evals/GOALS.md). Select affected responsibilities and contrasting cases that protect neighboring behavior. A shared-contract change requires coverage across its affected consumers, not automatically every smoke case. Unchanged known-good paths do not need fresh expensive trials merely because a report or source link changed.

Use the [existing runner](evals/README.md) for isolated LLM tests. Preserve exact inputs, settings, raw output, failures and judgments. Small operation tests find responsibility defects; complete tasks test interactions and effort. For this delivery repair, compare with `a24b140ddda594bec61ae42ac272d3225892cfb5`; the release suite's baseline remains separately configured. A changed engine invalidates old compatible-run claims even when storage is the only change.

At a completed outcome, inspect whether the result still serves the original goal and whether the proposed next work has a concrete benefit. Record decisions in the existing plan/result page; do not create another report or round for this checkpoint. A passing test is evidence about its scope, not overall acceptance. Investigate material failures and rerun affected cases after a supported correction; keep infrastructure failures inconclusive.

Before release, run the full required heavy suite and `tools.canary release-gate` as documented in [evals](evals/README.md). The final candidate needs current passing evidence and a comparable baseline. Missing/stale/failed/inconclusive results block release, not normal PR review. Explicit task scope can authorize earlier complete trials.

The optional slower real hook exercise is `.venv/bin/python -m tests.manual.hook_trials`. Synthetic case inputs and licensed source archives retain original bytes; formatters exclude them. Their intended defects are not housekeeping tasks.

## Final PR acceptance

Inspect the whole intended diff after hook edits. Check user-visible behavior, scope, complexity, document usefulness, evidence access and clean-checkout usage. Reject unnecessary generated output or workflow machinery even if checks pass. Existing artifact conventions may legitimately include generated deliverables; assess purpose, not a universal file-count threshold.

Independent reviewers inspect stable content and actual outputs without a preferred verdict. Distinguish author fixes, verified fixes and human acceptance. Publish only the intended feature/evidence branches within authorization; retain current main until an authorized merge. Update the PR around its final behavior and observed validation.

## Version and release

`VERSION` is the single version source. Significant completed changes accumulate under Unreleased; ordinary commits do not bump versions. An authorized release updates version/notes, verifies the merged candidate and required checks/reviews, then tags/publishes that revision. This repository does not itself enforce remote branch protection or authorize a release.
