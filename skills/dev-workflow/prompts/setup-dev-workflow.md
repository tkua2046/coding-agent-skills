# Inspect or adapt a development workflow

Read the request, repository instructions, relevant developer/user guides, runtime/dependency configuration, checks, CI and local Git state. Identify the requested diagnosis or change; reuse the established environment and toolchain. Repair a demonstrated gap within scope, without replacing an effective gate to match an example.

Before changing a check, reuse applicable baseline evidence or observe its output and exit condition. Keep child results identifiable: wrapper success does not establish an unchecked child's result. An unavailable or failing baseline does not block justified authorized repair, but later success establishes only the later state. For inspection, report supported state and gaps without doing unrequested repairs; probe an unchanged runner's failure behavior only when propagation remains uncertain.

Trace the active check path from configuration to the invoked runner; read other scripts or historical output only when they help explain an observed gap.

## When checks or hooks change

- Keep a usable normal check entrypoint and the project's commit policy. For changed runners, discovery, wrappers or hooks, verify meaningful collection, passing/failing execution and relevant failure propagation. Test a hook through the installed hook path; calling the runner directly does not prove hook execution.
- Preserve existing hooks and custom hook paths; verify the intended repository/worktree before installation. Match the interpreter and dependencies to the application, prewarm needed hook dependencies and exercise failing probes in isolated scratch fixtures. Keep probes out of the deliverable.
- A full-suite pre-commit hook uses `pass_filenames: false` and runs on documentation-only commits when that is the chosen policy. Propagate test failures and zero-test collection failures. If application tests are absent, report the gap and identify meaningful tests needed with implementation; do not suppress the failure or create an empty suite merely to claim setup success. Documentation-only projects do not need an invented application test suite.
- Use established lint/format/test tools. For a Python setup that needs them, the optional samples use Ruff and pytest (including unittest collection); run Ruff fixes before formatting. Adapt sample paths and include required application dependencies in an isolated hook environment, or deliberately use the project's existing environment.
- Inspect formatter changes and restage only intended files when preparing a commit. Keep disposable environments, caches and scratch reports out of version control while preserving intentional deliverables and required evidence.

## When coverage or test policy changes

Measure the actual application source/modules, including initialization and subprocess execution where relevant, with branch and missing-line reporting. Adapt the sample `app` selector; add machine reports when useful or requested. Preserve an existing coverage threshold; a report is not a reason to invent a percentage gate. Report what was measured and consequential uncovered behavior without equating coverage with test quality. Meaningful assertions and independent expected outcomes still matter.

Preserve the project's fast commit/PR and expensive integration/behavior-test cadence. Add regression coverage for demonstrated defects when it verifies the behavior; rerun affected checks and mandatory gates, reusing adequate unaffected evidence. Label deferred checks accurately. If the project maintains agent behavior, use its existing evaluation system and retain relevant versioned regressions and real outcomes; ordinary application setup does not require an agent-testing framework.

## Documents and delivery

For document creation or reorganization, apply [document ownership](../references/documents.md); adapt templates only when helpful. Preserve original content/history, update affected links and metadata, and keep one authoritative owner for each instruction.

Finish with the result, observed validation and material limits or remaining work. Make changed check commands and required environment accessible in the response or linked developer guide. For coverage, make actual measurements and consequential gaps easy to find; disclose unavailable measurement. State configured, installed and executed hook status accurately when affected. Support successes and alleged gaps with observed output or applicable inspected configuration/source; missing optional tools alone are not defects. Reuse existing evidence locations rather than creating a log or report by default.
