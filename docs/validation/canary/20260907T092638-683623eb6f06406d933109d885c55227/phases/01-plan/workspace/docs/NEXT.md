# Next work: reuse the catalog within each report call

Status: proposed design and implementation plan; no production change implemented.
Authority: [original request](REQUEST.md), [fixture guidance](../AGENTS.md), and
[current API](../report.py). Existing source documents and reports are preserved.

**Next developer outcome:** remove repeated catalog loading within a nonempty
`summarize(orders, catalog_path)` call, with compatibility tests and a before/after
measurement in one reviewable change. Keep the current synchronous API, output
order and exact integer-cent arithmetic. An empty input must still return `[]`
without opening the catalog. Each new call must read a fresh catalog snapshot.

This is a bounded local change: inspection and a small baseline probe establish
avoidable repeated work; they do not establish production latency or justify a
database, shared cache or background queue. A combined design/plan is sufficient.

## Evidence and limits

- [Existing tests](../tests/test_report.py): both passed, exit 0; [raw output](planning-baseline.txt).
- [Reproducible scratch probe](../scratch/probe_report.py): exit 0;
  [raw measurements and profile](planning-probe.txt). It exercises unmodified code
  with a generated 1,000-row, 37,015-byte catalog. Three unprofiled repetitions
  gave median times of 0.000326 s for one order, 0.031454 s for 100 orders and
  0.322908 s for 1,000 orders. Separate profiles counted one catalog load per order
  (zero for empty input). At 1,000 orders, loading consumed 0.309 of 0.338 profiled
  seconds, including JSON decoding, file reads and dictionary construction.
- Exact outputs were checked against independently calculated values. The probe
  also verified iterator input, empty iterators with a missing path and catalog
  freshness between calls.
- These are synthetic local, repeatedly read workloads, subject to filesystem
  caching and profiler overhead. No production trace, approved latency target,
  concurrency measurement or optimized implementation was supplied or measured.
  The measured fraction is evidence for this workload, not a promised speedup.

Commands run from the repository root (scratch existed before execution):

```sh
TMPDIR="$PWD/scratch" PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
TMPDIR="$PWD/scratch" PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" scratch/probe_report.py
```

## Design decision and compatibility

`report.py` currently reads, parses and indexes the whole catalog inside the
order loop. The request explicitly fixes the catalog within a batch and permits
changes between calls. Proposed default: lazily load it when the first order is
encountered and retain that mapping only for the current invocation. Do not use
mapping truthiness as a loaded-state check: an empty catalog is a loaded catalog.
This preserves single-pass iterable inputs and avoids an eager read for empty
input, including an empty generator.

With N orders and C catalog entries, catalog processing changes from O(N*C) to
O(C+N) for a successful nonempty call, with one catalog mapping and the existing
result list retained. Keep `load_catalog` semantics, including last-row-wins for
duplicate SKUs. Preserve lookup and multiplication behavior; do not add rounding,
float conversion, aggregation, validation, error swallowing or partial results.
For nonempty inputs, existing missing-file, malformed-JSON and missing-key errors
continue to propagate. Mid-call catalog mutation is outside the stated snapshot
contract; cross-call changes must remain visible.

A shared cache would add invalidation and stale-price risk. A database or queue
would introduce operational and API decisions with no demonstrated requirement.
Keep those options deferred; the local change needs no new dependency or service.

## One planned implementation stage

**Scope and boundary:** in the subsequent implementation task, change the loading
lifetime in `report.py`, add meaningful regression coverage in
`tests/test_report.py`, and record validation together as one intended commit.
Dependencies: the supplied batch-snapshot contract and prepared runtime; no
external service or outstanding stakeholder answer blocks this local work.

Acceptance examples and risk checks:

| Case | Required result |
| --- | --- |
| Catalog `a=125`, `b=200`; orders `b×2, a×3, b×0` | Ordered rows `[{"sku":"b","subtotal_cents":400},{"sku":"a","subtotal_cents":375},{"sku":"b","subtotal_cents":0}]`, with integer totals |
| Repeated SKUs, multiple orders, including a one-pass iterator | Same ordered results; one catalog load for a successful nonempty call |
| Empty list or empty iterator; nonexistent catalog path | `[]`; zero catalog loads |
| Call with `a=125`, then rewrite catalog to `a=200`; quantity 3 each time | First subtotal 375, second 600; each nonempty call loads independently |
| Nonempty input with missing file or invalid JSON | Existing `FileNotFoundError` or `JSONDecodeError` propagates |
| Unknown SKU or an empty catalog with a requested SKU | Existing `KeyError` propagates; no partial report is returned |
| Duplicate catalog rows for `a` priced 125 then 200; order `a×3` | Subtotal 600, retaining current last-row-wins behavior |
| Large integer price, e.g. `9007199254740993`, quantity 3 | Exact integer subtotal `27021597764222979` |

Done means these behaviors and the existing suite pass, a deterministic load-count
check confirms the intended reduction, and the same synthetic workload has a
recorded before/after comparison with exact-output parity. Timings are diagnostic,
not a brittle CI threshold or an invented service-level objective. Review the
changed snapshot for failure behavior, iterator handling and cross-call freshness.

Follow [contributor checks](../DEVNOTES.md): implement/test, run the existing
unittest command plus relevant new checks, review the snapshot, fix findings and
rerun affected checks before a future authorized commit. No separate reviewer,
hook or CI gate is specified or claimed by this fixture. Record actual commands,
results and reviewed revision/diff with the implementation. This planning pass
does not create a commit or mark that stage complete.

## What would justify going further

After the local change, collect representative batch sizes, catalog sizes and
latency distributions; profile the remaining work and agree a latency/throughput
target with the owner. Those inputs are unknown, not requirements to invent.
If representative performance meets the target, stop. If it misses, use the
remaining measured bottleneck to select the next bounded experiment.

Consider a database only with evidence that catalog access/size or query needs
require it; a shared cache only if repeated cross-call loading remains material
and a versioning/invalidation design preserves freshness; a queue only if agreed
asynchronous UX, job status, retries and operational ownership justify changing
the synchronous contract. Any such expansion needs an explicit design decision
and authorization. The teammate's suggestion supplies neither.

Handoff self-check: original requirements remain authoritative; baseline evidence
is separated from proposed behavior; empty-input and freshness risks are covered;
the next stage has an observable outcome and acceptance. Production adequacy and
the proposed optimization's measured gain remain unverified.
