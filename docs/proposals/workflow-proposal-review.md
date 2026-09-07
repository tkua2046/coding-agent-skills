Verdict: **ready** (static proposal review). Open material finding IDs: **none**.
Prior findings: **SC01 and SC02 adequately addressed in the validation design**; behavioral verification remains unexecuted.
Next action: present the proposal and this review for the owner's implementation decision. If authorized, implement the bounded changes and execute the declared trials and gates before claiming improvement. This verdict grants no implementation or publication authorization.

# Independent workflow proposal review

Reviewer: separate review context, with no authorship of the proposal or candidate skills in this pass. This is one bounded static review, not a review of an implemented workflow.

## Reviewed identity

Repository HEAD observed: `6573f8f422cb6528981ff43bc0d20c656096e7dc`.
The four live inputs read below match the SHA-256 identities in [the workflow-v2 snapshot manifest](evidence/workflow-v2/manifest.json). The verdict applies to those bytes, not subsequent revisions or HEAD alone.

| Reviewed input | SHA-256 |
|---|---|
| [Proposal](workflow-proposal.md) | `4a9948a9b60de201b7b1c16410c1a4ed349ac7619dc9891d1d8669373fca879f` |
| [Validation](workflow-validation.md) | `e480417f0b122a7b4a05098cab00bebdee4f5fff6d1213262e4d32509bac277a` |
| [Research](../research/workflow/RESEARCH.md) | `9eeae722198190c3241d7b6079977022a1788ec8ea5af59a5dbd6233362cbbef` |
| [Sources](../research/workflow/SOURCES.md) | `68644b3508bb7f5bece22ab95db92021afa63e6487fe50b6ac6fdb9b16e2a822` |

Snapshot manifest SHA-256: `d14f20bb6b3a6fd6e676f7745e5bc86c5a696ce37278ddf4ab5f088826919f2f`.
Prior [SC review](small-change-workflow-review.md) SHA-256: `e2c3aeeee56f8f63d442843949bed66db0416a22253a9c12c7ef6a43c9a38871`; its findings concern the separately identified v1 proposal and remain historical facts.

## Material findings

No new material issue requiring correction was found. The following assessment explains the verdict and its limits; it does not establish runtime effectiveness.

### Scope and proportionality

The proposal's workflow table covers intake, existing-code investigation, design and plan review, implementation with checks, human/agent review, recovery of context, PR preparation and release. This matches the sequence in `docs/sources/user-workflow.md` and requirements R1–R8 in `docs/SPEC.md`. The broader scope is substantive: execution records and delivery state have proposed behavior and V6 exercises them. Planning brevity is no longer the sole objective.

The deliverables identify affected existing bundles, examples, evidence and navigation updates. They expressly preserve functioning hooks and delivery behavior and limit integration edits to demonstrated inconsistencies. One initial increment is reasonable for coordinated prompt/template changes, with splitting permitted for an independent outcome. Neither four separate implementation stages nor a new framework is necessary to make this proposal reviewable.

The planning conflict is directly observable in `skills/implementation-plan/prompts/plan-implementation.md`: it requires a summary table and detailed cards while discouraging duplication. Replacing that requirement, rather than merely appending a brevity rule, is a concrete correction. The existing execution and review operations already establish snapshot identity, affected rechecks and human-review policy; the proposal appropriately builds on them instead of claiming these controls are absent.

### Maintainable artifacts and reuse

The document contract and research responsibility table distinguish preserved original requests, current behavior, design rationale, pending execution, completed history and executable details. V3 challenges both directions: a private refactor should not cause a documentation rewrite, while a changed public contract must update the affected documents. That distinction prevents brevity from becoming permission to leave living contracts stale. Separate long evidence and a compact current-state record are compatible with keeping history available.

The reuse decisions are grounded in the selected pinned originals:

- Superpowers at `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`: the planner really requires code/test snippets, its reviewer emphasizes material problems, and brainstorming combines proportional paths with a universal approval gate. Selective adaptation is justified.
- Spec Kit at `4a7341a93d944d6efe153b71da4a1adb9c2b578c`: inspected specification/plan/task templates separate concerns and support independently testable outcomes. The task template explicitly makes tests conditional on a request. This is a template-level observation, not proof that every Spec Kit operation omits tests; retaining the user's test policy is the appropriate adaptation.
- Awesome Copilot at `f38fb6cf039b835990d0f49dc161d7c2af99ef69`: the short planner and the detailed implementation-plan skill differ materially. The latter mandates exact implementation details and populated sections. Calling the former a possible adapted prompt, rather than a Codex-ready bundle, is appropriately limited.
- Historical OpenAI create-plan at `a5119697b819090e00e5d11ee1d86834d7c1043a` supports concise, implementation-agnostic planning; Cookbook ExecPlans at `a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7` supports observable milestones and recovery while imposing substantial self-containment and maintenance requirements. Borrowing selected principles is supported by their actual text.

These comparisons justify adapting the four existing skills. They do not prove that no alternative package could work, and the proposal does not make that broader claim.

