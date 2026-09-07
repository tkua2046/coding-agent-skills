"""Synthetic baseline probe; runs existing report code without modifying it."""
import cProfile
import io
import json
from pathlib import Path
import pstats
import sys
import tempfile
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import report

print(sys.version)
print("Synthetic warm local filesystem; no production representativeness claimed.")
with tempfile.TemporaryDirectory() as directory:
    catalog = Path(directory) / "catalog.json"
    catalog.write_text(json.dumps([
        {"sku": str(i), "price_cents": 125 + i} for i in range(1000)
    ]))
    for size in (0, 1, 100, 1000):
        orders = [{"sku": str(i % 1000), "quantity": 3} for i in range(size)]
        expected = [{"sku": str(i % 1000), "subtotal_cents": (125 + i % 1000) * 3}
                    for i in range(size)]
        started = time.perf_counter()
        with patch.object(report, "load_catalog", wraps=report.load_catalog) as loader:
            actual = report.summarize(orders, catalog)
            loads = loader.call_count
        assert actual == expected
        print(f"orders={size}, catalog_rows=1000, loads={loads}, elapsed_s={time.perf_counter()-started:.6f}")
    profiler = cProfile.Profile()
    profiler.runcall(report.summarize, orders, catalog)
    output = io.StringIO()
    pstats.Stats(profiler, stream=output).strip_dirs().sort_stats("cumulative").print_stats(12)
    print(output.getvalue())
    assert report.summarize(iter([]), "missing.json") == []
    catalog.write_text('[{"sku":"a","price_cents":125},{"sku":"a","price_cents":200}]')
    assert report.summarize(iter([{"sku":"a","quantity":3}]), catalog) == [
        {"sku":"a","subtotal_cents":600}]
    catalog.write_text('[{"sku":"a","price_cents":250}]')
    assert report.summarize([{"sku":"a","quantity":3}], catalog) == [
        {"sku":"a","subtotal_cents":750}]
    for label, orders, path in (
        ("missing catalog", [{"sku":"a","quantity":1}], "missing.json"),
        ("unknown sku", [{"sku":"unknown","quantity":1}], catalog),
    ):
        try:
            report.summarize(orders, path)
        except Exception as error:
            print(f"{label}: {type(error).__name__}: {error}")
        else:
            raise AssertionError(label)
    catalog.write_text('{')
    try:
        report.summarize([{"sku":"a","quantity":1}], catalog)
    except json.JSONDecodeError:
        print("invalid JSON: JSONDecodeError")
    else:
        raise AssertionError("invalid JSON")
    print("Compatibility probes passed: empty iterator, single-pass iterator, duplicate SKU last wins, freshness between calls.")
