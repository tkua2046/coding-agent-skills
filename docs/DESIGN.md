# Design: four portable workflow skills

Status: original design retained; authorized workflow refinement and canary added below. Original validation and current limitations: [validation](VALIDATION.md). Requirements: [SPEC](SPEC.md).

## At a glance

Four self-contained skill folders expose ten focused operations. A user chooses the next operation; prompts and templates load only when relevant. Reviewers examine a fixed version, while the executing agent owns fixes. Human documentation stays separate from agent instructions and raw evidence.

Main consequence: copying one skill must be sufficient; no runtime resource may point outside its folder. The tradeoff is a few short repeated operational principles, without duplicating full manuals.

Outline: [Structure](#structure) · [Execution](#execution-and-review) · [Documents](#documents) · [Verification](#verification).

## Structure

- `skills/<name>/SKILL.md`: discovery metadata, scope, and operation routing.
- Each skill's `prompts/`, `assets/`, and optional `references/`: only its required resources.
- `.agents/skills/<name>`: relative symlinks to canonical skill directories for use in this repository. Independent folder copies are also supported.
- `tools/check.py` and `tests/`: packaging checks and regression tests for validation behavior.
- `tools/evidence.py`: exclusively creates a separate report for each trial, including failures.
- Root README/DEVNOTES/CHANGELOG/AGENTS: distinct audiences. Detailed architecture and evidence references live under docs.

Installation is a normal directory copy into a supported skill location. Do not add an installer that silently overwrites existing skills. No global installation occurs as part of creating the repository.

## Execution and review

Intake records relevant existing behavior and baseline before design. Design review evaluates the behavioral contract and tradeoffs. Plan review evaluates dependencies and stage boundaries. Stage review evaluates actual code and tests, independently of the author's summary.

Stage state follows planned → implementing → reviewing → fixing → verified → committed. Fixed content, test evidence and review findings must agree. A baseline commit alone is insufficient when there are uncommitted or new files. Review findings include the trigger, consequence, proposed correction and verification, plus disposition.

Default stage collaboration expects human and agent review. A user-requested autonomous run may use an explicitly recorded agent-only review policy; this does not count as human approval. Already authorized work proceeds without repeated permission questions; a template does not authorize an external action by itself.

## Documents

README describes what users receive and how to invoke it. DEVNOTES describes development commands, hooks and maintenance. CHANGELOG describes completed significant changes. AGENTS gives working constraints and command/navigation entrypoints. Specs, designs, plans and immutable historical reviews remain in docs. Full command logs remain separate from readable guides.

Each design/plan starts with the result and next action; longer files have a navigable outline. Use Decision → Reason → Consequence → Example for important choices. Keep examples concrete; do not require a particular test count or duplicate a complete specification in multiple documents.

## Verification

The first commit includes the checker, meaningful regression tests, pinned dependencies and runnable hooks along with the bundles. Validate frontmatter, resource links (including template assets) and independently copied skill folders. Parse Markdown links and references while ignoring code examples; reject local machine paths. Exercise the checker against broken bundles. Link validation covers Markdown links/images, not arbitrary paths mentioned in prose, shell commands or raw HTML.

Validate the Python sample in a temporary Git repository: successful tests pass; failures/no tests fail; Ruff fixes require review/restaging. To prove full-suite execution, leave a failing test unchanged while staging a different passing test, then observe the hook fail. Also check a documentation-only commit and a passing control. Coverage measures the configured implementation, including relevant subprocesses, and is not a score for prompt quality.

Delivery trials cover version/notes preparation, pending or failed CI/review, a merged revision different from the previously tested candidate, and a verified merged candidate. Incomplete or mismatched evidence must prevent tagging; a valid dry-run must identify the exact candidate and authorized next operation. These controlled trials do not publish a real release.

Fresh agents receive realistic tasks plus only necessary artifacts. They may write temporary trial outputs, but must not change the bundle being evaluated. Record exact tested file hashes and actual outcomes. Fix demonstrated defects, then rerun affected checks. Details and tradeoffs: [JUSTIFICATION](JUSTIFICATION.md).

## Refinement: proportional documents and repeatable evidence

Amend affected decisions/pending stages for local extensions; retain original requirements and completed work. Plans own observable increments, dependencies and decisive acceptance. Implementation/test inventories stay with code. Reviews retain stable findings and round identities; author fix claims remain distinct from verified closure. Handoffs expose current state and next action before historical evidence.

Ten versioned [canary cases](../evals/cases/README.md) cover the declared behaviors. The worker sees a disposable Git fixture and selected immutable skill bundles; evaluator criteria/oracles are outside the worker's tool read boundary. Each phase uses a fresh context. A separate grader assesses archived artifacts against an anchored rubric after calibration. Runtime probes fail closed when isolation is unavailable. Records preserve raw phase output and failed attempts; the release gate recomputes acceptance from evidence associated with the candidate and matching baseline.

Fast mechanical controls run at commit/PR time. The full heavy suite is deferred until release; its absence blocks release rather than ordinary PR work. Evidence identity includes case files, selected bundles, grader/engine, model settings and environment. The implementation is a local runner and review procedure, not a universal workflow state machine or server-enforced publishing lock. See [operation and limitations](../evals/README.md).
