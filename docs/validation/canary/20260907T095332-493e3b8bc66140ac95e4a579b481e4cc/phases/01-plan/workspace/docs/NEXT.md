# Next work: reuse the catalog within a report batch

Status: proposed design and implementation plan; production change not implemented.

**Next developer outcome:** retain the catalog after its first load within one
`summarize(orders, catalog_path)` call. Load only when the first order is consumed,
reuse it for that batch, and discard it when the call ends. Deliver this local
change with compatibility tests and a before/after measurement in one reviewable
commit. No database, shared cache, queue, dependency, or API change is justified
by the available evidence.

The authority is [the original request](REQUEST.md), supported by
[README](../README.md) and the current [implementation](../report.py). The catalog
is fixed within a batch but may change between calls; results must remain exact
integer-cent subtotals in input order. A short combined design and plan fits this
bounded, reversible change: the uncertain repeated-work premise has now been
checked locally. This proposal does not claim an approved architecture or a
measured production bottleneck.

## Evidence and design

The existing implementation loads, reads, parses, and indexes the whole catalog
inside the order loop. Both existing tests passed (exit 0), using the
[contributor command](../DEVNOTES.md); [raw baseline output](../scratch/report-planning/baseline.txt).
Those tests cover one subtotal and an empty list with a missing catalog only.

A [reproducible scratch probe](../scratch/report-planning/probe.py) ran the unchanged
implementation on a synthetic 1,000-row catalog. At 0, 1, 100, and 1,000 orders it
observed respectively 0, 1, 100, and 1,000 catalog loads. The 1,000-order run took
about 0.323 seconds; a separate profiled run took 0.334 seconds, with 0.305 seconds
cumulative in `load_catalog` (about 91%). Exact expected results were asserted.
[Raw probe output](../scratch/report-planning/probe.txt), exit 0, also records
compatibility observations. These are single synthetic local runs, with mock or
profiler overhead, not production measurements or a speedup estimate.

**Proposed decision:** batch-local lazy loading preserves the empty-input behavior
and iterable API while eliminating redundant reads and parsing. For N orders and
C catalog rows, catalog work goes from approximately O(N × C) to O(C), with O(N)
order processing and existing output storage. Catalog memory remains O(C), now
retained across the batch. Keep `load_catalog` semantics, including last duplicate
SKU winning; introduce no new validation, numeric conversion, or rounding.

An eager load before the loop would break empty batches with missing paths.
A process-wide/shared cache would risk stale data between calls and require an
invalidation policy. A database or queue introduces persistence or asynchronous
behavior without addressing a demonstrated requirement; neither is a prerequisite
for removing this repeated work. No production latency target is assumed.

## Acceptance for the implementation

Preserve the public signature, returned list of dictionaries, input sequence, and
existing exception behavior. Do not require `len(orders)`, indexing, a second
iteration, or materializing orders before processing.

| Case | Required result or observation |
| --- | --- |
| Catalog `a=125`, `b=230`; orders `b×2, a×3, b×0, a×(-2)` | In that order: `b:460, a:375, b:0, a:-250`, with integer subtotals and existing `sku`/`subtotal_cents` keys. Zero and negative quantities retain current arithmetic. |
| Empty list or exhausted iterator, missing catalog | `[]`; zero catalog loads. |
| Multiple orders supplied as a single-pass iterator | Same results as a list; exactly one catalog load for a successful nonempty call. |
| First call has `a=125`, quantity 3; file changes to `a=250` before a second call | First result 375, second 750; each call loads independently. |
| Duplicate catalog rows `a=125`, then `a=200`, quantity 3 | 600, preserving last-row-wins lookup. |
| Nonempty call with missing file, malformed JSON, or unknown SKU | Existing `FileNotFoundError`, `JSONDecodeError`, or `KeyError`, respectively; no swallowed error or partial return. An empty catalog with an order still raises `KeyError`. |

These are acceptance cases to add where absent, not claims of existing test
coverage. The scratch probe verifies selected baseline cases only. Preserve
ordinary dictionary lookup failures for missing order/catalog fields rather than
adding a new error contract.

## Delivery plan and completion gate

One planned implementation stage, with no unresolved dependency for the local
change: update [report.py](../report.py), extend
[tests/test_report.py](../tests/test_report.py) for the acceptance above, and attach
measurement evidence. Keep the change, regression tests, and evidence together
as one intended commit boundary; this planning pass creates no commit.

Done means the [contributor checks](../DEVNOTES.md) pass; the contract examples
pass; successful nonempty batches load once and empty batches never load; and
repeated before/after measurements on identical inputs confirm reduced work with
unchanged outputs. Compare several order and catalog sizes, including small
batches, using the same runtime and filesystem conditions. Report timings and
variation without introducing a fragile wall-clock unit-test threshold. Operation
counts provide the deterministic acceptance of the optimization. Record any
unexpected regression before declaring the stage complete.

For the subsequent authorized implementation task: implement and test, run the
documented checks, review the resulting diff against this contract, fix findings
and rerun affected checks, then commit only within that task's authorization.
The fixture specifies no additional reviewer approval, hooks, or CI gate; do not
report those as passed. This note has been checked against the supplied request,
code, skills, and observed evidence; no independent review is claimed.

## What would justify going further

After the local change, collect representative order counts, catalog sizes,
end-to-end timings and profiles under relevant concurrency. Ask the request owner
for the latency/throughput target and workload distribution; these are needed to
judge sufficiency, but do not block this compatibility-preserving local stage.

Continue only if representative results still miss the agreed target, and choose
the next experiment from the remaining measured cost. Consider shared caching
only if loading across calls dominates and freshness/invalidation requirements
are resolved; a database only if measured access or data-management needs warrant
it; and a queue only if users accept an asynchronous contract with status,
failure, retry, and ordering semantics. Those would require separate design
decisions and authorization, not automatic follow-on stages. If the local change
meets the agreed target, stop.

Evidence can be reproduced from the repository root without bytecode writes:

```sh
TMPDIR="$PWD/scratch/report-planning" PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
TMPDIR="$PWD/scratch/report-planning" PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" scratch/report-planning/probe.py
```
