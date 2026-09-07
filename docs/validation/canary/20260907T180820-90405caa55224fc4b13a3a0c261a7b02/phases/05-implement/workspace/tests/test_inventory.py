import copy
import json
import unittest
from unittest.mock import patch
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
    def test_whole_order_rejection_and_sequential_stock(self):
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            for rejected_items in ([["a", 2], ["b", 2]], [["b", 2], ["a", 2]]):
                with self.subTest(api=api, rejected_items=rejected_items):
                    stock = {"a": 3, "b": 1, "untouched": 7}
                    orders = [
                        {"id": "rejected", "items": rejected_items},
                        {"id": "exact", "items": [["a", 3], ["b", 1]]},
                        {"id": "depleted", "items": [["a", 1]]},
                        {"id": "empty", "items": []},
                    ]
                    original_stock = stock.copy()
                    original_orders = copy.deepcopy(orders)
                    remaining, outcomes = api(stock, orders)
                    self.assertEqual(remaining, {"a": 0, "b": 0, "untouched": 7})
                    self.assertEqual(outcomes, [
                        {"order_id": "rejected", "accepted": False},
                        {"order_id": "exact", "accepted": True},
                        {"order_id": "depleted", "accepted": False},
                        {"order_id": "empty", "accepted": True},
                    ])
                    self.assertTrue(all(type(outcome["accepted"]) is bool for outcome in outcomes))
                    self.assertTrue(all(type(count) is int for count in remaining.values()))
                    self.assertIsNot(remaining, stock)
                    self.assertEqual(stock, original_stock)
                    self.assertEqual(orders, original_orders)

    def test_empty_orders_and_batches_through_both_apis(self):
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            for stock in ({}, {"a": 2}):
                for orders, expected in (
                    ([], []),
                    ([{"id": "empty", "items": []}], [{"order_id": "empty", "accepted": True}]),
                ):
                    with self.subTest(api=api, stock=stock, orders=orders):
                        remaining, outcomes = api(stock, orders)
                        self.assertEqual((remaining, outcomes), (stock, expected))
                        self.assertIsNot(remaining, stock)

    def test_adapter_preserves_validation_before_engine_execution(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_orders = [
            None,
            {"id": "bad"},
            {"id": "bad", "items": [], "extra": True},
            {"id": 1, "items": []},
            {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": [["unknown", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 2]]},
        ] + [{"id": "bad", "items": [["a", quantity]]}
             for quantity in (0, -1, 1.5, True, "1", None)]
        texts = ["{", "{}", "null"] + [json.dumps([valid, order]) for order in invalid_orders]
        for text in texts:
            with self.subTest(text=text):
                stock = {"a": 4}
                with patch("batch.reserve") as engine:
                    with self.assertRaises(ValueError):
                        execute(stock, text)
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
