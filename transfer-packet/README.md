# Frozen independent acceptance — 2026-09-07

Two fresh tasks, authored outside the repository without inspecting skill implementations or future edits. Keep this packet withheld from the skill author until the candidate freeze. `FREEZE.json` fingerprints the finalized contract. No solutions or LLM runs are included; no repository files were changed.

| Task | Goal |
| --- | --- |
| `transcript-search` | Implement an understood search/context feature in an existing transcript tool, preserving output compatibility and providing useful tests and usage guidance. |
| `packet-import` | Implement safe local ZIP import with adequate filesystem-boundary reasoning, rejection/cleanup/retry verification, and an understandable maintenance handoff. |

`route-uncertain` is the main evaluation's third, familiar task; it is not fresh transfer and has no new fixture here. The two selected focused guards are `smoke-intake-conflict` and `smoke-review-partial`. See `EXISTING_CASES.md`.

## Directory contract

```text
TASK/
  fixture/          # worker project: existing code, tests, README, AGENTS, original REQUEST
  REQUEST.md        # evaluator's original copy; feed unchanged as the user task
  accept.py         # evaluator-only deterministic behavior check
  REVIEW.md         # evaluator-only human/agent review criteria
FREEZE.json
AUTHOR_VALIDATION.json
runs/author-baseline/  # retained fixture-author checks only
```

Only copy `fixture/` into a fresh worker workspace. Add the supplied frozen skills under `skills/` and initialize the local Git repository as the existing runtime normally requires. Keep evaluator files and output outside the worker workspace; do not copy this entire packet into it. Preserve separate workspaces/evidence for prior and candidate versions and every attempt. All runtime files/output should remain under this external directory for this task's ownership boundary.

## Existing runtime settings and invocation

Use the existing `tools.canary_runtime.execute`; no new harness is required. Python 3.10+ with standard-library `unittest` is sufficient for both fixtures and checkers. Use the experiment's selected model and effort identically for prior/candidate; `timeout_seconds=900` is a practical per-invocation ceiling, not a task quality threshold. The existing runtime sets `CANARY_PYTHON`, local temporary storage, restricted reads, no network, and no interactive approvals. Run its usual isolation probe against an evaluator-only file first; a failed/unavailable capability is not a behavioral pass.

```python
from tools import canary_runtime as runtime

settings = {"model": MODEL, "effort": EFFORT, "timeout_seconds": 900}
prompt = (case / "REQUEST.md").read_text() + "\n\n" + (
    "Use the supplied skills/ as applicable to complete this task. "
    "Read fixture AGENTS.md and the existing code and instructions. "
    "CANARY_PYTHON points to the prepared Python runtime. "
    "Use only this project and supplied skills; no packages or external services."
)
result = runtime.execute(workspace, prompt, evidence / "reply.md", settings)
```

Here `case`, `workspace`, and `evidence` are absolute `Path` objects; the caller creates workspace/evidence directories first. Supply the same frozen bundle selection and neutral prompt on both sides. Do not force a design-first sequence or reveal evaluator expectations to the worker.

After execution, run the two commands from the worker workspace using the prepared Python interpreter, retaining their real stdout/stderr and exit codes:

```sh
python -B -m unittest discover -s tests -v
python -B /tmp/coding-skills-transfer-20260907/TASK/accept.py /absolute/path/to/worker
```

The second command is an evaluator process, outside the worker read sandbox. Review the original request's preservation, final diff, worker tests, transcript, actual check records, and handoff against `TASK/REVIEW.md`. The script's success alone is insufficient, especially for atomic placement and filesystem error handling. A fresh reader should be able to locate usage, the relevant decisions, actual completion/checks, and any pending work from the delivered material. No new worker deliverable is implied by the evaluator's own reporting needs.

## Acceptance interpretation

Each required criterion needs supported pass evidence; missing evidence is inconclusive. Report quality separately from improvement versus the prior skills. Compare correct delivery, effort justified by actual uncertainty/consequences, and usable documentation/handoff. No universal word, line, time, document, phase, or test-count threshold; a useful short README note is welcome. Record worker effort separately from evaluation overhead. Keep all attempts. Failure-informed reuse is regression evidence, not unseen transfer.

The fresh fixtures authorize normal autonomous local code changes, checks, and useful documentation. They impose no human-approval or independent-review prerequisite. Existing explicit human acceptance, agent review, and gates elsewhere remain valid; self-review cannot substitute for independent review. Missing capabilities/evidence must remain pending, never waived or claimed passed. No task permits publishing.

`AUTHOR_VALIDATION.json` records that original tests pass and both unfinished baselines are rejected for the intended missing behavior. These are fixture checks, not skill evaluations or full positive-path oracle validation. Development-time convenience scripts were removed in favor of the existing runtime and direct unittest/check commands. Freeze corrections need an explicit new contract version, rationale, and compatible prior/candidate reruns.
