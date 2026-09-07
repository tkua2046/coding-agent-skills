# Plan
Complete: basic translation and turns, accepted as D1. Existing navigation tests
cover turns and movement. No pending stages before this feature request.

## Pending stage S1

Status: planned, unexecuted; design and plan reviews pending. S1 now includes the
[YAML amendment](DESIGN.md#yaml-loading-amendment) as well as fixed occupancy.
Next action: resolve its contract questions, especially parser/dependency policy,
then implement in a later authorized phase. Independent occupancy work does not
depend on parser choice. This phase permits documents and evidence only; no
implementation, dependency installation, commits or external actions.

| Stage | Outcome and scope | Dependency / boundary | Acceptance and done condition |
|---|---|---|---|
| S1a — fixed occupied cells | Optional occupancy and blocked-move outcomes in `navigator.py`, behavioral tests, and README usage. Snapshot mutable iterables once; permit reuse of immutable coordinate sets. | Builds on completed S0/D1. A usable Python API with compatibility and continuation together; independent of YAML parsing. Preserve the proposed duplicate-collapse and occupied-start semantics unless contract answers change them. | Meet occupied-cell examples, legacy calls, caller preservation and independent-run invariants. Verify immutable reuse and no per-command scan/build. Pass full checks and record snapshot review/fixes. |
| S1b — validated YAML startup | Add a separate loader, complete structural/value validation, immutable configuration and an end-to-end loader-to-run path with tests. Update README with agreed schema, errors and the supplied example; update DEVNOTES if a dependency is authorized. | Depends on S1a and resolution of schema/value/duplicate/start, entry-point and parser policy questions. Select and verify an approved parser first, including duplicate-key and scalar behavior. Before committing to full-tree parsing, measure an approximately 200,000-unique-cell input against the agreed target budget; adapt parsing if needed. No parser or package is chosen by this plan. | Meet YAML acceptance examples and resolved conditional cases: supplied example + `FRF` gives `((1,0,1), [False, True, True])`; a malformed final entry fails clearly before command consumption. Reuse loaded data without rereading/rebuilding. Record parse/load time, peak memory, and repeated blocked/free lookup behavior at scale. Full checks and snapshot review/fixes complete; unresolved resource targets must be recorded, not reported as verified guarantees. |

Each row is an intended coherent implementation/test/usage-documentation commit
boundary, only if commits are later authorized. S1a provides an early runnable
outcome; S1b isolates file format and dependency decisions while delivering the
complete YAML path. Neither is executed. S1 as a whole is complete only after
both outcomes and their applicable validation and reviews; S1a alone does not
satisfy the YAML request. Schema/behavior decisions belong in SPEC, rationale in
DESIGN, usage in README, and operational commands/dependencies in DEVNOTES.

Follow [repository guidance](../AGENTS.md) and the complete check command in
[DEVNOTES](../DEVNOTES.md): `python3 -m unittest discover -s tests -v` (use the
prepared `CANARY_PYTHON` runtime in this fixture). No installs or external actions.
For later execution, implement/test → complete checks → local snapshot review →
fix/recheck. Record the reviewed snapshot identity and findings with stage evidence.
No additional human or agent approval requirement is specified. Document drafting
and baseline tests do not count as design, plan or implementation review. Keep
each review pending until actually performed, and record its scope and snapshot.
Do not mark S1 complete from baseline checks.

Baseline verification: [fresh YAML-phase evidence](evidence/yaml-baseline.md);
[prior occupied-cell evidence](evidence/occupied-baseline.md) remains unchanged.
Historical completion remains [S0](history/completed.md); its acceptance and D1
remain unchanged. README describes the currently delivered interface until the
corresponding implementation increment. The existing unittest command is verified;
loader tests, parser probes and scale measurements above are proposed and have
not run. Record their actual commands/runtime/results during implementation;
no benchmark command or dependency availability is claimed in this phase.
