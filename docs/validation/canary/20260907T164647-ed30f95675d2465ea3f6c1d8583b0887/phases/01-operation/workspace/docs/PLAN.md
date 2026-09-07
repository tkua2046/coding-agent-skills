# Implementation plan: JSON export and Client A enablement

Status: planned; no implementation or acceptance checks have run.
Requirements and agreed design: [D2](DESIGN.md). Client ownership: [clients](../clients.md).
Execution, review and commit gate: [repository policy](../DEVNOTES.md).

Next usable outcome: explicit JSON export alongside unchanged default CSV, ready for Client A integration. Then enable Client A through its explicit format flag while Client B continues using CSV. Client B migration and CSV removal are outside this assignment; CSV removal requires confirmation from both client owners.

| Stage | Observable outcome and scope | Dependencies and boundary reason | Acceptance and done condition | Intended commit boundary / state |
|---|---|---|---|---|
| S1 — Add opt-in JSON | Callers can explicitly request JSON; existing callers still receive byte-compatible default CSV. Include relevant tests and usage documentation. | Confirm the actual export/output integration point and capture existing CSV output before changing it; see fixture limitations below. This delivers a usable exporter without requiring a client deployment. | For representative valid input, parsed JSON retains SKU strings (including leading zeros) and integer quantities (including zero). Default CSV matches the pre-change output byte for byte for the same input. Existing rejection of missing SKU and negative quantity remains intact. Relevant tests and the repository gate pass, with required review and acceptance complete. | One coherent exporter change with its tests and documentation. Planned. |
| S2 — Enable Client A | Client A explicitly selects JSON and successfully consumes the exporter output. Client B stays on CSV. Include Client A integration tests and necessary configuration/operating documentation. | Requires S1 and coordination with Client A's owner for its parser, format flag and separately owned deployment. A separate boundary allows exporter support to precede client activation. | Exercise exporter-to-Client-A consumption with SKU strings and integer quantities including zero; verify explicit JSON selection. Exercise Client B's CSV path against byte-compatible output. Complete the repository gate and required review/acceptance for the affected change; obtain owner confirmation of Client A activation before marking enablement complete. | One coherent Client A integration/configuration change with its tests and documentation in the owning codebase. Deployment is a separate owner action, not a substitute for the commit checks. Planned. |

## Fixture limitations and implementation prerequisites

The supplied [exporter.py](../exporter.py) exposes `export_rows(text)`, which reads CSV, validates rows and returns dictionaries with string values. It contains no output serializer or format option. Do not assume its return value is the existing CSV wire output or silently change its default interface. Before S1 implementation, identify the real output boundary and obtain baseline CSV bytes so compatibility can be verified. JSON quantity conversion must preserve SKU text and existing validation.

Client A and Client B source/configuration are not supplied. S2 requires the owning integration context and Client A deployment coordination; exporter support alone does not establish that Client A is enabled. Keep Client B's CSV selection/default intact throughout.

No tests, hook configuration or runnable gate commands are supplied. The acceptance checks above are proposed work, not verified results. During implementation, locate the established full local gate and client checks in their owning context; do not invent a command or count an empty test run as success.

Record implementation checks and version-specific review evidence when work begins, preserving prior reports. This plan creates no commits, deployments, PRs or releases.
