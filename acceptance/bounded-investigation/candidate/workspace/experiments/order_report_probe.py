"""Bounded local probe for repeated catalog work in report.summarize."""

import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

import report


def summarize_load_once(orders, catalog_path):
    orders = iter(orders)
    first = next(orders, None)
    if first is None:
        return []
    catalog = report.load_catalog(catalog_path)
    remaining = [
        {
            "sku": order["sku"],
            "subtotal_cents": catalog[order["sku"]]["price_cents"]
            * order["quantity"],
        }
        for order in orders
    ]
    return [
        {
            "sku": first["sku"],
            "subtotal_cents": catalog[first["sku"]]["price_cents"]
            * first["quantity"],
        },
        *remaining,
    ]


def timed(function, orders, catalog_path, repeats=3):
    samples = []
    for _ in range(repeats):
        started = time.perf_counter()
        result = function(orders, catalog_path)
        samples.append(time.perf_counter() - started)
    return result, statistics.median(samples), samples


def main():
    catalog_rows = [
        {"sku": f"sku-{index}", "price_cents": 100 + index}
        for index in range(1_000)
    ]
    with tempfile.TemporaryDirectory() as directory:
        catalog_path = Path(directory) / "catalog.json"
        catalog_path.write_text(json.dumps(catalog_rows))

        print(f"python={sys.version.split()[0]} catalog_rows={len(catalog_rows)} repeats=3")
        print(
            "empty_missing_catalog_equal="
            f"{report.summarize([], catalog_path / 'missing') == summarize_load_once([], catalog_path / 'missing')}"
        )
        print("orders,current_median_s,load_once_median_s,ratio,outputs_equal")
        for count in (100, 500, 2_000):
            orders = [
                {"sku": f"sku-{index % len(catalog_rows)}", "quantity": index % 5 + 1}
                for index in range(count)
            ]
            current_result, current_time, _ = timed(
                report.summarize, orders, catalog_path
            )
            once_result, once_time, _ = timed(
                summarize_load_once, orders, catalog_path
            )
            print(
                f"{count},{current_time:.6f},{once_time:.6f},"
                f"{current_time / once_time:.1f},{current_result == once_result}"
            )

        calls = 0
        load_seconds = 0.0
        original = report.load_catalog

        def counted_load(path):
            nonlocal calls, load_seconds
            calls += 1
            started = time.perf_counter()
            loaded = original(path)
            load_seconds += time.perf_counter() - started
            return loaded

        report.load_catalog = counted_load
        try:
            probe_orders = [
                {"sku": f"sku-{index % len(catalog_rows)}", "quantity": 1}
                for index in range(500)
            ]
            started = time.perf_counter()
            report.summarize(probe_orders, catalog_path)
            total_seconds = time.perf_counter() - started
        finally:
            report.load_catalog = original
        print(
            f"instrumented_500_orders: load_calls={calls} "
            f"load_seconds={load_seconds:.6f} total_seconds={total_seconds:.6f} "
            f"load_share_pct={100 * load_seconds / total_seconds:.1f}"
        )


if __name__ == "__main__":
    main()
