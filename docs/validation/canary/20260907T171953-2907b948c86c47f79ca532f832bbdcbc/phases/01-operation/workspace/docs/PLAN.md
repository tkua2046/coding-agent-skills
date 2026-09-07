# JSON export and Client A enablement

Next usable outcome: an explicit JSON export option alongside unchanged default CSV. Before implementing, identify the consumer-facing export entry point and obtain representative current CSV output: the supplied `export_rows` reads CSV and returns dictionaries, but does not serialize output. Acceptance requires JSON to preserve SKU strings and emit integer quantities, including zero, while default CSV remains byte-compatible for identical input.

The assigned outcome extends through Client A explicitly selecting JSON, with Client B continuing to receive CSV. Client B migration and CSV removal are outside this assignment.

| Ordered outcome and meaningful commit boundary | Dependencies and boundary rationale | Acceptance evidence to produce |
|---|---|---|
| 1. Deliver optional JSON export with the existing default CSV behavior, relevant compatibility and validation tests, and format-selection documentation in one coherent implementation commit. | Resolve the export entry point and capture the existing CSV byte contract first. This is a usable producer capability that can ship before either separately owned client deployment; both clients initially remain on CSV. | Parse exported JSON and verify exact SKU strings, including leading zeros, and integer quantities including zero. Compare default CSV bytes against captured existing output for the same inputs; verify explicit CSV selection preserves that contract. Verify missing/empty SKU and negative or non-integer quantity still fail rather than producing a successful export, and unsupported format selection fails explicitly. |
| 2. Enable Client A to explicitly request and parse JSON, with its integration checks and affected usage/deployment documentation in a separate client change. Keep Client B on CSV. | Requires outcome 1 to be available and coordination with Client A's owner: its parser and deployment configuration are absent from this fixture. The boundary reflects separate deployment ownership and allows independent rollback. | Run an end-to-end Client A export/read check preserving SKU strings and integer quantities including zero. Demonstrate Client A explicitly opts in, while the existing Client B path still receives byte-compatible CSV. Exercise returning Client A to explicit CSV selection and confirm it can consume exports again without a producer rollback. |

Sources: [agreed design D2](DESIGN.md), [client ownership and format assumptions](../clients.md), and [current exporter](../exporter.py).

Execution and review follow [repository policy](../DEVNOTES.md). The fixture supplies no full-gate command or test configuration; locate the established gate in the implementation environment before executing it. No additional approval procedure, PR, release, or version work is proposed here.

Material integration details remain to be resolved with the relevant source and owners: the external export option and JSON payload shape are not specified in D2, and Client A's format flag alone does not establish JSON parser support. Agree that producer/consumer contract before outcome 1 so outcome 2 can use it. Preserve existing validation behavior when adding serialization; no broader input-validation redesign is assigned.

CSV remains available until both client owners confirm migration. Client B's later opt-in and any subsequent removal require future scope; completing Client A enablement does not authorize either.

## Current delivery status

Planning only. Both outcomes are proposed; no implementation, deployment, acceptance checks, or commits have been performed. No prior reports or source records were changed.
