"""Bounded synthetic experiment; production code and tests remain untouched."""
import cProfile
import hashlib
import io
import json
import platform
import pstats
import statistics
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import report


def once_per_batch(orders, catalog_path):
    # Lazy initialization preserves summarize([], missing_path) == [].
    catalog = None
    rows = []
    for order in orders:
        if catalog is None:
            catalog = report.load_catalog(catalog_path)
        item = catalog[order['sku']]
        rows.append({'sku': order['sku'],
                     'subtotal_cents': item['price_cents'] * order['quantity']})
    return rows


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


print('Python:', sys.version, 'Platform:', platform.platform())
protected = [ROOT / 'report.py', ROOT / 'tests/test_report.py']
before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
print('Protected file SHA256 before:', json.dumps(before, sort_keys=True))
assert report.summarize([], 'missing.json') == once_per_batch([], 'missing.json') == []
print('Empty batch with missing catalog: PASS')
print('Synthetic fixed catalogs; repeated SKUs, integer prices and quantities including zero/negative.')
print('Uninstrumented timings: 3 paired trials, alternating execution order; median wall time.')
with tempfile.TemporaryDirectory(dir=Path(__file__).parent / 'tmp') as d:
    path = Path(d) / 'catalog.json'
    for catalog_size in (100, 1000):
        catalog = [{'sku': f's{i}', 'price_cents': 101 + i * 17}
                   for i in range(catalog_size)]
        path.write_text(json.dumps(catalog))
        for count in (100, 1000, 5000):
            orders = [{'sku': f's{i % catalog_size}', 'quantity': i % 9 - 2}
                      for i in range(count)]
            expected = [{'sku': o['sku'], 'subtotal_cents':
                         (101 + (i % catalog_size) * 17) * o['quantity']}
                        for i, o in enumerate(orders)]
            samples = {'current': [], 'once': []}
            for trial in range(3):
                variants = [('current', report.summarize), ('once', once_per_batch)]
                if trial % 2:
                    variants.reverse()
                for name, fn in variants:
                    start = time.perf_counter()
                    actual = fn(orders, path)
                    samples[name].append(time.perf_counter() - start)
                    assert actual == expected
            medians = {k: statistics.median(v) for k, v in samples.items()}
            print(json.dumps({'catalog_rows': catalog_size, 'catalog_bytes': path.stat().st_size,
                              'orders': count, 'seconds': samples, 'median_seconds': medians,
                              'speedup': medians['current'] / medians['once'],
                              'exact_expected_output': 'PASS'}), flush=True)
    for name, fn in [('current', report.summarize), ('once', once_per_batch)]:
        with patch.object(report, 'load_catalog', wraps=report.load_catalog) as wrapped:
            assert fn(orders, path) == expected
            print(name, 'load_catalog calls for 5000 orders:', wrapped.call_count)
    profiler = cProfile.Profile()
    profiler.runcall(report.summarize, orders, path)
    output = io.StringIO()
    pstats.Stats(profiler, stream=output).strip_dirs().sort_stats('cumulative').print_stats(18)
    print('Current implementation profile (1000 catalog rows, 5000 orders):')
    print(output.getvalue())
after = {str(p.relative_to(ROOT)): digest(p) for p in protected}
assert before == after
print('Protected file SHA256 after:', json.dumps(after, sort_keys=True))
print('Production/test files unchanged during experiment: PASS')
