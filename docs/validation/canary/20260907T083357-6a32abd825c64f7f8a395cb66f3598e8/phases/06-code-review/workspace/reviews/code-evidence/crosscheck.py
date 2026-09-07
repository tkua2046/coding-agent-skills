"""Bounded independent review probe; run from fixture root with bytecode disabled."""
import copy
import itertools
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from inventory import reserve
from batch import execute

vectors = list(itertools.product(range(3), repeat=2))
cases = 0
for quantities in vectors:
    stock = dict(zip(('a', 'b'), quantities))
    for requests in itertools.product(vectors, repeat=3):
        orders = []
        for i, request in enumerate(requests):
            items = [[sku, q] for sku, q in zip(('a', 'b'), request) if q]
            orders.append({'id': str(i), 'items': items if i % 2 else items[::-1]})
        original = copy.deepcopy((stock, orders))
        expected_stock = dict(stock)
        expected_outcomes = []
        for order in orders:
            trial = dict(expected_stock)
            for sku, q in order['items']:
                trial[sku] -= q
            accepted = min(trial.values()) >= 0
            if accepted:
                expected_stock = trial
            expected_outcomes.append({'order_id': order['id'], 'accepted': accepted})
        for result in (reserve(stock, orders), execute(stock, json.dumps(orders))):
            assert result == (expected_stock, expected_outcomes), (original, result)
            assert result[0] is not stock
            assert all(type(q) is int and q >= 0 for q in result[0].values())
            assert all(type(o['accepted']) is bool for o in result[1])
        assert (stock, orders) == original
        cases += 1
print(f'PASS: {cases} three-order batches; {cases * 2} API evaluations against tentative-copy reference; stock 0..2, requests absent/1/2 per SKU, alternating item order, deep immutability and exact result types.')
