# Initial design and implementation-plan review

**Verdict: needs changes.** Resolve the commit-gate dependency and make the sample-hook and delivery/release acceptance cases explicit. The portable-folder boundary, document audiences, review-evidence principles, and authorized agent-only bootstrap policy are consistent with the requirements.

Reviewer: independent reviewer in this task, with no authoring history or supplied prior review conclusions. Date: 2026-09-06. All findings below are **P2 / pending**, ordered by implementation dependency.

## Actual scope and checks

Compared DESIGN and IMPLEMENTATION_PLAN against SPEC R1–R8 and the original workflow; consulted JUSTIFICATION as rationale, not verification evidence. Applied the feature-design and implementation-plan review prompts and the feature-design review template, plus repository AGENTS instructions. Assessed stage ordering, behavioral acceptance, review/fix boundaries, portability commitments, authorization, and reading cost.

Performed file/line inspection and SHA-256 calculation only. No implementation, check configuration, unrelated skill directories, prior reviews, or linked validation records were reviewed. No runtime tests, hook execution, or fresh-agent trials were performed. These are gaps in the documented contract/plan, not claims about defects in unseen code. Only this report was written.

## Findings

### F1 — Establish the commit gate before the first commit boundary

- **Location:** IMPLEMENTATION_PLAN lines 10–18 and 24; DESIGN lines 18 and 39.
- **Trigger / consequence:** S1 offers a commit boundary with metadata/resource validation, while S2 establishes packaging regressions and hook behavior. The mandatory gate already requires a virtual environment, pre-commit configuration, checker, full test suite, coverage, and Ruff. Their bootstrap/stage ownership is unspecified. Following the S1 boundary can therefore leave the executor unable to establish the required gate, or committing bundles before their relevant checks are available. The permission to combine stages records an eventual boundary but does not select the dependency order.
- **Minimal correction:** Assign gate setup and meaningful initial checks to S1 before its commit, or explicitly make S1+S2 the first commit boundary. Identify setup prerequisites and when the stated command becomes runnable.
- **Verification:** Trace the first intended commit from a fresh checkout: every gate prerequisite and its relevant tests must be delivered by that boundary, with an explicit no-tests failure condition.

### F2 — Prove that the sample commit hook runs the full suite

- **Location:** SPEC R5 (line 15); DESIGN line 39; IMPLEMENTATION_PLAN lines 11 and 24.
- **Trigger / consequence:** The sample trials specify passing tests, failing tests, no tests, and formatter changes, but do not distinguish a full-suite hook from one filtered to staged files. A filtered hook can pass those trials while missing an unchanged failing test when only a different passing test is staged. The repository's explicit full-suite gate does not establish the copied sample's behavior.
- **Minimal correction:** State that the sample hook runs the configured full suite independently of staged filenames. Add an isolated trial with an unchanged failing test and only a different passing test changed/staged, plus a passing control; observe the commit result through the hook.
- **Verification:** The former commit must fail because of the unchanged test, and the control must pass. Require these outcomes in S2 acceptance, rather than only successful hook invocation.

### F3 — Give the reusable PR/release workflow its own acceptance cases

- **Location:** SPEC R6 (line 16), source workflow lines 14–15; JUSTIFICATION line 17; IMPLEMENTATION_PLAN lines 11–12 and 18–20.
- **Trigger / consequence:** S3 appropriately covers this repository's initial push and unreleased version. S2 names fresh-agent scenarios without specifying a delivery/release scenario. Consequently, the stated stage acceptance could be met without exercising the reusable workflow's PR/CI review or merged-version verification. For example, a release prompt could accept a stale pre-merge snapshot without any named trial detecting it; the rationale's correct merged-version rule alone provides no behavioral evidence.
- **Minimal correction:** Map R6 to S2 scenarios covering version/changelog preparation, pending or failed PR/CI review, a changed merged revision, and a verified merged release candidate. Define expected progression/evidence under the supplied task authorization. Keep live tag/release execution outside this bootstrap's scope.
- **Verification:** Controlled fixtures or agent trials must show that incomplete CI or mismatched version evidence prevents progression to tagging, while the valid case identifies the exact merged candidate and authorized next operation.

## Reviewed input fingerprints

SHA-256 of raw file bytes; findings apply only to these versions.

| Input | SHA-256 |
|---|---|
| [DESIGN.md](../DESIGN.md) | `bf5996d7aefacbb77762615dfd0ca5fe7f71fb1177beba7b9b024cdb438fc530` |
| [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) | `2d312605b841186e19f5d3899519778aa4664d648ddf5c0f2ce2cf7a04d4d1cc` |
| [SPEC.md](../SPEC.md) | `c6ccfca7c06e6e23e59b9ce5426a98e7b37988345634e73c52317cbb7aafebf0` |
| [user-workflow.md](../sources/user-workflow.md) | `f8bd2d7207152a20d52d106b3ba6b75e08b8aaf88f28ffab285510a59ea0a0f1` |
| [JUSTIFICATION.md](../JUSTIFICATION.md) | `4bb7ae8fc5a6b1edd30830c0eb7b176d9da45ac78f77fabcaffff17e57b94a6e` |

## Next action

Revise the affected design/plan commitments to resolve F1–F3, then review the revised versions. No product or design changes were made by this reviewer; runtime correctness remains unestablished.
