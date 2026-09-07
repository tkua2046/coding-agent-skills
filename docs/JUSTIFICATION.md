# Why this design

Status: implementation rationale. Related: [requirements](SPEC.md), [design](DESIGN.md).

## Decision summary

| Decision | Why | Consequence and example |
|---|---|---|
| Four skills, ten internal prompts | Match four user activities without making discovery a ten-command checklist | Design drafting and design review share context rules but have separate instructions |
| Self-contained bundles | A user may install only one skill | Copying stage-development must retain its stage/review templates; no cross-skill relative dependency |
| On-demand references | Users complained about large mixed documents | A design request loads design material, not release instructions or an interview manual |
| Shared artifact contract for author and reviewer | Different implicit expectations create unnecessary rewriting | Both assess the same decisions, consequences and examples; templates remain adaptable |
| Silent checks after generation | Catch a concrete reporting or consistency defect without another ceremony | A plan opening must match its first pending stage; a satisfactory artifact produces no extra checklist report |
| Small real LLM operation tests plus complete workflows | Responsibility defects need quicker feedback; interactions still need end-to-end evidence | A multi-stage plan smoke checks the next delivery, while complete migration tests retain recovery and reader checks |
| Separate design from stage plan | Reasoning and execution answer different questions | Changing a stage order need not duplicate the architectural argument |
| Fixed review content | Concurrent edits can invalidate review and test evidence | A formatter changing staged code requires inspection and fresh relevant checks |
| Human/agent review status is explicit | Agent confidence is not human approval | A stage waits for human review unless an autonomous policy was actually requested |
| Report coverage without an arbitrary threshold | Execution coverage cannot prove meaningful assertions | Inspect an uncovered error path; never label 100% coverage proof of correctness |
| Root entry documents have separate audiences | Mixed README content makes both usage and maintenance harder | Test counts go to evidence, significant behavior changes go to CHANGELOG |
| Version/release is separate from ordinary commits | Multiple commits may belong to one feature or release | Prepare one version update; tag the verified merged version, not each stage |
| Parse Markdown instead of matching link-shaped text | References and code examples have different meanings | A reference to a missing template dependency fails; the same text inside a code example does not |
| One exclusively created report per run | A passing rerun must not erase a failed attempt | Both failure and recovery remain independently inspectable |

## Alternatives and limits

A single large skill would simplify installation but make every invocation load unrelated workflow detail. Ten standalone skills would make operation boundaries explicit but increase discovery overhead and repeated context rules. Four self-contained bundles are the chosen compromise.

Cross-folder shared runtime templates would reduce duplication but break independent installation. Instead, each asset has a clear owner. Short shared review principles may be repeated; the repository documentation explains the overall contract without becoming a required runtime dependency.

A deterministic state machine or automatic PR/release bot could enforce more transitions, but would add integration, authorization and persistence complexity. This version uses prompts plus explicit evidence. It does not promise strong isolation between roles in one context; independent review requires a separate context.

Repository tests establish packaging and checking behavior. Fresh-agent exercises provide limited behavioral evidence. Neither proves all future reasoning or confirms VS Code UI discovery on every machine. Such limitations belong in [validation records](VALIDATION.md).

The Markdown parser adds one pinned development dependency. This is preferable to maintaining an incomplete regular-expression parser: an independent review demonstrated missed reference links and a real review report exposed false positives in inline code. Parsing is inert; links are never rendered or fetched. Validation is limited to Markdown links/images and local resources, not every possible dependency expressed in natural language or code.

## Workflow refinement and canary

The subsequent [outcome-driven revision](proposals/outcome-workflow.md) changes how much process a task receives. Adding another instruction to “be concise” would leave the original sequence and review incentives intact. The short route therefore permits combined design/planning and removes conflicting leaf/template prerequisites, while preserving the normal code review and actual commit gate. Investigation resolves important unknowns before architecture is expanded.

This is a hypothesis under evaluation, not a demonstrated speedup. [Goals](../evals/GOALS.md) include first-screen comprehension, plan maintenance, review restraint/convergence, meaningful runtime checks and workflow adaptation. Known faulty outputs test the scoring prompt separately. Real runs retain failures and original artifacts; the final judgment distinguishes acceptable results from reduced developer effort. High-risk migration checks prevent a superficially shorter workflow from winning by omitting necessary reasoning.

The [research](research/workflow/RESEARCH.md) supports a practical distinction: designs explain consequential choices, plans explain delivery order and acceptance, and code/tests retain implementation detail. A new test should not force synchronized prose edits. Local extensions amend affected work while preserving completed history; substantial migration risk still needs explicit preservation, activation and retry decisions.

The [approved proposal](proposals/workflow-proposal.md) applies these rules to the four existing bundles rather than adding a workflow framework. Current verdict/open IDs plus append-only recheck evidence make review closure readable without erasing failed rounds. The plan template uses one overview, with detail only where a dependency or risk needs explanation.

The [canary](../evals/README.md) standardizes previously ad hoc behavior checks. Machine oracles cover observable invariants; a separate calibrated grader covers decisions, maintainability and truthful closure. Fresh workspaces and recorded identities make a regression inspectable. The cost is explicit release-time model work and retained evidence; fast commits do not incur that cost. Passing local controls proves gate mechanics only, not prompt effectiveness.

The [continued iteration](proposals/continuation-repair.md) selects small operation tests during prompt changes and retains complete checks for workflow interactions and release. A grading result is evidence, not a replacement for the skill's goal: an automatic PASS can still contain an unsupported claim, and a FAIL can come from a contradictory fixture. Preserve both, diagnose against original requirements and actual artifacts, and version any correction. Positive capability claims and alleged defects require applicable evidence equally. This avoids teaching the skill to manufacture success, defects, headings or extra work merely to satisfy a test.

Existing frameworks informed this design but are not runtime dependencies. In particular, full executable plans and code/test recipes can suit long autonomous tasks; imposing them on every local feature would recreate the owner's maintenance problem. Licensed source files are retained with commit/hash/license metadata in the [source register](research/workflow/SOURCES.md). Articles without redistribution permission retain short excerpts and links, not reconstructed full text.

## Sources

The owner's [original workflow](sources/user-workflow.md) sets the requirements. Tool facts were checked against [official references](SOURCES.md). Interview reports and proprietary/source interview materials are outside this library's content.
