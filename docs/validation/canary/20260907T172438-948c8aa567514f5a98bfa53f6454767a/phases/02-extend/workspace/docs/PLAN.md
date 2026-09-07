# Plan
Next: resolve the YAML contract questions, then S1: validated YAML startup and fixed
occupied-cell navigation at about 200,000 cells. Status: planned, not executed;
design and plan reviews remain pending. The [current spec](SPEC.md) owns confirmed
behavior; the [revised design](DESIGN.md) owns proposals, rationale and acceptance.
This document phase performs no implementation, dependency installation or commits.

| Stage | Outcome and scope | Dependencies / risk | Acceptance and boundary |
| --- | --- | --- | --- |
| S1 — pending, revised | Load pose and occupancy once from YAML, validate completely before commands, retain an immutable lookup, and provide blocked F outcomes with continued processing and unchanged turns. Preserve two-argument `run`. Deliver loader/navigation behavior, focused tests, README usage and DEVNOTES dependency/measurement instructions together. | Builds on S0/D1. Resolve the design's dependency rule, value/schema, duplicate/start and YAML-language contracts before dependent implementation. Confirm invocation/lifetime; obtain resource limits for any numeric performance claim. Risks: late validation allowing movement, parser coercion/duplicate overwrite, excess parse-time memory, repeated copying or lookup scans, and compatibility regressions. | Meet the design's startup, movement, ownership and compatibility examples. Run full unittest discovery plus a documented 200,000-cell load/query measurement. Record environment and peak/retained memory separately. One coherent implementation/tests/usage boundary is proposed for a later authorized phase; no commit is authorized now. |

The single revised stage keeps invalid-startup rejection and movement integration
in the same deliverable; a loader-only result would not establish the required
before-movement boundary. Within S1, settle parser/schema choices first, then
implement complete validation and reusable state, integrate occupancy checks, and
verify end-to-end behavior and scale. Independent movement work can follow the
confirmed blocked-F contract, but open input decisions must not be silently chosen.
Do not add a parser dependency until the standard-library-only conflict is resolved.

Use the [development check instructions](../DEVNOTES.md): implement and test, run
full unittest discovery, review the resulting snapshot against S1, fix findings
and rerun affected checks. No independent reviewer or human approval gate is
specified. This phase has not performed a formal design, plan, or implementation
review; all remain pending. Record actual checks, reviewed snapshot identity and
findings before marking the stage complete. Commit boundaries here are proposals
only; no installation, remote action or publication is authorized by this plan.

Existing check: `"$CANARY_PYTHON" -B -m unittest discover -s tests -v` in this
fixture, corresponding to DEVNOTES' unittest command. New YAML/occupancy tests and
the scale measurement are proposed, not existing commands or passing results.
Measure one load followed by repeated hit/miss queries; verify no reads/parsing or
lookup rebuilding during movement. Exercise a malformed last cell with a command
iterator that must remain untouched. If observed resource use is unsuitable,
revisit the design with measurements before adding streaming or compact storage.

Done means confirmed YAML contracts and old navigation behavior are verified,
startup failures are clear and precede all commands, lookup is retained once,
scale results and any unresolved budget limitation are explicit, implemented usage
and operations are documented, and snapshot review has no unresolved findings.
Do not claim performance acceptance against an unspecified budget.
[Fresh baseline evidence](evidence/yaml-baseline.md) and the preserved
[earlier baseline](evidence/occupied-baseline.md) are not S1 completion evidence.

## Completed history (preserved)
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

The original [S0 acceptance record](history/completed.md) remains historical and
does not cover occupied cells or YAML startup.
