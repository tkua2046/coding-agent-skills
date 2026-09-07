# Continuation test inputs

- `candidate-1/` preserves the first repaired skill bytes before new behavior results.
- `candidate-2/` preserves the reviewed setup scope/evidence correction; the first three skill bundles are unchanged. Fresh runs retain the corrected review/setup case inputs themselves.
- `candidate-3/` preserves the next-stage consistency and positive/negative evidence corrections. Already-initialized trials retain their copied predecessor bundles; subsequent trials identify this version separately. Canonical run inputs, rather than the live tree, establish which version an attempt used.
- `candidate-4/` preserves the reviewed stage evidence/status ownership correction.
- `candidate-5/` adds concrete pre-edit baseline observation to the setup operation.
- `candidate-6/` adds the reviewed author-side comparison step: retain observed results and meaningful differences, reference the existing unchanged candidate.
- `candidate-7/` makes the owning handoff opening expose actual state/next action ahead of policy/history, with one current block and a silent check.
- `setup-baseline-draft-1/` retains the pre-correction smoke draft, recovered and verified against every hash in its original no-model controls. The corrected promoted case is in `evals/cases/smoke-setup-baseline`.
- `evaluation-1/` preserves engine `2a888d…`, grader `0addfd…` and prospective case inputs, including both transfer tasks, with per-file hashes. Source files are inside its verified ZIP.
- Canonical run folders under `../canary/` retain their own complete inputs, actual model executions, outputs, environment, grades and evidence hashes. They are the result authority.

The preceding candidate is Git commit `d76bb80fa15a01e8240a9c328a0bac485b95564b`. Fresh paired trials use identical current case, runner, grader, model settings and environment with only selected skill bytes changed. A case/rubric correction alone does not establish a skill improvement. Limited transfer tasks were authored before candidate completion and withheld from the skill writer; after any repair based on their result, they become regression cases.

Engine `14b11e…` was announced before a final evidence-classification correction. The first calibration on it was interrupted and retained; it cannot qualify the current engine. See the [attempt disposition](../../reviews/continuation-dispositions.md).
