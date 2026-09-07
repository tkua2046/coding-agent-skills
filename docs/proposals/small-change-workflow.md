# Proposal: proportionate changes and visible review closure

Status: superseded by the broader [workflow proposal](workflow-proposal.md). Preserve this draft and its original review as history; the immutable v1 input is in `evidence/small-change/`. The earlier unreviewed skill edits have been withdrawn.

## At a glance

Keep the four existing skills. Make small add-ons update the accepted documents locally, let a coherent change use one implementation stage, and make current review status visible immediately. Preserve meaningful checks, original findings and the user's requested review steps. Validate agent behavior in isolated fixtures before claiming improvement.

Next: independent review of this proposal, then the owner's decision. No Rover files, skill behavior, installation, commit or remote state change is part of this proposal phase.

Outline: [Evidence](#observed-problem) · [Changes](#proposed-changes) · [Validation](#validation-before-delivery) · [Delivery](#implementation-and-delivery-if-approved).

## Observed problem

The Rover add-on originally asked for fixed obstacles. A later user clarification added a YAML file containing starting position, heading and a potentially large in-memory obstacle list. YAML and configurable pose are therefore real scope, not inventions by the agent.

The observed draft nevertheless replaced much of the accepted documentation: SPEC +55/-76 lines, design +82/-135, implementation plan +154/-175. Its four stages prescribe 30 new named tests and cumulative counts. A duplicate-key policy led to a custom YAML loader, followed by review of that loader's own error cases. These are reasons to examine proportionality; they do not establish that every validation rule or finding was wrong.

Review closure exists: D01 was resolved at design level, and I01/I02 were resolved in the plan. Current document hashes match the final recheck records. Those conclusions appear near the bottom, below earlier open findings. No obstacle code or tests were implemented. The recorded planning turn lasted about 17m35s, including clarification and waits, and included compaction; this is not a measurement of model-only latency or proof of an Astra defect.

Original Rover documents, accepted versions, hashes and diffs are preserved privately alongside interview preparation. They will not be imported into the public skills repository. The current skills were not installed in that Rover workspace. They already discourage fixed test counts, but their table/card templates and full-review wording can still encourage excessive work. Existing packaging tests do not establish proportionate agent behavior.

## Proposed changes

| Decision | Intended behavior | Consequence / example |
|---|---|---|
| Amend an existing design by default for a local add-on | Update affected contracts/examples; retain unaffected sections and source requirements | Obstacle blocking changes movement and CLI feedback without replacing the base command/parser design |
| Use a separate design only when useful | Separate work with an independent lifecycle, substantial alternatives or a change too large to read inline; link the base | A persistence/migration feature may need its own design; another interview question alone does not require one |
| Preserve completed implementation history | Append an add-on stage or revise affected pending stages; mark genuinely superseded work | Completed base stages stay completed; no new narrative pretending they are future commits |
| Begin with one coherent stage | Split for useful intermediate outcomes, dependencies, risk or rollback boundaries | Fixed obstacles can be one stage with code and tests; YAML integration might justify one or two, depending on actual boundaries |
| Make templates optional in depth | A small design can be a short change note; a one-stage plan can be a checklist | Do not produce both a summary table and a detailed card that repeat the same content |
| Specify behavior, not test arithmetic | Use decisive acceptance cases and reference the existing gate once | Blocked move leaves position/heading unchanged; subsequent commands still work. Do not freeze future test-method counts |
| Review changes and consequences | Reuse unaffected decisions; justify blockers against requirements or an adopted contract | A stricter config policy must justify its cost before a custom loader is prescribed |
| Surface current review state | Put verdict, reviewed revision, unresolved IDs and next action first | The reader can see that D01 is verified closed without searching the historical findings |
| Keep review evidence honest | Preserve original findings and round-specific checks; distinguish author-fixed, reviewer-verified and user-approved | A design finding can be closed in the document while runtime checks remain unperformed |
| Recheck proportionately | After a fix, recheck the finding and affected contracts; expand only for new material evidence | A wording change does not restart design review. A changed behavioral contract can require it |

These are defaults, not a mandatory classification framework. Size depends on behavioral scope, uncertainty and risk, not line counts alone. Do not force a complex feature into a short note or skip a requested review. If an explicit interview time budget is exceeded, report the remaining material decision; do not silently approve it or continue cosmetic rewrites.

For a small change, design and implementation remain separate concerns but may be short sections in existing artifacts when repository conventions allow. Existing separate files should not be merged just to adopt this proposal.

### Intended edit scope

- feature-design: SKILL.md, drafting/review prompts, design/review templates.
- implementation-plan: SKILL.md, planning/review prompts, plan template.
- README usage note and JUSTIFICATION/CHANGELOG entries documenting the change.

Prefer replacing contradictory instructions over appending another workflow manual. No new skill, MCP, framework, runtime dependency or enforced global setting is proposed. stage-development and dev-workflow remain unchanged unless review identifies a concrete conflicting instruction; any expansion must be explained before implementation.

## Validation before delivery

Do not treat metadata validation, test counts, or shorter prose alone as proof that the skills improved. Declare the behavioral criteria before evaluating the implementation.

| Scenario | What the worker receives | Acceptance evidence |
|---|---|---|
| Small obstacle add-on | Accepted base docs/code, fixed-obstacle requirement, candidate skills; planning only | Current contract is clear; unrelated sections and completed stages survive; a coherent stage includes meaningful tests; no full rewrite, arbitrary test census or code implementation |
| YAML scope extension | Confirmed config-file/starting-pose/large-list requirements | Real added requirements remain; lookup strategy and a basic invalid-input policy are explained; extra loader machinery and stage splits need concrete justification |
| Review/fix/recheck | A document with a real contract defect, original review and a proposed fix | Stable finding ID, original issue retained, author claim distinct from reviewer verification, current status visible; unresolved issues or required human review cannot be labeled approved |
| Larger-change control | A separate synthetic change with persistence/migration or a compatibility boundary | Additional design detail and stages are allowed when justified; the small-change default does not suppress necessary work |

Use temporary copies with separate author/reviewer contexts. Give workers raw requirements and the skill, not expected answers or the diagnosis above. Assess changed sections, acceptance coverage, current-review-state readability and unnecessary stages/artifacts. Retain original requests, input versions, outputs, elapsed time, findings and final dispositions. Inspect document diffs and judgment, rather than testing exact wording/headings. Timing and line counts are observations, not automatic pass/fail thresholds.

Run one representative small-add-on case against the current skills and the revised skills with the same task, environment and model/effort settings. This is a limited comparison, not a statistical claim about models or guaranteed latency. Run the other scenarios against the candidate. If a behavior fails, fix the demonstrated cause and rerun the affected scenario; do not repeat unrelated trials by default.

Also run the existing bundle/resource checks, skill-format validation and repository pre-commit/test suite. Their result establishes packaging/checker regressions only. Human-readable review evidence establishes the behavioral claims above. No test has been run against an implemented version of this proposal yet.

## Implementation and delivery if approved

One coherent implementation stage: revise the conflicting skill/template text, execute the declared trials and checks, address material review findings, and present the candidate diff with evidence. A separate independent review verifies consistency between entrypoints, prompts and templates without repeating the entire original library audit.

Then commit/push within the agreed delivery scope and verify CI. Keep original failed evidence and distinguish this new validation from bootstrap results. No release/version bump or global/Rover installation is proposed.

## Proposal review

Current proposal review is pending. Review should assess whether the scope is sufficient, whether the defaults preserve correctness and user intent, and whether the planned behavioral checks could detect the reported failure. It is a review of the proposal, not approval or runtime validation of future edits.
