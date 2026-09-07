"""Synthetic baseline probe; exercises the existing report without changing it."""
import cProfile
import io
import json
import pstats
import statistics
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import report

print('Runtime:', sys.version)
print('Synthetic local workload; not a production trace or latency target.')
with tempfile.TemporaryDirectory(dir=ROOT / 'scratch') as directory:
    path = Path(directory) / 'catalog.json'
    catalog = [{'sku': f's{i}', 'price_cents': 125 + i} for i in range(1000)]
    path.write_text(json.dumps(catalog))
    print('Catalog rows:', len(catalog), 'bytes:', path.stat().st_size)
    for count in (0, 1, 100, 1000):
        orders = [{'sku': f's{i % 1000}', 'quantity': 3} for i in range(count)]
        expected = [{'sku': f's{i % 1000}', 'subtotal_cents': (125 + i % 1000) * 3}
                    for i in range(count)]
        elapsed = []
        for _ in range(3):
            start = time.perf_counter()
            actual = report.summarize(orders, path)
            elapsed.append(time.perf_counter() - start)
            assert actual == expected
        profile = cProfile.Profile()
        profile.runcall(report.summarize, orders, path)
        stats = pstats.Stats(profile)
        loads = sum(value[1] for key, value in stats.stats.items()
                    if key[2] == 'load_catalog')
        print(f'orders={count} load_catalog_calls={loads} median_seconds={statistics.median(elapsed):.6f} exact_outputs=pass')
        if count == 1000:
            stream = io.StringIO()
            pstats.Stats(profile, stream=stream).sort_stats('cumulative').print_stats(12)
            print(stream.getvalue())
    path.write_text(json.dumps([{'sku': 'a', 'price_cents': 125}]))
    assert report.summarize(iter([{'sku': 'a', 'quantity': 3}]), path) == [{'sku': 'a', 'subtotal_cents': 375}]
    path.write_text(json.dumps([{'sku': 'a', 'price_cents': 200}]))
    assert report.summarize([{'sku': 'a', 'quantity': 3}], path) == [{'sku': 'a', 'subtotal_cents': 600}]
    assert report.summarize(iter([]), Path(directory) / 'missing.json') == []
    print('Iterator input, refresh between calls, empty iterator with missing path: pass')
