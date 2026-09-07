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

Use the existing design for a local extension: change only affected decisions, contract examples and open questions. Preserve unrelated accepted decisions and original requirements. A separate design is useful for independently owned/lived work or a substantial new risk; an extra follow-up alone is not a reason. A private helper rename or another test normally changes neither the design nor the plan.

For example, adding occupied cells to a navigator needs an occupancy lookup choice, the blocked-move invariant, and one decisive example. If moving east into an occupied cell fails, the pose stays unchanged and the next command may still run when that is the agreed contract. Preserve the accepted movement design. If the user later requests YAML input or large collections, incorporate that genuine scope and discuss validation/lookup consequences without prescribing unnecessary machinery.

Scale up for consequential risks. A persisted-data migration needs validation before activation, preservation of the usable original after interruption, and safe retry. Include an interrupted-run/retry example; brevity does not justify omitting these decisions. Research an uncertain external API or compatibility guarantee when it can change the design; retain the source and distinguish its guarantee from your inference.

The default document is `docs/DESIGN.md`, using the supplied template; preserve an established location. Keep original specs and clarification notes separate. Include a tiny diagram only when it explains a meaningful interaction. Keep historical reviews tied to their original reviewed version. Do not reopen unaffected decisions or re-review the whole document for a local amendment.

Before handing off, check that a reader can explain the goal, main choice, consequence, acceptance example, and next step from the first screen. State which facts were verified and which remain proposed.
