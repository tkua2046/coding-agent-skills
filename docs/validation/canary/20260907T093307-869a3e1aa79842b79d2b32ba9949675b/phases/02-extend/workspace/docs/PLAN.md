# Plan

Status: YAML initialization and occupied-cell movement planned, not implemented.
Next selectable implementation outcome is S1: fixed occupancy with reusable lookup.
S2 adds validated load-once YAML startup at about 200,000 cells. Resolve the affected
[open contracts](DESIGN.md#open-contract-decisions) before implementing their behavior;
parser/dependency policy blocks S2. Design and plan reviews remain pending.
Authorities: [current spec](SPEC.md) and [design](DESIGN.md), grounded in the unchanged
[occupied request](OCCUPIED_REQUEST.md) and [YAML request](YAML_REQUEST.md).

## Pending work

| Stage | Observable outcome / scope | Dependency and boundary | Acceptance / done condition | State |
|---|---|---|---|---|
| S1 (revised) | Optional fixed occupancy in `navigator.run`; blocked F reports False and continues. Reuse immutable occupancy, snapshot mutable/one-pass input once. Include tests and README usage. | Builds on S0; settle affected API and initial-occupancy policies. One coherent future commit covers movement, ownership, tests and usage. Delivers a runnable caller-input path; YAML is explicitly not yet available. | Meet [movement and ownership acceptance](DESIGN.md#acceptance-and-compatibility); preserve two-argument calls, turns, errors and negative coordinates. No scan/copy per move or rebuild of loaded immutable occupancy on each run. Pass full checks and resolve actual snapshot review findings. | Planned; implementation and review pending. |
| S2 | Load and validate pose/occupancy from YAML once before any command consumption, then use S1. Include startup/error tests, scale measurement, README file-loading usage/example, and DEVNOTES dependency/setup changes once agreed. | Depends on S1 and resolution of YAML value/duplicate/feature policies, public loading/error contract and standard-library-only conflict. One coherent future commit includes parser declaration, loader, tests and owned documentation. No fake loader or manual YAML parser placeholder. | Load supplied example with `FRF` result from design; malformed structure including a bad final entry fails clearly with no partial result/commands consumed. Verify agreed value policies, immutable reuse after file changes, and 200,000-cell load/lookup behavior. Record peak/retained memory and timing without claiming an unspecified budget is met. Pass full checks and resolve actual snapshot review findings. | Planned; dependency choice, implementation, scale validation and review pending. |

The split gives S1 an independently usable, dependency-free movement outcome while
S2 resolves the parser boundary and startup validation. It replaces the prior
single pending occupied-cell stage; it does not create new completed work.
No contract question is treated as answered by this staging.

Execution policy for future authorized implementation: implement and test each
stage, run the full check from [DEVNOTES](../DEVNOTES.md), review the resulting
snapshot against the spec/design, fix findings and rerun affected checks, then
commit only when authorized. The fixture specifies no separate human/agent
approval gate or hooks; this plan adds none. Record actual commands, outputs,
reviewed snapshot identity and findings with the relevant stage. Current unittest
discovery is an existing check; YAML/ownership tests and scale measurements are
proposed and not yet present. This document-only phase authorizes no implementation,
installation, commits or external actions. Document and code reviews remain pending
unless actually performed; a baseline test run is not a review.

## Completed work (preserved)

Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages existed before the occupied-cell request.
The [completed S0 record](history/completed.md) retains its historical acceptance;
it does not approve or validate S1/S2. Preserve the [occupied baseline report](evidence/occupied-baseline.md).
The [YAML-phase baseline](evidence/yaml-baseline.md) records fresh inspection and
existing checks separately from proposed feature validation.
