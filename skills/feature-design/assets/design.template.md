# Optional design shape and example

Use this while organizing the final result if it helps. A concise paragraph can serve a local decision; adapt to existing conventions. These are prompts for useful content, not mandatory headings or fields.

- **Decision:** what changes, the chosen approach, why it fits, and its important consequence.
- **Decisive example:** an input/state and expected outcome that clarifies a meaningful boundary.
- **Needed support:** affected compatibility/state/failure behavior, a consequential tradeoff or unresolved choice. Add navigation when detail grows.
- **Sources:** existing requirements and decision/history references; link an existing plan/status only where useful.

The design owns choices and consequences, not implementation order, test-name inventories or a second live progress record. A completed decision does not require a next-action sentence. Do not copy these instructions into the user's document.

## Example

Allow a saved display preference to override the system theme; leaving it unset preserves automatic selection. One optional setting preserves existing users' behavior, at the cost of storing a value and defining reset behavior. Explicit light stays light when the system changes to dark; resetting resumes the system choice. Reject an unknown setting without replacing the previous value.

This illustrates a decision and its consequence, not a required feature or architecture.
