# Delivery record contract and adaptable example

This record owns current execution/review state and the next action. Reuse the existing plan/handoff section; a separate file is useful only when it improves resumption. Design/spec own decision status and behavior; independent reviews own their findings. PR descriptions may summarize validation for an identified revision without becoming a second live record.

Keep one current-state block with evidence links. Preserve original reports and failures through existing immutable links, capturing otherwise unavailable reviewed content once. Code/tests own their detail; raw output stays in its evidence location. Reuse applicable identity/checks; do not generate manifests of prior manifests.

## Possible shape

# [Outcome] — current handoff

State: [completed work; remaining condition]. Open findings: [IDs or none].
Next: [one action]. Review policy / human acceptance: [actual status].
Candidate: [existing snapshot]. Checks and agent review: [applicable results/links and limits].
Delivery: [actual commit/action, or pending condition].

[Link original requirements, prior findings/dispositions and relevant failed/successful checks. Add a short check table only if it helps compare different results.]

## Small illustration

Notification mute is implemented and independently reviewed on the linked snapshot. Checks passed on that candidate; human acceptance is pending. No findings are open. Next: owner acceptance before the authorized commit. Link the existing review and raw checks; do not repeat their contents.

After committing, the durable delivery response can identify the resulting commit and hook outcome. Do not require the committed record to contain its own resulting hash.
