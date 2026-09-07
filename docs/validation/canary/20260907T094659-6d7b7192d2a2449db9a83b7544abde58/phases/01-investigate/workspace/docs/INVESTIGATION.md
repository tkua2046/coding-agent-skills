# Order report investigation — 2026-09-07

Recommend pursuing a separately authorized, small change to load the catalog once
per nonempty report batch, then measuring representative workloads against an agreed
latency target. The local evidence does not justify a database, cache service, or
job queue. This entry is intake/investigation only; no feature or rebuild was delivered.

Confirmed scope comes from the current user request, [README](../README.md), and
[AGENTS](../AGENTS.md): catalog is fixed within each batch; preserve exact integer-cent
totals, order sequence, production code/tests, source inputs and prior reports.
[Current code](../report.py) reloads, parses, and indexes the entire JSON catalog for
each order. [Existing tests](../tests/test_report.py) cover one subtotal and an empty
batch with a nonexistent catalog. Both passed (exit 0; [baseline output](investigation-evidence/baseline.txt)).

**Bounded evidence.** A standard-library scratch probe compared current behavior with
one lazy catalog load per batch, using synthetic catalogs of 100/1,000 rows and
batches of 100/1,000/5,000 orders. Three wall-time repetitions per case alternated
execution order; every full output matched both the candidate and calculated totals.
For the 1,000-row catalog, median seconds were:

| Orders | Current | Scratch |
| --- | ---: | ---: |
| 100 | 0.032668 | 0.000345 |
| 1,000 | 0.328819 | 0.000468 |
| 5,000 | 1.660186 | 0.001148 |

For 1,000 orders, measured loader calls dropped from 1,000 to 1. A separate profile
at that size attributed 0.316/0.346 seconds (~91%) to `load_catalog`, including
0.219 seconds in JSON loading and 0.036 seconds in file reading (nested times,
not additive). Inspection explains scaling from roughly O(orders × catalog rows)
to O(orders + catalog rows). The probe also matched iterator input, repeated SKUs,
zero/negative quantities, missing-file/SKU/quantity and malformed-JSON outcomes.
For example, an empty iterator with a missing catalog still returns `[]`; loading
unconditionally before iteration would break this existing behavior.

**Limits and next decision.** These are small synthetic local files (3,890/40,015
bytes), repeated in one process with likely warm filesystem caches. Three samples
and profiler overhead do not establish production latency, cold-storage behavior,
memory usage, concurrency, or an SLA. The evidence isolates redundant loading in
this fixture, not every cause of real batch slowness. A batch-local catalog is a
proposed implementation default, with no shared state or cross-batch invalidation;
the scratch probe is not production delivery. Before implementation, obtain typical
and largest order/catalog sizes and an acceptable latency target, then validate the
small change on that workload with compatibility review. Reconsider infrastructure
only if residual measurements or independent durability/concurrency requirements
support it. No stakeholder contact was made.

[Reproduction commands and exit statuses](investigation-evidence/commands.md),
[probe source](investigation-evidence/probe.py), and
[raw timings/profile/assertions](investigation-evidence/results.txt) retain the evidence.
