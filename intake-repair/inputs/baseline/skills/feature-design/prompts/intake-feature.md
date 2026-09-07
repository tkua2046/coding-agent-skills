# Intake a feature

Inputs: original specifications, target project, known decisions, and any time budget. The useful outcome is the next justified decision, not a completed intake template. Infer missing routine details from the repository; ask only when the answer materially changes behavior, compatibility, scope, or architecture.

1. Read the target repository's instructions and user/developer entry documents. Locate relevant entry points, state, public interfaces, tests, and development commands. In a new project, state that there is no existing baseline.
2. Run the relevant existing checks when practical. Record command, exit status, and actual output location. Distinguish pre-existing failures from regressions; neither silence failures nor call an incomplete baseline green.
3. Identify what the feature changes and what must remain compatible. Do not inventory unrelated subsystems.
4. Separate clarification candidates into decisions that require the user's answer and reversible implementation defaults. Give an example showing why each important answer matters. The user may ask an interviewer or stakeholder; do not contact anyone yourself.
5. Record confirmed answers and proposed defaults separately. Preserve original requirements with a source locator; add an addendum rather than replacing original text with a summary.

Output a short intake note: current behavior, relevant files, baseline, proposed behavioral change, examples, and outstanding decisions. Adapt the [spec addendum](../assets/spec-addendum.template.md) when useful. Link raw stdout/stderr and diagnostic probes from existing execution records or an evidence file; do not embed them in the main note. Respect output-file restrictions and never invent durable evidence.

When an unknown could change the approach, isolate the question and obtain the smallest useful evidence: reproduce the behavior, inspect a caller, or run an authorized experiment. State what the observation establishes and what remains unknown. Once answered, proceed within the requested scope; do not turn an investigation into an architecture proposal by default.

Use requirement IDs only when they help connect acceptance to later stages. Stop before design or implementation unless those steps were also requested. If an essential answer is pending, continue independent inspection but do not resolve the dependent decision by timeout or silence.

After writing the note, load the Intake section of [artifact checks](../references/artifact-checks.md). Correct supported issues; expose unresolved material decisions. Otherwise the check is silent, without an additional report or review round.
