# Draft or revise the design

Read the original requirements, clarification record, relevant code, and current design. Preserve supplied behavior; identify assumptions explicitly. If a decision that changes the contract is missing, describe the alternatives and hold that decision open.

Use a short first screen containing the goal, status, scope, main decision, consequence, and next step. Follow with a navigable outline and only the sections necessary for this change.

Cover:

- Current behavior and the proposed change; public interfaces and compatibility.
- Data/state ownership and invariants, including failure behavior.
- Important decisions as **Decision → Reason → Consequence → Example**. Explain the credible alternative and why it was not chosen when that affects assessment.
- Acceptance examples with explicit input, expected output/state, and error behavior. Derive expected values independently of the implementation.
- Validation strategy, remaining questions, and known limitations. Put exhaustive test matrices or long transcripts in a linked appendix.

For an existing repository, favor a small change using its conventions. For a new project, explain the minimal structure needed. Do not turn this into a function-by-function implementation plan or preselect an exhaustive test count.

The default document is `docs/DESIGN.md`, using the supplied design template; preserve an established location. Keep original specs and clarification notes separate. Include a tiny diagram only when it explains a meaningful interaction. Update affected decisions when revising a design, and keep historical reviews tied to their original reviewed version.

Before handing off, check that a reader can explain the goal, main choice, consequence, acceptance example, and next step from the first screen. State which facts were verified and which remain proposed.
