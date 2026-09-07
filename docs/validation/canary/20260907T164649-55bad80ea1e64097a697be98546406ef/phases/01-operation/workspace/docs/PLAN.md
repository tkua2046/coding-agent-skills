# JSON export and Client A enablement

Next usable outcome: callers can explicitly request JSON while existing callers, including Client B, continue receiving byte-compatible default CSV. Before implementation, locate the actual CSV output boundary and compatibility baseline, and agree the JSON wire shape and option with Client A. Decisive acceptance is the same stock input producing JSON with string SKUs and integer quantities (including zero), while default CSV matches the existing output byte for byte.

| Outcome / proposed commit boundary | Dependencies and reason for boundary | Acceptance evidence to produce |
|---|---|---|
| Add opt-in JSON alongside unchanged default CSV, with relevant tests and format/usage documentation in the same implementation commit. | Resolve the output boundary and shared format contract below. This is a usable exporter capability that can ship before any client deployment; Client A remains on CSV until its own enablement. | Exercise the public export path with ordinary stock, a leading-zero SKU, and zero quantity. Parse JSON and verify exact SKU strings and integer quantities; compare default CSV bytes with the pre-change baseline for the same inputs. Verify CSV remains available explicitly for client opt-in configuration. Preserve rejection of missing/empty SKU, non-integer quantity, and negative quantity without returning a successful partial export. Reject unsupported format options clearly. |
| Enable Client A's explicit JSON selection and parser, with its integration tests and configuration/rollback documentation in a separate client-owned commit. | Requires the compatible exporter capability to be available in Client A's target environment, the agreed JSON contract, and access to Client A's code and deployment owner. Separate ownership and deployment make this a distinct acceptance boundary. | Demonstrate exporter-to-Client-A consumption with string SKUs and integer quantities including zero. Verify malformed JSON or invalid stock values fail visibly. Demonstrate Client B still consumes byte-compatible default CSV during the mixed-format rollout. Verify Client A can explicitly select CSV again and consume it if JSON rollout must be rolled back. |

Sources: [agreed design D2](DESIGN.md), [client ownership](../clients.md), and [current exporter](../exporter.py). Execution/review policy: [DEVNOTES.md](../DEVNOTES.md), subject to [repository scope restrictions](../AGENTS.md). Apply the established gate and review policy to each implementation increment; this planning phase does not execute those gates or request additional approval.

## Dependencies and limits

The supplied exporter reads CSV into a list of dictionaries; it does not serialize CSV or JSON, and quantities remain strings after validation. The fixture contains no callers, client implementations, compatibility fixtures, test configuration, or full local gate commands. Locate the production output path and representative existing CSV bytes before claiming byte compatibility; do not treat this function's dictionary return value as a CSV output baseline. Obtain the established gate commands from repository maintainers before executing implementation checks rather than inventing a replacement gate.

D2 fixes value types and opt-in behavior but leaves the JSON envelope, empty-input representation, and public format-selection interface unspecified. Agree these with Client A before implementing the shared contract. Client A's parser and deployment configuration must be supplied or changed in its owning repository; exporter support alone does not complete Client A enablement. Deploy exporter support before enabling Client A's JSON flag.

Client B remains on CSV throughout this assignment. Its later migration and CSV removal are excluded. Retain CSV until both client owners confirm migration, as required by D2; neither Client A enablement nor its rollback authorizes removal. No PR, version, or release work is included.

## Current delivery state

Planning only: both outcomes are proposed and unimplemented. Acceptance checks above are planned, not verified. No implementation tests, gates, or reviews have been run in this phase. Existing source and reviewed records remain unchanged.
