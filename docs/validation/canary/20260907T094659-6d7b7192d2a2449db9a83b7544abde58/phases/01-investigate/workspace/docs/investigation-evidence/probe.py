"""Investigation only; synthetic fixtures and a scratch candidate, no delivery."""
import cProfile
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import pstats
import statistics
import sys
import tempfile
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import report


def once_per_batch(orders, catalog_path):
    catalog = None
    rows = []
    for order in orders:
        if catalog is None:
            catalog = report.load_catalog(catalog_path)
        item = catalog[order["sku"]]
        rows.append({"sku": order["sku"],
                     "subtotal_cents": item["price_cents"] * order["quantity"]})
    return rows


def outcome(fn, orders, path):
    try:
        return ("result", fn(iter(orders), path))
    except Exception as exc:
        return (type(exc).__name__, str(exc))


print("Python:", platform.python_version(), "platform:", platform.platform())
print("Method: perf_counter wall seconds; 3 repeats; alternate execution order;")
print("synthetic local JSON, exact full-output equality each run; median reported.")
for path in [ROOT / "report.py", ROOT / "tests/test_report.py"]:
    print("SHA256", path.relative_to(ROOT), hashlib.sha256(path.read_bytes()).hexdigest())

with tempfile.TemporaryDirectory(dir=ROOT / ".investigation-tmp") as directory:
    path = Path(directory) / "catalog.json"
    for catalog_size in (100, 1000):
        catalog = [{"sku": f"sku-{i}", "price_cents": 125 + i}
                   for i in range(catalog_size)]
        path.write_text(json.dumps(catalog))
        for batch_size in (100, 1000, 5000):
            orders = [{"sku": f"sku-{i % catalog_size}", "quantity": i % 7}
                      for i in range(batch_size)]
            samples = {"current": [], "scratch": []}
            functions = {"current": report.summarize, "scratch": once_per_batch}
            for repeat in range(3):
                results = {}
                for name in (("current", "scratch") if repeat % 2 == 0
                             else ("scratch", "current")):
                    start = time.perf_counter()
                    results[name] = functions[name](orders, path)
                    samples[name].append(time.perf_counter() - start)
                assert results["current"] == results["scratch"]
                assert results["current"] == [
                    {"sku": o["sku"], "subtotal_cents":
                     (125 + i % catalog_size) * o["quantity"]}
                    for i, o in enumerate(orders)]
            medians = {k: statistics.median(v) for k, v in samples.items()}
            print(json.dumps({"catalog_rows": catalog_size, "orders": batch_size,
                              "catalog_bytes": path.stat().st_size,
                              "seconds": samples, "median_seconds": medians,
                              "ratio_current_to_scratch": medians["current"] / medians["scratch"]}))

    orders = [{"sku": f"sku-{i}", "quantity": 3} for i in range(1000)]
    for name, fn in (("current", report.summarize), ("scratch", once_per_batch)):
        with patch.object(report, "load_catalog", wraps=report.load_catalog) as loader:
            fn(orders, path)
            print("load_catalog calls:", name, loader.call_count, "for 1000 orders")
        profile = cProfile.Profile()
        profile.runcall(fn, orders, path)
        stream = io.StringIO()
        pstats.Stats(profile, stream=stream).strip_dirs().sort_stats("cumulative").print_stats(12)
        print("PROFILE", name, stream.getvalue())

    cases = [
        ("empty missing catalog", [], Path(directory) / "missing.json"),
        ("missing catalog", [{"sku": "sku-0", "quantity": 1}], Path(directory) / "missing.json"),
        ("missing sku", [{"sku": "absent", "quantity": 1}], path),
        ("missing quantity", [{"sku": "sku-0"}], path),
        ("duplicates, signed and zero quantities", [
            {"sku": "sku-1", "quantity": 0},
            {"sku": "sku-0", "quantity": -2},
            {"sku": "sku-1", "quantity": 5}], path),
    ]
    for label, orders, source in cases:
        old, new = outcome(report.summarize, orders, source), outcome(once_per_batch, orders, source)
        assert old == new, (label, old, new)
        print("compatibility PASS:", label, old)
    path.write_text("invalid json")
    orders = [{"sku": "sku-0", "quantity": 1}]
    assert outcome(report.summarize, orders, path) == outcome(once_per_batch, orders, path)
    print("compatibility PASS: malformed JSON")
print("All experiment assertions passed.")
