# Order report: proposed local optimization

Status: proposed, not implemented or independently reviewed. Authority: [original request](REQUEST.md), [fixture guidance](../AGENTS.md). Baseline observations: [evidence](PLANNING-EVIDENCE.md).

## At a glance

Improve large-batch reporting while preserving `summarize(orders, catalog_path)`, exact integer-cent subtotals, and order sequence. First measure the baseline, then reuse one catalog snapshot within each nonempty call. Load lazily on the first yielded order: empty inputs must still return `[]` without accessing the catalog. Keep the snapshot local to the call so a later call sees catalog changes. This removes repeated parsing at the cost of retaining the snapshot until the call ends; it introduces no persistent state. A timing benefit is plausible, not measured. Next work: [stages in NEXT.md](NEXT.md).

## Current behavior and compatibility

[report.py](../report.py) reads and parses the JSON file, builds a SKU dictionary, and repeats that work for every order. For N orders and C catalog rows, catalog construction is roughly O(N × C); one per-call load would make this roughly O(C + N), excluding file-byte size and output allocation. Output and catalog storage remain O(N + C). This is code-derived analysis, not a production profile.

The function consumes an iterable sequentially and returns a list of dictionaries containing `sku` and `subtotal_cents`. Repeated SKUs remain separate output rows. Arithmetic is direct multiplication, with no float conversion or rounding. The catalog loader keeps the last row for duplicate SKUs. It performs no schema validation; this change must not introduce validation, normalization, aggregation, sorting, or altered exceptions.

## Decisions and consequences

| Decision | Reason / alternative | Consequence | Example |
|---|---|---|---|
| Lazily load once per nonempty call | The request guarantees a fixed catalog during a batch. Unconditional loading breaks empty-input behavior; testing iterable truthiness misses empty generators. | Retain the existing loop and consume orders once; load after the first order is yielded and before looking up its SKU. Track initialization separately from catalog emptiness. | Empty iterator + missing file → `[]`, zero loads. Empty catalog + one order → `KeyError`, not a reload policy. |
| Own the snapshot within the call | A module/global/shared cache needs invalidation and can return stale prices. | A subsequent nonempty call reloads; no cache keys, TTL, synchronization or new service. | Price changes from 125 to 150 between calls; quantity 3 returns 375 then 450. |
| Defer database, cache service, and queue | No measured bottleneck, latency goal, production workload or approved infrastructure choice. A queue also needs a different interaction/failure contract. | No infrastructure work in this plan. Reconsider only against measured unmet requirements. | If file parsing is no longer significant but reporting remains slow, profile the remaining work before choosing another mechanism. |

## Acceptance and failure behavior

The following are hand-derived requirements/examples for the implementation stage; most are not existing tests.

- Catalog `a:125, b:230`; orders `(b,2), (a,3), (b,0)` → `[{"sku":"b","subtotal_cents":460},{"sku":"a","subtotal_cents":375},{"sku":"b","subtotal_cents":0}]`. Preserve order and duplicates for both lists and one-shot iterators; exactly one catalog load for a successful nonempty batch.
- `[]` or an exhausted/empty iterator with a nonexistent catalog → `[]`, zero loads. Do not preconsume/materialize the iterable merely to detect emptiness.
- Two separate nonempty calls against a catalog changed from `a:125` to `a:150`, each with `(a,3)` → 375 then 450, one load per call.
- Price `9007199254740993`, quantity 3 → integer `27021597764222979`; preserve exact arithmetic. Zero and negative quantities retain multiplication semantics (125 × -2 = -250); do not invent validation.
- Duplicate catalog rows `a:125` then `a:150`, order `(a,2)` → 300. Preserve `load_catalog` semantics.
- Nonempty input with missing file → `FileNotFoundError`; invalid JSON → `json.JSONDecodeError`; unknown SKU or empty catalog with order `a` → `KeyError('a')`. Missing required fields retain existing `KeyError` behavior. Exceptions propagate; no partial list is returned on failure, even after earlier valid orders.
- Preserve execution order: an iterator failing before its first yield raises without a catalog load; a missing file is encountered before looking up fields of the first yielded malformed order. Do not swallow iteration errors or add retries.

The fixed-catalog assumption excludes mid-batch content changes. Repeated I/O failures after a first successful read will no longer occur because subsequent reads disappear; preserving such read side effects would defeat this optimization. Mutable concurrent inputs and custom arithmetic objects are not specified; do not claim expanded support.

## Validation and remaining questions

Use compatibility tests plus load-count instrumentation for deterministic proof of eliminated work, and baseline/candidate timings on the same prepared runtime and workload. Timings are diagnostic, not a flaky unit-test threshold. Record order count, catalog size/file bytes, SKU distribution, iterations, timing spread and environment; include empty/small batches and growing large batches. Clearly label synthetic results, distinguish warm filesystem-cache runs, and avoid generalizing them to production.

Support/product should supply representative workload sizes and distributions, an agreed latency/throughput target and deployment/resource constraints. These are not blockers to the bounded local experiment. No numerical target or speedup is invented here. Profile a representative workload and establish a remaining target gap before proposing broader architecture; evaluate simpler local changes, operational costs, invalidation and API/failure semantics against that evidence.
