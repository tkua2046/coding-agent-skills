import unittest
import copy
import json
from unittest.mock import patch
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
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

    def assert_both_apis(self, stock, orders, expected):
        original_stock = copy.deepcopy(stock)
        original_orders = copy.deepcopy(orders)
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            with self.subTest(api=api):
                remaining, outcomes = api(stock, orders)
                self.assertEqual((remaining, outcomes), expected)
                self.assertIsNot(remaining, stock)
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)
                self.assertTrue(all(type(value) is int and value >= 0 for value in remaining.values()))
                self.assertTrue(all(type(outcome["accepted"]) is bool for outcome in outcomes))

    def test_late_shortage_rejects_whole_order_and_continues(self):
        self.assert_both_apis(
            {"a": 4, "b": 1},
            [{"id": "reject", "items": [["a", 3], ["b", 2]]},
             {"id": "later", "items": [["a", 4], ["b", 1]]},
             {"id": "empty", "items": []}],
            ({"a": 0, "b": 0}, [{"order_id": "reject", "accepted": False},
                                {"order_id": "later", "accepted": True},
                                {"order_id": "empty", "accepted": True}]),
        )

    def test_rejection_preserves_prior_success_and_remaining_stock(self):
        self.assert_both_apis(
            {"a": 2},
            [{"id": "first", "items": [["a", 1]]},
             {"id": "reject", "items": [["a", 2]]},
             {"id": "last", "items": [["a", 1]]}],
            ({"a": 0}, [{"order_id": "first", "accepted": True},
                        {"order_id": "reject", "accepted": False},
                        {"order_id": "last", "accepted": True}]),
        )

    def test_rejection_alone_leaves_every_quantity_unchanged(self):
        self.assert_both_apis(
            {"a": 4, "b": 1, "unused": 9},
            [{"id": "reject", "items": [["a", 3], ["b", 2]]}],
            ({"a": 4, "b": 1, "unused": 9}, [{"order_id": "reject", "accepted": False}]),
        )

    def test_zero_stock_rejects(self):
        self.assert_both_apis(
            {"a": 0}, [{"id": "reject", "items": [["a", 1]]}],
            ({"a": 0}, [{"order_id": "reject", "accepted": False}]),
        )

    def test_empty_order_on_empty_stock(self):
        self.assert_both_apis(
            {}, [{"id": "empty", "items": []}],
            ({}, [{"order_id": "empty", "accepted": True}]),
        )

    def test_empty_batch_both_apis(self):
        self.assert_both_apis({"a": 2}, [], ({"a": 2}, []))

    def test_adapter_validation_finishes_before_execution(self):
        invalid_orders = [
            None, {}, {"id": "bad", "items": [], "extra": 1},
            {"id": 1, "items": []}, {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": ["a"]},
            {"id": "bad", "items": [["missing", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 1]]},
        ]
        invalid_orders.extend(
            {"id": "bad", "items": [["a", quantity]]}
            for quantity in (0, -1, 1.5, True, False, "1", None)
        )
        texts = ["{", "{}", "null"] + [
            json.dumps([{"id": "first", "items": [["a", 1]]}, invalid])
            for invalid in invalid_orders
        ]
        for text in texts:
            with self.subTest(text=text):
                stock = {"a": 4}
                with patch("batch.reserve") as engine:
                    with self.assertRaises(ValueError):
                        execute(stock, text)
                    engine.assert_not_called()
                self.assertEqual(stock, {"a": 4})
