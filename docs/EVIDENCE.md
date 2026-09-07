# Evidence index

Original records remain accessible separately from the maintained source tree. This page locates them; [validation](VALIDATION.md) owns the current result summary.

## Before the delivery repair

The complete original tree is retained at commit `a24b140ddda594bec61ae42ac272d3225892cfb5`, held by the published `codex/evidence-before-repair` branch. The ref was checked against the remote before any source-tree removal. Git stores identical content once; paths and original bytes remain intact, including failed and incomplete runs.

| Record | Original location |
|---|---|
| Results and limitations | [Original result index](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/validation/canary/INDEX.md) |
| Raw model runs | [Original trials](https://github.com/tkua2046/coding-agent-skills/tree/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/validation/canary) |
| Proposals and their evidence | [Original proposals](https://github.com/tkua2046/coding-agent-skills/tree/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals) |
| Review findings and follow-ups | [Original reviews](https://github.com/tkua2046/coding-agent-skills/tree/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/reviews) |
| Prior final local gate | [Original hook result](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/validation/continuation-checks/pre-commit-20260907T182959Z.json) |

Retrieve an original without restoring thousands of files into the source checkout:

```sh
git fetch origin codex/evidence-before-repair
git show a24b140ddda594bec61ae42ac272d3225892cfb5:docs/validation/canary/INDEX.md
```

For complete offline inspection, use a separate worktree at that commit. Historical results describe those exact inputs; they do not certify the repaired skills or changed runner. The retained ancestor still contributes to Git history size; this repair does not rewrite history to disguise it.

## Delivery-repair records

The complete new evidence tree is pinned at `9957cffae75f7e51f351bac2905573bbb116ae5c` on `codex/evidence-delivery-repair`. A fresh remote clone verified all 766 manifest entries against SHA-256, including original failures and the review that led to the ZIP regression. This separate branch is evidence storage, not another source PR.

| Inspect | Original record |
|---|---|
| Scope, reproduction and integrity | [Archive README](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/README.md), [manifest](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/manifest.json), [26 worker records and available usage](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/acceptance-summary.json) |
| Original requests, rubrics and frozen skills | [Original comparison inputs](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/acceptance/inputs), [independently authored transfer packet](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/transfer-packet), [final intake inputs](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/final-intake/inputs) |
| Operation failures, corrections and independent judgments | [Behavior review](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/behavior-review.md), [final timed-out invocation](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/final-intake/smoke-intake-conflict/candidate) |
| Glanceable output and actual reader | [Final investigation](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/final-intake/bounded-investigation/candidate/workspace/docs/INVESTIGATION.md), [reader response](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/final-intake/bounded-investigation/candidate/reading-probe/reply.md) |
| Complete-task originals and implementation repair | [Transfer review and verified closure](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/transfer-review.md), [original failed candidate](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/acceptance/packet-import/candidate-r2), [separate fix and rechecks](https://github.com/tkua2046/coding-agent-skills/tree/9957cffae75f7e51f351bac2905573bbb116ae5c/packet-fix) |
| Test gap found by review | [Original review bytes](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/packet-import-v2-regression/original-review.md), [both old outputs rejected](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/packet-import-v2-regression/summary.json) |
| Preservation, package and setup acceptance | [Storage review](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/storage-review.md), [package review](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/package-review.md), [fresh-export hook output](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/clean-check.json) |
| Method limits and retained gate attempt | [Transfer isolation limitation](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/transfer-isolation-disposition.md), [local gate disposition](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/final-gate-disposition.md), [original gate log](https://github.com/tkua2046/coding-agent-skills/blob/9957cffae75f7e51f351bac2905573bbb116ae5c/final-gate.log) |

Report-relative source links retain their original local context. Restore the tree under ignored `artifacts/repair/` as the archive README explains; current maintained transfer cases are [transcript search](../evals/cases/transfer-transcript-search/case.json) and [packet import](../evals/cases/transfer-packet-import/case.json). Archive records bind observations to their actual inputs; they do not certify later revisions.

## Future records

New execution records belong in ignored `artifacts/`. Before citing a run as delivered evidence, preserve its complete inputs, outputs, failed attempts and dependencies separately, then link its immutable commit here. Local scratch alone is not durable evidence. Research originals and the minimal inputs needed by ordinary regression tests stay in maintained source. Final commit checks are also visible on [PR #1](https://github.com/tkua2046/coding-agent-skills/pull/1).
