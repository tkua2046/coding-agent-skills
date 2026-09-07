# Delivery record contract and adaptable example

Use a durable record when required or useful for resumption; a completion response suffices for a local change otherwise. Reuse the existing plan/handoff section to own current execution/review state and next action. Design/spec own decisions and behavior; reviews own their findings. PR descriptions may summarize validation for an identified revision.

Make the current outcome, remaining conditions and next action easy to find before historical detail. Link relevant original reports and failures through existing immutable references, capturing otherwise unavailable reviewed content once. Keep status in one place and raw output at its evidence source, with retention scoped to this work and repository policy. Omit fields that do not help the handoff.

## Possible shape

# [Outcome] — current handoff

State: [completed work; remaining condition]. Open findings: [IDs or none].
Next: [action or complete]. Required review / approval: [actual status, if applicable].
Candidate: [existing revision reference when needed]. Validation: [actual checks/review and limits].
Delivery: [actual commit/action, or pending condition].

[Link original requirements, prior findings/dispositions and relevant failed/successful checks. Add a short check table only if it helps compare different results.]

## Small illustration

Notification mute is implemented and independently reviewed on the linked revision. Checks passed; the project's required human acceptance is pending. No findings are open. Next: owner acceptance before the authorized commit. Link the existing review and raw checks.

After committing, the durable delivery response can identify the resulting commit and hook outcome. Do not require the committed record to contain its own resulting hash.
