"""Independent bounded review experiment; run from the project root."""
import copy
import itertools
import json
import sys
sys.path.insert(0, '.')
from inventory import reserve
from batch import execute

options = [[]] + [[[sku, n]] for sku in ('a', 'b') for n in (1, 2)]
options += [[[s, n], [t, m]] for s, t in [('a', 'b'), ('b', 'a')] for n in (1, 2) for m in (1, 2)]
cases = 0
for a, b in itertools.product(range(3), repeat=2):
    for length in range(4):
        for items in itertools.product(options, repeat=length):
            stock = {'a': a, 'b': b, 'unused': 7}
            orders = [{'id': str(i), 'items': copy.deepcopy(item)} for i, item in enumerate(items)]
            snapshot = copy.deepcopy((stock, orders))
            expected_stock = dict(stock)
            expected_outcomes = []
            for order in orders:
                proposed = dict(expected_stock)
                for sku, quantity in order['items']:
                    proposed[sku] -= quantity
                accepted = min(proposed.values()) >= 0
                if accepted:
                    expected_stock = proposed
                expected_outcomes.append({'order_id': order['id'], 'accepted': accepted})
            for result in (reserve(stock, orders), execute(stock, json.dumps(orders))):
                assert result == (expected_stock, expected_outcomes), (snapshot, result)
                assert result[0] is not stock
                assert all(type(n) is int for n in result[0].values())
                assert all(type(o['accepted']) is bool for o in result[1])
                assert (stock, orders) == snapshot
            cases += 1
print(f'PASS: {cases} cases, {cases * 2} API calls; lengths 0..3; two SKUs, stock 0..2, quantities 1..2, both item orders, unused stock retained; independent tentative-subtraction oracle and deep input/type checks.')
