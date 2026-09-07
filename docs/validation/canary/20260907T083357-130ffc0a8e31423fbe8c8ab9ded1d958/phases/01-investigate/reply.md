Recorded findings in [docs/INVESTIGATION.md](docs/INVESTIGATION.md), with linked commands and raw evidence.

Repeated catalog loading consumed ~91% of profiled runtime. For 1,000 orders and 1,000 catalog rows, the scratch batch-local version reduced median time from 322 ms to 0.471 ms with matching outputs.

Recommend evaluating a minimal per-batch catalog reuse change before considering infrastructure. These synthetic, warmed-file measurements don’t establish production performance; representative workloads and a latency target remain needed.

Both existing tests passed. Production code and tests are unchanged; no dependencies, services, or commit.