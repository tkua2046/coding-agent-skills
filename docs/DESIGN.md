# Design: four portable workflow skills

Current decision: keep four portable skills, with one substantive artifact contract shared by each author/reviewer operation and small actual LLM tests for individual responsibilities. Design explains consequential choices; plans own delivery boundaries; reviews own findings/dispositions; one handoff owns live execution state. This reduces competing format instructions and status synchronization. For example, a private helper rename changes code and relevant check evidence without rewriting an accepted design or plan.

Small tests identify basic decision regressions cheaply; complete canaries still test workflow interactions and correctness. Reusing existing checks saves work only when their content, inputs/environment and freshness remain applicable, and required gates still run. The [reviewed continuation](proposals/continuation-repair.md) develops these choices; [implementation plan](IMPLEMENTATION_PLAN.md) owns current delivery status. Earlier [outcome-driven decisions](proposals/outcome-workflow.md) remain the basis below.

Requirements: [SPEC](SPEC.md). [Earlier design](https://github.com/tkua2046/coding-agent-skills/blob/d76bb80fa15a01e8240a9c328a0bac485b95564b/docs/DESIGN.md) remains in Git history. Outline: [Task depth](#task-depth-and-completion) · [Structure](#structure) · [Execution](#execution-and-review) · [Documents](#documents) · [Verification](#verification).

## Task depth and completion

Select depth using material uncertainty, failure consequences/reversibility and affected boundaries. A local understood change may combine design and planning in a short note and one document review; normal code review and checks still apply. A consequential change expands relevant risk analysis. An unknown first needs a bounded evidence-gathering step. A one-sentence reason is enough; the skills do not require a classification artifact or another routing framework.

Each operation ends at a useful outcome: sufficient decisions to implement, an actionable next increment, verified resolution of material findings, or an identified pending decision. Review preferences are optional; repeated disagreement calls for evidence or a decision rather than cosmetic rounds. A time budget cannot manufacture approval. Existing user authorization and project gates remain authoritative.

The [goal map](../evals/GOALS.md) connects these decisions to actual canaries. A restricted reader tests whether document openings convey the required facts; full artifacts remain subject to correctness/usability review. Paired elapsed time and unnecessary review/document work inform a separate benefit decision. The prescribed multi-role delivery scaffold does not prove autonomous phase selection, and machine comprehension does not replace owner reading.

## Structure

Copying one skill must be sufficient; no runtime resource may point outside its folder. This requires a few short repeated contracts across bundles, without duplicating full manuals. Within each bundle, author and reviewer share one artifact contract, and load only the selected operation's resources.

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

Validate frontmatter, resource links (including template assets) and independently copied skill folders using the repository's checker, regression tests and pinned environment. Parse Markdown links and references while ignoring code examples; reject local machine paths. Exercise the checker against broken bundles. Link validation covers Markdown links/images, not arbitrary paths mentioned in prose, shell commands or raw HTML.

Validate the Python sample in a temporary Git repository: successful tests pass; failures/no tests fail; Ruff fixes require review/restaging. To prove full-suite execution, leave a failing test unchanged while staging a different passing test, then observe the hook fail. Also check a documentation-only commit and a passing control. Coverage measures the configured implementation, including relevant subprocesses, and is not a score for prompt quality.

Delivery trials cover version/notes preparation, pending or failed CI/review, a merged revision different from the previously tested candidate, and a verified merged candidate. Incomplete or mismatched evidence must prevent tagging; a valid dry-run must identify the exact candidate and authorized next operation. These controlled trials do not publish a real release.

Fresh agents receive realistic tasks plus only necessary artifacts. They may write temporary trial outputs, but must not change the bundle being evaluated. Record exact tested file hashes and actual outcomes. Fix demonstrated defects, then rerun affected checks. Details and tradeoffs: [JUSTIFICATION](JUSTIFICATION.md).

## Refinement: proportional documents and repeatable evidence

Amend affected decisions/pending stages for local extensions; retain original requirements and completed work. Plans own observable increments, dependencies and decisive acceptance. Implementation/test inventories stay with code. Reviews retain stable findings and round identities; author fix claims remain distinct from verified closure. Handoffs expose current state and next action before historical evidence.

Versioned [complete canaries and smaller operation cases](../evals/cases/README.md) cover the declared behaviors. The worker sees a disposable Git fixture and selected immutable skill bundles; evaluator criteria/oracles are outside the worker's tool read boundary. Each phase uses a fresh context. A separate grader assesses archived artifacts against an anchored rubric after calibration. Runtime probes fail closed when isolation is unavailable. Records preserve raw phase output and failed attempts; the release gate recomputes acceptance from evidence associated with the candidate and matching baseline.

Fast mechanical controls run at commit/PR time. The full heavy suite is deferred until release; its absence blocks release rather than ordinary PR work. Evidence identity includes case files, selected bundles, grader/engine, model settings and environment. The implementation is a local runner and review procedure, not a universal workflow state machine or server-enforced publishing lock. See [operation and limitations](../evals/README.md).
