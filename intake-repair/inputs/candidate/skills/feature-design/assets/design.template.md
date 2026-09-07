# Design contract and adaptable example

Use this contract for both authoring and review. Adapt the shape below; do not copy these drafting instructions into the product document.

Design owns behavior relevant to consequential choices, boundaries, reasons, tradeoffs and examples. Original requirements own the requested contract. Code/tests own implementation details; an existing plan owns delivery order and a delivery record owns current status when needed. These responsibilities do not require separate documents.

The opening explains the current outcome, chosen approach and reason, material consequence and a decisive example before history or workflow metadata. Include a blocking decision there when it changes the next action. Link sources and decision status afterward. Detail should answer a real implementer/reviewer question, with navigation when it grows.

Explain relevant compatibility, state ownership, failure behavior and validation. Derive expected examples from requirements, independently of code. When a choice has a credible alternative, explain its consequence; avoid an alternatives catalog for an obvious local change. An abstraction or dependency needs a current requirement or observed constraint. Where failure can leave persistent or external effects, explain what remains usable, validation before activation, interruption detection and conditions for safe retry, including a failure/retry example. Extra detail is appropriate when those decisions need it.

## Possible shape

# [Feature decision]

[Outcome. Choice and reason. Benefit/cost or failure consequence. Concrete input → outcome.]

[Open decision if any; otherwise next implementation outcome or link.]

Decision: [proposed / accepted, with source]. Requirements: [original reference]. Delivery: [existing plan/handoff if useful].

[Only needed detail: current behavior, boundaries, consequential alternatives, acceptance/failure examples, validation and remaining uncertainty. Link long evidence and original reviewed versions.]

## Small illustration

Allow a saved display preference to override the system theme; leaving it unset preserves automatic selection. One optional setting avoids changing existing users, at the cost of storing a value and defining reset behavior. For example, explicit light stays light when the system changes to dark; resetting resumes the system choice. Reject an unknown setting without replacing the previous value. Next outcome: implement selection/reset with these acceptance examples in one local increment.

This illustrates a decision, consequence and next outcome, not a required feature or implementation pattern.
