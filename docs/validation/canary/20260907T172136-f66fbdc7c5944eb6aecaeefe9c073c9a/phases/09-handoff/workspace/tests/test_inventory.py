import copy
import json
import unittest
from unittest.mock import patch
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
    def assert_both_apis(self, stock, orders, expected):
        for api in (reserve, execute):
            with self.subTest(api=api.__name__):
                original_stock = copy.deepcopy(stock)
                original_orders = copy.deepcopy(orders)
                argument = orders if api is reserve else json.dumps(orders)
                result = api(stock, argument)
                self.assertEqual(result, expected)
                self.assertIsNot(result[0], stock)
                self.assertTrue(all(type(count) is int for count in result[0].values()))
                self.assertTrue(all(type(outcome["accepted"]) is bool for outcome in result[1]))
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)

    def test_rejection_and_later_exact_stock_success(self):
        self.assert_both_apis(
            {"a": 4, "b": 1},
            [
                {"id": "first", "items": [["a", 1]]},
                {"id": "reject", "items": [["a", 2], ["b", 2]]},
                {"id": "later", "items": [["a", 3], ["b", 1]]},
                {"id": "empty", "items": []},
            ],
            ({"a": 0, "b": 0}, [
                {"order_id": "first", "accepted": True},
                {"order_id": "reject", "accepted": False},
                {"order_id": "later", "accepted": True},
                {"order_id": "empty", "accepted": True},
            ]),
        )

    def test_isolated_rejection_preserves_all_stock(self):
        self.assert_both_apis(
            {"a": 4, "b": 1, "untouched": 7},
            [{"id": "reject", "items": [["a", 2], ["b", 2]]}],
            ({"a": 4, "b": 1, "untouched": 7}, [
                {"order_id": "reject", "accepted": False},
            ]),
        )

    def test_availability_uses_remaining_stock(self):
        self.assert_both_apis(
            {"a": 2},
            [{"id": "first", "items": [["a", 2]]},
             {"id": "second", "items": [["a", 1]]}],
            ({"a": 0}, [{"order_id": "first", "accepted": True},
                        {"order_id": "second", "accepted": False}]),
        )

    def test_empty_batch_and_order_through_both_apis(self):
        for stock in ({}, {"a": 2}):
            self.assert_both_apis(stock, [], (stock, []))
            self.assert_both_apis(
                stock, [{"id": "empty", "items": []}],
                (stock, [{"order_id": "empty", "accepted": True}]),
            )

    def test_validation_prevents_any_reservation(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_orders = [
            None, {}, {"id": "bad", "items": [], "extra": 1},
            {"id": 1, "items": []}, {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": [["missing", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 1]]},
        ]
        invalid_orders.extend(
            {"id": "bad", "items": [["a", quantity]]}
            for quantity in (0, -1, 1.5, "1", True, False, None)
        )
        texts = ["{", "{}", "null"] + [
            json.dumps([valid, invalid]) for invalid in invalid_orders
        ]
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
