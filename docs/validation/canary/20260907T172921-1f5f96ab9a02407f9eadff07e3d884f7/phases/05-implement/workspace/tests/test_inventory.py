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


class WholeOrderTests(unittest.TestCase):
    def assert_both_apis(self, stock, orders, expected_stock, expected_outcomes):
        for api in (reserve, execute):
            with self.subTest(api=api.__name__):
                original_stock = copy.deepcopy(stock)
                original_orders = copy.deepcopy(orders)
                argument = orders if api is reserve else json.dumps(orders)
                remaining, outcomes = api(stock, argument)
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)
                self.assertIsNot(remaining, stock)
                self.assertEqual(remaining, expected_stock)
                self.assertEqual(outcomes, expected_outcomes)
                for quantity in remaining.values():
                    self.assertIs(type(quantity), int)
                    self.assertGreaterEqual(quantity, 0)
                for outcome in outcomes:
                    self.assertIs(type(outcome["accepted"]), bool)

    def test_mixed_batch_and_rejection_prefix(self):
        orders = [
            {"id": "first", "items": [["a", 1]]},
            {"id": "reject", "items": [["a", 2], ["b", 3]]},
            {"id": "later", "items": [["a", 3], ["b", 2]]},
            {"id": "empty", "items": []},
        ]
        outcomes = [
            {"order_id": "first", "accepted": True},
            {"order_id": "reject", "accepted": False},
            {"order_id": "later", "accepted": True},
            {"order_id": "empty", "accepted": True},
        ]
        self.assert_both_apis({"a": 4, "b": 2}, orders[:2],
                              {"a": 3, "b": 2}, outcomes[:2])
        self.assert_both_apis({"a": 4, "b": 2}, orders,
                              {"a": 0, "b": 0}, outcomes)

    def test_shortage_uses_remaining_stock(self):
        self.assert_both_apis(
            {"a": 4},
            [{"id": "first", "items": [["a", 1]]},
             {"id": "reject", "items": [["a", 4]]},
             {"id": "later", "items": [["a", 3]]}],
            {"a": 0},
            [{"order_id": "first", "accepted": True},
             {"order_id": "reject", "accepted": False},
             {"order_id": "later", "accepted": True}],
        )

    def test_single_item_shortage(self):
        for available in (0, 2):
            with self.subTest(available=available):
                self.assert_both_apis(
                    {"a": available, "b": 5},
                    [{"id": "reject", "items": [["a", 3]]}],
                    {"a": available, "b": 5},
                    [{"order_id": "reject", "accepted": False}],
                )

    def test_empty_order_and_batch(self):
        self.assert_both_apis({"a": 2}, [], {"a": 2}, [])
        self.assert_both_apis({}, [{"id": "empty", "items": []}], {},
                              [{"order_id": "empty", "accepted": True}])

    def test_adapter_validates_entire_payload_before_reserving(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_payloads = [
            {},
            [valid, []],
            [valid, {"id": "second"}],
            [valid, {"id": "first", "items": []}],
            [valid, {"id": "second", "items": {}}],
            [valid, {"id": "second", "items": [["a"]]}],
        ]
        invalid_payloads.extend(
            [valid, {"id": "second", "items": [["a", quantity]]}]
            for quantity in (0, -1, 1.5, "1", True)
        )
        for text in ["["] + [json.dumps(value) for value in invalid_payloads]:
            with self.subTest(text=text):
                stock = {"a": 4}
                with patch("batch.reserve") as engine:
                    with self.assertRaises(ValueError):
                        execute(stock, text)
                    engine.assert_not_called()
                self.assertEqual(stock, {"a": 4})
