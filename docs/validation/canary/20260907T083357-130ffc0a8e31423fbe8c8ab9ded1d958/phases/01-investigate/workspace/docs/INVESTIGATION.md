# Order report investigation — 2026-09-07

Recommendation: defer the database/cache-service/job-queue proposal. Evaluate loading the catalog once per nonempty report batch as the next narrowly scoped change, subject to separate delivery authorization. The local experiment identifies repeated catalog loading as the dominant cost; it does not establish production performance.

Confirmed scope/source: this session's user request (fresh intake, five-minute local investigation, fixed catalog within each batch, preserve production/tests/prior reports, no dependencies/services/commit); [README](../README.md) defines ordered integer-cent results, and [AGENTS](../AGENTS.md) allows scratch experiments only. No rebuild or feature implementation is authorized. Intake guidance: [feature-design](../skills/feature-design/prompts/intake-feature.md).

Current behavior: [`summarize`](../report.py) calls `load_catalog` inside the order loop, rereading JSON and rebuilding the SKU map on every order. It preserves order and integer arithmetic; empty input never opens the catalog. [`tests/test_report.py`](../tests/test_report.py) covers a subtotal and empty input with a missing file. Both existing tests passed (exit 0; [baseline output](investigation-evidence/baseline.txt)).

Evidence: a stdlib-only scratch comparison uses the same loader once per nonempty batch. Three unprofiled repetitions per case alternate implementation order, after a correctness warmup. Selected medians:

| Catalog rows | Orders | Existing | Scratch batch-local |
|---:|---:|---:|---:|
| 1,000 | 100 | 31.4 ms | 0.328 ms |
| 1,000 | 1,000 | 322 ms | 0.471 ms |
| 1,000 | 3,000 | 974 ms | 0.807 ms |
| 100 | 1,000 | 52.7 ms | 0.213 ms |
| 3,000 | 1,000 | 965 ms | 1.208 ms |

For 1,000 orders/1,000 catalog rows, instrumentation counted 1,000 loads versus one. A separate existing-code profile attributed 0.311 of 0.341 seconds (~91%) to `load_catalog`, including 0.214 seconds in JSON loading and 0.038 seconds in file reading (nested times, not additive). This supports repeated parsing/map construction and file access as the mechanism, with expected work changing from O(orders × catalog rows) to O(orders + catalog rows). It does not support attributing the slowdown chiefly to physical disk latency.

All timed outputs matched. Scratch probes also matched sequence/repeated SKUs, duplicate catalog SKU behavior, zero/negative/large integer quantities, generator input, and missing-SKU/file/malformed-JSON exceptions. Examples: price 125 × quantity 3 remains 375 cents; empty input with a missing path stays `[]` with zero loads. Source and test SHA256 values were unchanged. [Raw results](investigation-evidence/probe.txt), [reproduction commands](investigation-evidence/commands.md), and [scratch probe](../scratch/order-report-investigation/probe.py) retain the evidence.

Limits and next decision: synthetic catalogs of 100–3,000 rows and batches of 100–3,000 orders, one local Python 3.12.4 process, warmed filesystem cache, three samples, no concurrency, memory profiling, production data, cold-storage measurements, or latency target. Sub-millisecond candidate timings and observed speedups are not a production promise; compatibility probes are not exhaustive. Proposed default is per-invocation reuse, with lazy loading to retain empty-input behavior and no reuse across batches. Before delivery, establish representative batch/catalog sizes, latency target and memory budget, then validate a separately authorized minimal change with regression coverage including freshness between batches. These answers determine whether the local fix meets the actual workload; no clarification blocks this investigation. Reconsider infrastructure only if representative measurements or independent persistence/asynchronous-processing requirements justify its operational complexity.
