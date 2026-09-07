# Plan

Status: occupied-cell implementation planned, not executed. Next outcome: S1,
caller-supplied fixed occupancy with recoverable forward-move failure. Requirements:
[current spec](SPEC.md), grounded in the unchanged [request](OCCUPIED_REQUEST.md).
Design: [proposed local extension to D1](DESIGN.md).

## Pending work

| Stage | Observable outcome / scope | Dependency and boundary | Acceptance / done condition | State |
|---|---|---|---|---|
| S1 | Add optional occupancy to `navigator.run`, copy it per run, and return False for blocked F while continuing commands. Include regression tests and README usage for the optional argument and failure outcomes. | Builds on completed S0 and the proposed design choices. One coherent future commit keeps lookup, failure behavior, tests, and public usage together; no new dependency. | Meet the [design acceptance examples and ownership checks](DESIGN.md#acceptance-and-compatibility), preserve existing calls and errors, pass the complete unittest gate, and resolve snapshot review findings. Main risks: updating pose before checking occupancy, accidentally ending the session, or retaining mutable caller data. | Planned; no implementation or feature validation performed. |

Execution policy for a future authorized implementation: implement and test S1,
run the full check from [DEVNOTES](../DEVNOTES.md), review the resulting snapshot
against the spec/design, fix findings and rerun affected checks, then commit only
when authorized. The fixture specifies no separate human/agent approval gate or
hooks; this plan adds none. Record actual checks, reviewed snapshot identity and
findings with S1 when executed. This document-only phase does not authorize code
changes or commits.

## Completed work (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages existed before this feature request.
The [completed S0 record](history/completed.md) retains its historical acceptance;
it does not approve or validate S1. The [fresh baseline evidence](evidence/occupied-baseline.md)
records inspection and existing checks separately from proposed feature checks.
