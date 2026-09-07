# Order report investigation

## 2026-09-07 — large batches

**Conclusion / next action:** Do not replace the report with a database, cache
service, or job queue based on the current evidence. The local experiment isolates
repeated catalog loading as a sufficient explanation for the observed batch-size
scaling, but it is synthetic and does not establish production latency. Next,
propose and review the smallest compatible change: reuse one loaded catalog within
each non-empty `summarize` batch, retaining order sequence, exact integer-cent
totals, and the existing empty-batch behavior (which does not access the catalog
path). Add multi-order equivalence/one-load coverage and measure a representative
production batch before considering infrastructure.

**Evidence:** With a fixed 1,000-row JSON catalog and five median-timed repeats,
the current implementation took 0.003182s, 0.031965s, and 0.327907s for 10, 100,
and 1,000 orders. A scratch load-once equivalent took 0.000319s, 0.000334s, and
0.000483s (10.0x, 95.6x, and 679.1x faster); outputs matched for all generated
cases. The baseline tests also passed. Commands and full output are in
[`order-report-evidence.txt`](order-report-evidence.txt); the reproducible harness
is [`../investigations/benchmark_report.py`](../investigations/benchmark_report.py).

**Limits:** This is a short synthetic benchmark on one machine and warm local
filesystem caches, using valid SKUs, one catalog size, at most 1,000 orders, and no
concurrency. It demonstrates the cost and scaling of repeated local parse/read
work; it does not quantify production latency, prove behavior for every input/error
case, or rule out additional production bottlenecks.
