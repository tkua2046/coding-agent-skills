"""Bounded benchmark for the catalog-loading hypothesis; not production code."""

import json
import statistics
import sys
import time
from pathlib import Path

from report import load_catalog, summarize


CATALOG_SIZE = 1_000
ORDER_COUNTS = (10, 100, 1_000)
REPEATS = 5


def summarize_preloaded(orders, catalog_path):
    """Experimental equivalent when the catalog is fixed for the whole batch."""
    catalog = load_catalog(catalog_path)
    return [
        {
            "sku": order["sku"],
            "subtotal_cents": catalog[order["sku"]]["price_cents"]
            * order["quantity"],
        }
        for order in orders
    ]


def median_seconds(callable_):
    samples = []
    for _ in range(REPEATS):
        started = time.perf_counter()
        callable_()
        samples.append(time.perf_counter() - started)
    return statistics.median(samples)


def main(work_dir):
    work_dir.mkdir(parents=True, exist_ok=True)
    catalog_path = work_dir / "benchmark_catalog.json"
    catalog_path.write_text(
        json.dumps(
            [
                {"sku": f"sku-{index}", "price_cents": 100 + index}
                for index in range(CATALOG_SIZE)
            ]
        )
    )

    print(
        f"catalog_rows={CATALOG_SIZE} repeats={REPEATS} "
        "statistic=median_wall_seconds"
    )
    print("orders baseline_s preloaded_s speedup outputs_equal")
    for count in ORDER_COUNTS:
        orders = [
            {"sku": f"sku-{index % CATALOG_SIZE}", "quantity": index % 5 + 1}
            for index in range(count)
        ]
        expected = summarize(orders, catalog_path)
        candidate = summarize_preloaded(orders, catalog_path)
        baseline = median_seconds(lambda: summarize(orders, catalog_path))
        preloaded = median_seconds(lambda: summarize_preloaded(orders, catalog_path))
        print(
            f"{count} {baseline:.6f} {preloaded:.6f} "
            f"{baseline / preloaded:.1f}x {expected == candidate}"
        )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
