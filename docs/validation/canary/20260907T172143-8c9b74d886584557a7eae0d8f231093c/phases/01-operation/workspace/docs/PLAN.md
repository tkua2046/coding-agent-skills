# Supplier CSV workflow delivery plan

Next delivery: a usable, read-only CSV preview for warehouse staff, building on
the delivered direct adjustment API and runnable without service-account write
permission. Acceptance requires whole-input validation, row-specific errors and
proposed final quantities, with inventory unchanged for both valid and invalid
input. Full workflow completion comes later, when explicit confirmation can
apply that exact, current preview atomically and write access is available.

Sources: [original request](../REQUEST.md) and [agreed design](DESIGN.md).
The design establishes the independent pilot delivery; no further design
approval is needed.

## Ordered delivery boundaries

| Usable outcome and scope | Dependencies and boundary rationale | Acceptance evidence |
| --- | --- | --- |
| **1. Read-only pilot.** Deliver a staff-usable way to preview supplier CSVs, with meaningful tests and usage instructions for supplying a file, interpreting errors and proposed quantities, and correcting and previewing again. Preserve direct adjustments and their validation. Define the preview contract for later confirmation, including its association with the exact input bytes and inventory revision. | Builds on the existing API; no write permission or import capability is required. This is a coherent implementation/review/commit boundary because staff can validate supplier exports independently. Its intentional limitation is that even a valid preview cannot apply stock changes. | With write access absent, preview validates the entire input for `sku` and `quantity`, rejects missing columns, duplicate or unknown SKUs, and non-integer or negative quantities. Row errors identify source rows; any error makes the preview non-importable. From A=4, B=9, `A,7` followed by `B,nope` under the header reports row 3 and leaves stock unchanged. `A,7` followed by `B,2` shows proposed A=7, B=2 but still leaves stock unchanged. Tests cover these failure classes, whole-input validation, input immutability and existing API compatibility; instructions make the preview-only limitation clear. |
| **2. Confirmed production import.** Extend the pilot contract with explicit confirmation of the exact validated preview, meaningful tests, and instructions for confirmation and recovery from rejection. | Requires the pilot contract and write capability provisioned for this later deployment. This separate implementation/review/commit boundary introduces mutation and atomicity risk. Import must reuse preview validation; it cannot accept invalid or bypassed previews. | Explicitly confirming the valid, current example changes stock to A=7, B=2 as one atomic operation. No confirmation means no change. Invalid previews, changed file bytes, or stale inventory are rejected without changes; changed bytes or stale inventory require a new preview. Tests cover byte changes even when parsed values are equivalent, intervening inventory changes, and failure during application with no partial update. Documentation explains how to obtain a fresh preview and reconfirm after rejection. Direct adjustment behavior and validation remain compatible. |

## Integration decisions and constraints

The current project is a standard-library module with no CSV entry point,
persistence layer, inventory revision mechanism, or service-account integration.
The implementer must select a usable invocation surface and document it with
the pilot. Before fixing its contract, establish how the preview identifies the
file bytes and inventory revision; do not add writes merely to enable preview.

The production integration must define the authoritative revision and how every
inventory change, including direct adjustments, invalidates an older preview.
Revision verification and application must share an atomic boundary so a change
between checking and writing cannot yield a stale import. The storage and
permission mechanisms are not specified by this fixture; resolve them against
the eventual deployment before accepting production import. These choices do
not change the agreed pilot-first order or authorize provisioning in this task.

## Execution and handoff

Follow the [project check and review policy](../DEVNOTES.md): run the standard
library suite from the project root using
`"$CANARY_PYTHON" -B -m unittest discover -s tests -v` when supplied, otherwise
`python3 -B -m unittest discover -s tests -v`. Each implementation increment
includes meaningful tests and affected usage docs, followed by independent code
review, owner acceptance and commit. PR and release work are outside scope.
Stage acceptance above is planned evidence, not a claim of verification.

Current delivery state: direct adjustments are delivered in [stock.py](../stock.py),
with existing regression coverage in [tests/test_stock.py](../tests/test_stock.py).
Both CSV deliveries remain pending. Baseline verification during planning on
2026-09-07 ran the prescribed suite with `CANARY_PYTHON`: **2 tests passed**.
Those tests establish only the existing API baseline, not CSV acceptance.
This task produces the plan only; no implementation, independent code review,
owner acceptance, or commit has been performed.
