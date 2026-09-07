Recorded findings and linked raw evidence in [docs/INVESTIGATION.md](docs/INVESTIGATION.md).

Repeated catalog loading consumed ~91% of profiled runtime. For 5,000 orders and 1,000 catalog rows, loading once per batch reduced median runtime from **1.660 s to 0.00115 s**, with identical output.

Recommend a separately authorized batch-local optimization and representative workload validation before considering infrastructure. Synthetic local results do not establish production latency.

Both existing tests passed. Production code, tests, and prior reports were preserved; no dependencies, services, or commit.