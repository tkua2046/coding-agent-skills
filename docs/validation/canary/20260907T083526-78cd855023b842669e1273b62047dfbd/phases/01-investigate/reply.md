Defer the rebuild. Repeated catalog loading consumed **91% of profiled runtime** locally.

For 5,000 orders and 1,000 catalog rows, a scratch once-per-batch variant reduced median time from **1.693 seconds to 1.257 milliseconds**. Exact outputs matched across all six synthetic cases; both existing tests passed.

These small, likely warm-cache measurements don’t establish production performance. Next, evaluate the batch-local change against representative workloads, compatibility checks, and an agreed latency target.

Findings and linked evidence: [docs/INVESTIGATION.md](docs/INVESTIGATION.md). Production code and tests remain unchanged; no dependencies, services, or commit.