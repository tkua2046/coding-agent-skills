import copy
import json
import unittest
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


class WholeOrderTests(unittest.TestCase):
    def assert_both_apis(self, stock, orders, expected_stock, expected_outcomes):
        for api in ("reserve", "execute"):
            with self.subTest(api=api):
                original_stock = copy.deepcopy(stock)
                original_orders = copy.deepcopy(orders)
                text = json.dumps(orders)
                remaining, outcomes = (
                    reserve(stock, orders) if api == "reserve" else execute(stock, text)
                )
                self.assertEqual(remaining, expected_stock)
                self.assertEqual(outcomes, expected_outcomes)
                self.assertIsNot(remaining, stock)
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)
                self.assertTrue(all(type(value) is int for value in remaining.values()))
                self.assertTrue(all(type(row["accepted"]) is bool for row in outcomes))

    def test_rejection_preserves_all_items_and_later_orders_continue(self):
        self.assert_both_apis(
            {"a": 4, "b": 1},
            [
                {"id": "first", "items": [["a", 1]]},
                {"id": "reject", "items": [["a", 2], ["b", 2]]},
                {"id": "later", "items": [["a", 3], ["b", 1]]},
                {"id": "empty", "items": []},
            ],
            {"a": 0, "b": 0},
            [
                {"order_id": "first", "accepted": True},
                {"order_id": "reject", "accepted": False},
                {"order_id": "later", "accepted": True},
                {"order_id": "empty", "accepted": True},
            ],
        )

    def test_rejection_alone_leaves_stock_unchanged(self):
        self.assert_both_apis(
            {"a": 4, "b": 1},
            [{"id": "reject", "items": [["a", 2], ["b", 2]]}],
            {"a": 4, "b": 1},
            [{"order_id": "reject", "accepted": False}],
        )

    def test_availability_uses_stock_after_earlier_success(self):
        self.assert_both_apis(
            {"a": 3},
            [
                {"id": "first", "items": [["a", 2]]},
                {"id": "reject", "items": [["a", 2]]},
                {"id": "last", "items": [["a", 1]]},
            ],
            {"a": 0},
            [
                {"order_id": "first", "accepted": True},
                {"order_id": "reject", "accepted": False},
                {"order_id": "last", "accepted": True},
            ],
        )

    def test_zero_stock_rejects_but_empty_order_succeeds(self):
        self.assert_both_apis(
            {"a": 0},
            [{"id": "reject", "items": [["a", 1]]}, {"id": "empty", "items": []}],
            {"a": 0},
            [
                {"order_id": "reject", "accepted": False},
                {"order_id": "empty", "accepted": True},
            ],
        )

    def test_empty_batch_returns_copy(self):
        self.assert_both_apis({"a": 2}, [], {"a": 2}, [])

    def test_adapter_validates_later_orders_before_reserving(self):
        stock = {"a": 1}
        text = '[{"id":"reject","items":[["a",2]]},{"id":"bad","items":[["a",0]]}]'
        with patch("batch.reserve") as engine:
            with self.assertRaisesRegex(ValueError, "quantity must be a positive integer"):
                execute(stock, text)
            engine.assert_not_called()
        self.assertEqual(stock, {"a": 1})
