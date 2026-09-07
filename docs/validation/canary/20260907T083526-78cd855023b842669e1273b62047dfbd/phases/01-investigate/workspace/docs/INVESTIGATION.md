# Order report investigation — 2026-09-07

**Recommendation:** Defer the proposed database, cache service and job queue. Repeated catalog loading dominates this local workload. Next, seek authorization to evaluate a small change that loads the catalog once per nonempty batch, then validate against representative batch/catalog sizes and an agreed latency target. This investigation delivers no production change or rebuild design.

**Scope and current behavior:** The current user request authorizes a five-minute, fixture-only investigation and confirms that the catalog is fixed within each batch. [README](../README.md) requires integer-cent totals in order sequence; [report.py](../report.py) reloads, parses and indexes the same JSON catalog for every order. [Existing tests](../tests/test_report.py) also require an empty batch to return `[]` even for a missing catalog. The proposed scratch variant initializes lazily on the first order and keeps state only for that call. Exact totals, order, and the empty-batch behavior must remain compatible. No cross-batch cache is needed by this hypothesis.

**Evidence:** Baseline: 2 existing tests passed, exit 0. A standard-library scratch probe compared current code with a once-per-batch variant using fixed synthetic catalogs of 100/1,000 rows and batches of 100/1,000/5,000 orders. Three paired, alternating-order timing trials per case checked exact results against independently calculated expected lists, including repeated SKUs and zero/negative quantities. All passed; empty input with a missing catalog also passed.

| Catalog rows | Orders | Current median | Scratch median |
| --- | --- | --- | --- |
| 1,000 | 100 | 32.744 ms | 0.378 ms |
| 1,000 | 1,000 | 331.790 ms | 0.504 ms |
| 1,000 | 5,000 | 1,692.616 ms | 1.257 ms |

Separate instrumentation counted 5,000 catalog loads versus 1 for the largest case. Its current-code profile attributed 1.598 of 1.756 seconds (~91%) to `load_catalog`, including 1.110 seconds in JSON loading and 0.193 seconds in file reading (nested times, not additive). The ~1,347× largest-case timing ratio demonstrates avoidable work in this fixture, not a production speedup guarantee. Inspection explains the scaling: repeated catalog work is proportional to orders × catalog rows; loading once makes that work proportional to catalog rows plus orders.

**Limits and next decision:** One machine, three trials, small synthetic files, likely warm filesystem cache; no production trace, cold-disk isolation, concurrency, peak-memory measurement, or end-to-end latency target. Error behavior for malformed catalogs/missing SKUs and custom iterators was not exhaustively compared. Before authorized delivery, establish representative workload sizes and acceptable latency, verify exact totals/order, empty-input behavior, error compatibility and fresh catalog reads across separate batches, and measure time/memory on those workloads. Broader architecture needs independent evidence of persistence, coordination or throughput requirements; this experiment establishes none.

[Commands and statuses](evidence/order-report-20260907-0835/commands.md), [baseline output](evidence/order-report-20260907-0835/baseline.txt), [probe](evidence/order-report-20260907-0835/probe.py), and [raw timings/profile/hashes](evidence/order-report-20260907-0835/results.txt). Probe exit 0; source/test hashes unchanged. Production code, tests and source documents were preserved; no dependencies, services or commit.
