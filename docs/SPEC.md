# Coding workflow skills — requirements

Status: initial requirements preserved; authorized refinement below. Source: [user workflow](sources/user-workflow.md).

## At a glance

Deliver four reusable English skills that support the owner's development workflow, plus templates, configuration examples, and a short user entry point. Keep design and justification separate and readable. The repository is the source of truth; it contains no interview question bank.

| ID | Requirement | Observable acceptance |
|---|---|---|
| R1 | Clarify specs before design; support existing code | Intake preserves source text, records assumptions, inspects relevant code and runs a baseline |
| R2 | Design and plan have distinct review steps | Design explains decisions/consequences/examples; plan defines stages, dependencies and acceptance |
| R3 | Every stage has checks, review, fixes and a commit boundary | Review identifies its snapshot; changed code is rechecked; missing human review is not inferred as approval |
| R4 | Separate document audiences and locations | Root README, DEVNOTES, CHANGELOG, AGENTS; specs/design/plans/reviews in docs; logs separate |
| R5 | Reusable development checks | Python sample provides Ruff plus pytest/branch coverage, with a full-suite commit hook and correct failure propagation |
| R6 | Delivery and release are explicit operations | Version/changelog preparation, PR/CI review, merged-version verification, tag and release respect task authorization |
| R7 | Skills remain portable and concise | Each directory works after copying independently; entrypoints route to needed resources; no local absolute paths |
| R8 | Self-use and improvement have evidence | Static checks and behavioral trials are distinguished; discovered defects have changes and follow-up evidence |

## Scope and defaults

Names: feature-design, implementation-plan, stage-development, dev-workflow. Ten internal operation prompts support four user-facing entrypoints. Normal skill discovery remains enabled. Existing repository rules and explicit user instructions override template defaults.

The initial request authorizes implementation, local self-testing and adding this work to the new GitHub repository. It does not request a release or global installation. A real human review is never fabricated; autonomous prototype checks are recorded as such.

Repository documentation is English. Original user requirements retain their original language in the source record. Runtime/software dependencies are used for validation; the skills themselves are Markdown and have no required MCP connection.

## Authorized refinement

The owner approved execution of the [reviewed proposal](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/workflow-proposal.md) with “执行”. The original clarification “implementation plan不是拿自然语言把整个实现和test一个一个都说一遍” requires plans to own delivery decisions, not a duplicate implementation/test inventory. Local changes must preserve accepted work and keep current review closure easy to inspect. This is one material requirement among scope fidelity, consequential design, stage execution and evidence quality.

The [validation contract](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/workflow-validation.md) preserves the owner's request to standardize important tests, grading and original results as a safeguard for future skill changes. Its cadence is explicit: “当然太过heavy的测试也不能每次小改动都跑。在最后release之前跑就行。” Fast checks apply to normal commits/PRs; the required heavy suite and baseline comparison apply before release. Missing/inconclusive heavy results may not be reported as passing. No release or global installation was requested.

## Outcome-driven refinement

The subsequent [original authorization](sources/user-workflow.md#outcome-driven-revision-7-september-2026) requests task-appropriate workflow selection and actual canary-driven iteration now. The user will review the completed candidate afterward; autonomous implementation and independent-agent review are authorized for this increment.

Design and planning retain distinct purposes. For a local, understood and reversible change, a combined short note and review can satisfy both when useful or required. The subsequent delivery repair further permits direct implementation when the request and existing context suffice; documents and reviews are selected by actual decisions, risks and explicit policy. Significant uncertainty calls for bounded investigation, and consequential failures call for deeper analysis. Preserve meaningful tests, existing gates and real authorization in every route.

Required outcomes include readable document entrypoints, a usable next stage, low maintenance burden, review convergence, appropriate engineering effort and current evidence. [Goal-to-test coverage](../evals/GOALS.md) defines observable success/failure. Passing the suite does not by itself demonstrate lower developer effort or human readability. The [reviewed increment](https://github.com/tkua2046/coding-agent-skills/blob/a24b140ddda594bec61ae42ac272d3225892cfb5/docs/proposals/outcome-workflow.md) defines baseline comparison, iteration bounds and separate global benefit decisions.

## Delivery repair authorization

The owner approved the repair plan with “Go ahead。记得经常jump out of the box从high level观察，goal-oriented。不要陷入局部泥潭。” Source PRs must be reviewable, original evidence must remain retrievable, and tests must assess useful outcomes and effort. Historical raw output belongs in a separate archive, not repeated in the maintained source diff. Original requirements above describe the initial workflow; the authorized refinements govern current defaults. Explicitly requested reviews and repository gates still apply.
