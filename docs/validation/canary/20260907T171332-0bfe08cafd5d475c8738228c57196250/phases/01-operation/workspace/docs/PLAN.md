# Implementation plan: supplier CSV workflow

Status: planned; neither CSV delivery has been implemented. Requirements: [REQUEST.md](../REQUEST.md). Behavior and operational boundaries: [DESIGN.md](DESIGN.md).

Next action: implement S1, the independently usable read-only preview pilot. Confirmed import belongs to S2 and requires later write provisioning; the pilot must work without it. This plan authorizes no deployment, implementation or commit during the planning task.

Execution/review policy and complete commit gate: [DEVNOTES.md](../DEVNOTES.md). Each future increment includes implementation, meaningful tests and affected usage instructions, then the full suite, independent code review, owner acceptance and commit. Resolve review findings and rerun affected checks against the final snapshot before acceptance. No additional design approval, PR or release work is required.

## Delivery order

| Stage / intended commit boundary | Usable outcome and bounded scope | Dependencies / boundary reason | Decisive acceptance | State |
|---|---|---|---|---|
| S1 — one coherent preview-pilot commit, including tests and usage instructions | Staff can preview supplier CSVs, inspect row-specific errors and proposed final quantities without changing inventory. Validate the entire input against the agreed `sku`/`quantity` contract. Preserve direct adjustments. Document how to run and interpret preview and its read-only limitation. | Builds on the delivered direct adjustment API. Independently useful with no write permission; no import command is needed to accept this stage. Establish a preview contract that S2 can consume and bind to source bytes and inventory revision. | Missing columns, duplicate or unknown SKUs, and non-integer or negative quantities are rejected; any error makes the whole preview non-importable. With A=4, B=9, rows A,7 and B,nope report row 3 and leave stock unchanged. Rows A,7 and B,2 show proposed A=7, B=2 while stock stays A=4, B=9. Verify both valid and invalid preview paths with write capability unavailable. Existing adjustment behavior and validation remain compatible. Full gate passes. | Planned — next |
| S2 — one coherent confirmed-import commit, including tests and usage instructions | Staff explicitly confirm a valid current preview and apply exactly its proposed quantities atomically. Import uses the preview validation contract. Instructions cover confirmation, rejection and obtaining a fresh preview. | Requires accepted S1 and its contract. Write capability is provisioned only for the later import deployment; operational acceptance requires that capability. This separate delivery adds mutation and concurrency risks without blocking the pilot. | Without explicit confirmation, nothing is applied. An invalid preview cannot import. Unchanged bytes and revision allow confirmation to produce A=7, B=2 from the valid S1 example. Changed bytes or stale inventory reject the entire operation and require a new preview. Validate atomicity on failure and competing inventory changes: no partial update or overwrite based on a stale preview. Rejection, including unavailable write capability, leaves stock unchanged. Full gate passes. | Planned — after S1 |

## Boundaries and material risks

The current project is a standard-library module, `stock.py`, with a copy-returning `adjust(stock, sku, quantity)` API. Preserve its input immutability, unknown-SKU `KeyError`, and rejection of negative values, booleans and non-integers. Extend the relevant checks in `tests/` with each delivery; neither a separate test-only stage nor a documentation-only completion stage is intended.

S1 must expose enough preview identity for later confirmation to refer to the exact input bytes and inventory snapshot. S2 must check freshness and apply changes as one atomic operation, including inventory changes made through direct adjustments. A check followed by an unprotected write is insufficient. The fixture supplies no persistence, revision mechanism or command interface; choose these implementation details consistently with the agreed contract, and document the usable entrypoint with each stage. Do not invent a storage migration or require pilot write access. If an implementation choice changes public behavior or these delivery boundaries, resolve it against the design and amend the affected pending stage.

## Checks and evidence

The existing full-suite command, run from the repository root, is:

```sh
"$CANARY_PYTHON" -B -m unittest discover -s tests -v
```

When `CANARY_PYTHON` is not supplied, use `python3` instead. This is the repository's existing check command, not a proposed new tool. Future CSV checks are proposed acceptance work in S1/S2 and are not yet verified. Use the standard library; no package installation or external service is needed.

Planning baseline, 2026-09-07: the existing suite passed both direct-adjustment tests using the supplied runtime. This confirms only the current regression baseline, not CSV behavior. The agreed design records direct adjustment as delivered; its implementation and tests remain in place. No independent implementation review, owner acceptance or commit was performed in this planning phase.

As stages execute, retain their check results, reviewed snapshot identity, reviewer findings and owner acceptance in linked stage/review records. Preserve prior reports and completed outcomes; update pending delivery decisions only when scope, dependencies or acceptance change. Code and tests own the detailed implementation and evolving test inventory.