The external guidance also supports the distinctions attributed to it: document purpose and evolving design in [Google's documentation chapter](https://abseil.io/resources/swe-book/html/ch10.html) and [GitLab's workflow](https://handbook.gitlab.com/handbook/engineering/architecture/workflow/); proportional planning in [OpenAI's harness account](https://openai.com/index/harness-engineering/) and [Claude Code guidance](https://code.claude.com/docs/en/best-practices); incremental handoffs in [Anthropic's experiments](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). The contrasting maintenance models are supported by [Böckeler's account](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) and [SPDD](https://martinfowler.com/articles/structured-prompt-driven/). Material review and coherent changes are supported by [Google's review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) and [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html). None establishes a measured benefit for these proposed skill changes; the research correctly labels its synthesis and evidence limits.

### Behavioral validation and truthful claims

V1–V3 can expose rebuilding instead of reuse, discarded scope, excessive document synchronization and stale contracts. V4 supplies a real preservation/retry hazard. V5 supplies an incomplete fix. V6 requires actual failing/passing execution, affected recheck, a fresh context, pending acceptance and eventual authorized local delivery. These are meaningful failure opportunities, not checks of preferred headings or test counts.

The evaluator/worker separation, predeclared contracts, versioned evidence, retained failures and affected-case reruns are sufficient requirements at proposal level. Concrete fixtures and evaluator rubrics still need to be prepared before execution; demanding exact test code, transaction technology or every worker step now would undermine the intended proportionality. V6's boundary-case review must be evidenced under the declared independence rules, rather than inferred from the scenario's narrative.

The paired trial is explicitly a sanity check. Timing and churn cannot establish general speedups. Scripted fixture acceptance is explicitly distinguished from actual owner approval. Local gates, review, human acceptance and remote delivery remain separate states. No future tests are represented as completed.

The trial suite does not demonstrate remote CI, merge, tagging or publication. That is an explicit and acceptable boundary because those operations are retained, not redesigned, and V6 limits itself to local commit and reviewable PR text. Any later claim of successful remote delivery still needs its own evidence.

## Prior finding dispositions

### SC01 — adequately addressed at proposal level

- Original consequence: a short larger-change plan could omit migration recovery and still pass the permissive control.
- Reviewed correction: `workflow-validation.md:18` (V4) requires preservation of usable v1 data, validated activation, retry without loss/duplication, dependencies and a decisive interrupted-migration/retry case. Omission explicitly fails regardless of length.
- Verification performed: compared V4 against SC01's minimal remedy and evaluator-only requirement in the prior review; checked validation lines 9–11 and 28–30 for separation and failure disposition.
- Disposition: the validation-design blocker is resolved for the reviewed v2 identity. Future execution must still show that an output omitting the hazard fails. No runtime closure is claimed.

### SC02 — adequately addressed at proposal level

- Original consequence: supplying only a correct fix could let superficial status changes masquerade as meaningful recheck.
- Reviewed correction: `workflow-validation.md:19` (V5) first preserves heading while still incorrectly advancing position, then supplies a corrected document. It requires unresolved R1 and withheld readiness first, followed by full-invariant verification at an identified revision with original history preserved.
- Verification performed: compared this two-revision sequence and required outcomes against SC02, including the prohibition on runtime or human-approval claims from static review.
- Disposition: the validation-design blocker is resolved for the reviewed v2 identity. The incomplete/corrected sequence remains an unexecuted behavioral trial, not evidence that revised skills already converge correctly.

## Actual inspection and limitations

Read AGENTS, DEVNOTES, original workflow requirements, SPEC, all four skill entrypoints, design/plan/stage review operations and review template, planning and stage-execution guidance, stage record and document-ownership reference. Read the four proposal/research inputs, snapshot manifest, prior proposal/review, and the selected pinned original files discussed above, including the Superpowers requesting-review prompt and relevant Spec Kit philosophy passages. Spot-checked the cited web publications for the material research assertions above.

Identity checks were limited to binding this review's inputs. No duplicate archive/link audit or unchanged-product-file audit was performed. The historical create-plan removal/current-main inventory was not independently reconstructed; this review verified the archived planning content and the proposal's explicit historical-only use. Tooling references W10–W13 and the historical count of 32 tests were not independently revalidated. Neither those counts nor private Rover observations are used here as proof of skill quality.

During this review, the author reported that all 21 archived source files match their SHA-256 and Git blob identities, the four document snapshots match, `tools/check.py` passes, and tracked repository files remain identical to HEAD. These are author-supplied mechanical results, not checks performed by this reviewer. The author also reported that five live Rover documents now differ from the initial private audit snapshot, with no changes to this review's inputs. Accordingly, the proposal/research's Rover account is treated solely as a historical observation at the preserved initial snapshot, not verified current live state. No private documents were inspected or re-audited, and the verdict does not depend on their present contents.

Only this report was written. No skills, tools, configuration or private interview documents were changed; no installation, behavioral trial, runtime test, repository gate, commit, push or release was performed. The author's mechanical checks and future implementation evidence remain separate from this verdict.
