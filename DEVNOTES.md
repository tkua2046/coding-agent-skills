# Developer notes

For contributors changing the skill bundles or checks. Users should start at [README](README.md).

## Setup and check

Use Python 3.12 and uv. From the repository root:

```sh
uv venv --python python3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/pre-commit install --install-hooks
```

Preserve an existing `.venv`; do not recreate it unnecessarily. The first hook installation downloads its isolated dependencies. In each checkout, install hooks locally.

```sh
.venv/bin/python tools/check.py
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/python -m pytest
```

Before a commit, stage the intended files and run `.venv/bin/pre-commit run --all-files`. Hooks also run at commit. Inspect/restage any automatic edits. The full test gate includes documentation commits. Pytest reports missing lines/branches for `tools`, not prompt quality; no coverage percentage threshold is imposed.

## Structure and document ownership

`skills/` is canonical. `.agents/skills/` contains only relative discovery links. Each copied bundle must have no external runtime-resource dependency. Maintain metadata and invocation defaults together.

Root README owns usage, this guide owns contributor operations, CHANGELOG owns significant completed changes, and AGENTS owns agent rules. Detailed [document ownership](skills/dev-workflow/references/documents.md) is part of the dev-workflow skill.

## Design, tests and evidence

[Requirements](docs/SPEC.md) · [Design](docs/DESIGN.md) · [Justification](docs/JUSTIFICATION.md) · [Stage plan](docs/IMPLEMENTATION_PLAN.md) · [Validation](docs/VALIDATION.md)

Repository tests check bundle portability, metadata/resource failures and checker exit behavior. Fresh-agent behavioral trials use separate temporary workspaces; they never modify the bundle being evaluated. Record tested hashes, real outcomes, original findings and follow-up fixes. Keep full local command logs in ignored `artifacts/`; durable review reports and selected scenario outputs live under docs.

Run `.venv/bin/python -m tests.manual.hook_trials` for the slower isolated Git/hook exercise. Each invocation writes its own commands/results to a unique, exclusively created JSON file under `docs/validation/hook-trials/`, including failed runs. The original `hook-trials.json` is a retained historical run. This explicit trial is outside the fast commit-time test suite. Immutable validation archives are excluded from whitespace/newline fixers; preserve their bytes and fingerprints.

## Version and release

`VERSION` is the only library version source. Completed significant changes accumulate under Unreleased. A release request chooses the next version based on compatibility; update VERSION and notes together for review. Ordinary commits do not bump versions.

Merge the reviewed change, verify the final commit, tag that commit, validate any distributed bundle and publish within the authorized release scope. Creating this initial repository does not itself create a tag or release.
