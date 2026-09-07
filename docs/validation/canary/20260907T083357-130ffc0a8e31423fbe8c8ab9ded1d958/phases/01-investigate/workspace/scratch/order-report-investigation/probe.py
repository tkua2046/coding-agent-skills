"""Bounded, stdlib-only experiment; run from repository root."""
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import report


def batch_local(orders, catalog_path):
    # Lazy initialization retains summarize([], missing_path) == [].
    catalog = None
    rows = []
    for order in orders:
        if catalog is None:
            catalog = report.load_catalog(catalog_path)
        item = catalog[order['sku']]
        rows.append({'sku': order['sku'],
                     'subtotal_cents': item['price_cents'] * order['quantity']})
    return rows


def fingerprint():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT / 'report.py', *sorted((ROOT / 'tests').rglob('*.py'))]}


before = fingerprint()
print('Python:', sys.version, 'Platform:', platform.platform())
print('Source/test SHA256 before:', json.dumps(before, sort_keys=True))
print('Synthetic fixed catalog, deterministic orders; 3 repetitions, alternating implementation order.')
print('Each case is warmed by correctness comparison. Times exclude fixture creation and profiling.')
with tempfile.TemporaryDirectory(dir=ROOT / 'scratch/order-report-investigation') as directory:
    path = Path(directory) / 'catalog.json'
    print('catalog_rows,orders,bytes,original_seconds,candidate_seconds,median_speedup')
    for catalog_size, count in [(1000, 100), (1000, 1000), (1000, 3000), (100, 1000), (3000, 1000)]:
        path.write_text(json.dumps([{'sku': f's{i}', 'price_cents': 101 + i}
                                   for i in range(catalog_size)]))
        orders = [{'sku': f's{i % catalog_size}', 'quantity': i % 7}
                  for i in range(count)]
        assert report.summarize(orders, path) == batch_local(orders, path)
        timings = {'original': [], 'candidate': []}
        for repeat in range(3):
            funcs = [('original', report.summarize), ('candidate', batch_local)]
            if repeat % 2:
                funcs.reverse()
            for name, func in funcs:
                start = time.perf_counter()
                func(orders, path)
                timings[name].append(time.perf_counter() - start)
        print(catalog_size, count, path.stat().st_size,
              timings['original'], timings['candidate'],
              statistics.median(timings['original']) / statistics.median(timings['candidate']),
              sep=',', flush=True)

    path.write_text(json.dumps([{'sku': f's{i}', 'price_cents': 101 + i} for i in range(1000)]))
    orders = [{'sku': f's{i % 1000}', 'quantity': i % 7} for i in range(1000)]
    for name, func in [('original', report.summarize), ('candidate', batch_local)]:
        with patch.object(report, 'load_catalog', wraps=report.load_catalog) as loader:
            func(orders, path)
            print(name, 'load_catalog calls for 1000 orders:', loader.call_count)
        profile = cProfile.Profile()
        profile.runcall(func, orders, path)
        stream = io.StringIO()
        pstats.Stats(profile, stream=stream).strip_dirs().sort_stats('cumulative').print_stats(12)
        print(name, 'profile:', stream.getvalue())

    path.write_text(json.dumps([{'sku': 'a', 'price_cents': 125},
                                {'sku': 'b', 'price_cents': 999},
                                {'sku': 'a', 'price_cents': 127}]))
    cases = [[], [{'sku': 'b', 'quantity': 0}, {'sku': 'a', 'quantity': -2},
                  {'sku': 'b', 'quantity': 3}, {'sku': 'a', 'quantity': 10**18}]]
    for orders in cases:
        assert report.summarize(orders, path) == batch_local(orders, path)
        assert report.summarize(iter(orders), path) == batch_local(iter(orders), path)
    print('Equality: all timed cases; empty, order sequence, repeated SKU, zero/negative/large integer quantity, duplicate catalog SKU, generator input: PASS')
    for func in [report.summarize, batch_local]:
        with patch.object(report, 'load_catalog', wraps=report.load_catalog) as loader:
            assert func([], Path(directory) / 'missing.json') == []
            assert loader.call_count == 0
    print('Empty batch with missing path: [] and zero catalog loads in both: PASS')
    def outcome(func, orders, source):
        try:
            return ('value', func(orders, source))
        except Exception as error:
            return (type(error).__name__, str(error))
    for orders, source in [([{'sku': 'absent', 'quantity': 1}], path),
                           ([{'sku': 'a', 'quantity': 1}], Path(directory) / 'missing.json')]:
        assert outcome(report.summarize, orders, source) == outcome(batch_local, orders, source)
    path.write_text('{invalid')
    assert outcome(report.summarize, [{'sku': 'a', 'quantity': 1}], path) == outcome(batch_local, [{'sku': 'a', 'quantity': 1}], path)
    print('Missing SKU, missing file, malformed JSON exception type/message equality: PASS')
assert fingerprint() == before
print('Source/test SHA256 unchanged: PASS')
