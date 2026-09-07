import copy
import json
import unittest
from unittest.mock import patch
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
    def assert_both_apis(self, stock, orders, expected):
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            with self.subTest(api=api):
                stock_before = copy.deepcopy(stock)
                orders_before = copy.deepcopy(orders)
                remaining, outcomes = api(stock, orders)
                self.assertEqual((remaining, outcomes), expected)
                self.assertEqual(stock, stock_before)
                self.assertEqual(orders, orders_before)
                self.assertIsNot(remaining, stock)
                self.assertTrue(all(type(count) is int for count in remaining.values()))
                self.assertTrue(all(type(outcome["accepted"]) is bool for outcome in outcomes))

    def test_short_last_item_rejects_without_any_deduction(self):
        self.assert_both_apis(
            {"a": 3, "b": 1},
            [{"id": "reject", "items": [["a", 2], ["b", 2]]}],
            ({"a": 3, "b": 1}, [{"order_id": "reject", "accepted": False}]),
        )

    def test_continuation_depletion_and_empty_order(self):
        self.assert_both_apis(
            {"a": 3, "b": 1},
            [
                {"id": "reject", "items": [["a", 2], ["b", 2]]},
                {"id": "take", "items": [["a", 3], ["b", 1]]},
                {"id": "later", "items": [["a", 1]]},
                {"id": "empty", "items": []},
            ],
            ({"a": 0, "b": 0}, [
                {"order_id": "reject", "accepted": False},
                {"order_id": "take", "accepted": True},
                {"order_id": "later", "accepted": False},
                {"order_id": "empty", "accepted": True},
            ]),
        )

    def test_empty_batch_both_apis(self):
        self.assert_both_apis({"a": 2}, [], ({"a": 2}, []))

    def test_json_validation_before_reservation(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_batches = [
            {},
            [None],
            [{"id": "o"}],
            [{"id": "o", "items": [], "extra": 1}],
            [{"id": 1, "items": []}],
            [valid, valid],
            [{"id": "o", "items": {}}],
            [{"id": "o", "items": [["a"]]}],
            [{"id": "o", "items": ["a"]}],
            [{"id": "o", "items": [["missing", 1]]}],
            [{"id": "o", "items": [["a", 1], ["a", 2]]}],
        ]
        invalid_batches.extend(
            [valid, {"id": "bad", "items": [["a", quantity]]}]
            for quantity in (0, -1, 1.5, True, "1", None)
        )
        for payload in ["{"] + [json.dumps(batch) for batch in invalid_batches]:
            with self.subTest(payload=payload):
                stock = {"a": 4}
                with patch("batch.reserve") as engine:
                    with self.assertRaises(ValueError):
                        execute(stock, payload)
                    engine.assert_not_called()
                self.assertEqual(stock, {"a": 4})

    def test_success_and_input_preservation(self):
        stock={"a":4,"b":2}
        orders=[{"id":"o1","items":[["a",2],["b",1]]}]
        self.assertEqual(reserve(stock,orders),({"a":2,"b":1},[{"order_id":"o1","accepted":True}]))
        self.assertEqual(stock,{"a":4,"b":2})
    def test_empty(self):
        self.assertEqual(reserve({"a":2},[]),({"a":2},[]))
    def test_adapter(self):
        self.assertEqual(execute({"a":4},'[{"id":"o","items":[["a",1]]}]'),({"a":3},[{"order_id":"o","accepted":True}]))
    def test_unknown_sku(self):
        with self.assertRaises(ValueError):
            execute({"a":4},'[{"id":"o","items":[["missing",1]]}]')
    def test_duplicate_sku(self):
        with self.assertRaises(ValueError):
            execute({"a":4},'[{"id":"o","items":[["a",1],["a",2]]}]')
    def test_bad_quantity(self):
        with self.assertRaises(ValueError):
            execute({"a":4},'[{"id":"o","items":[["a",true]]}]')
