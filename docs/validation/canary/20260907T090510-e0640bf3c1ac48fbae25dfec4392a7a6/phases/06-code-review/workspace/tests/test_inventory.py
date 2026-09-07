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

    def test_whole_order_reservation_through_both_apis(self):
        cases = [
            ("late shortage", {"a": 4, "b": 1},
             [("reject", [["a", 3], ["b", 2]]), ("later", [["a", 2]])],
             {"a": 2, "b": 1}, [False, True]),
            ("early shortage", {"a": 4, "b": 1},
             [("reject", [["b", 2], ["a", 3]]), ("later", [["a", 2]])],
             {"a": 2, "b": 1}, [False, True]),
            ("current stock and exact depletion", {"a": 4, "b": 1},
             [("first", [["a", 3]]), ("reject", [["a", 2], ["b", 1]]),
              ("last", [["a", 1], ["b", 1]])],
             {"a": 0, "b": 0}, [True, False, True]),
            ("zero stock and empty order", {"a": 0},
             [("reject", [["a", 1]]), ("empty", [])],
             {"a": 0}, [False, True]),
            ("empty batch", {"a": 2}, [], {"a": 2}, []),
            ("successful multi-item order", {"a": 4, "b": 2},
             [("success", [["a", 2], ["b", 1]])],
             {"a": 2, "b": 1}, [True]),
            ("rejection alone preserves every item", {"a": 4, "b": 1},
             [("reject", [["a", 3], ["b", 2]])],
             {"a": 4, "b": 1}, [False]),
        ]
        for name, initial_stock, requests, expected_stock, accepted in cases:
            for api in (reserve, execute):
                with self.subTest(case=name, api=api.__name__):
                    stock = copy.deepcopy(initial_stock)
                    orders = [{"id": order_id, "items": copy.deepcopy(items)}
                              for order_id, items in requests]
                    before_stock, before_orders = copy.deepcopy((stock, orders))
                    argument = orders if api is reserve else json.dumps(orders)
                    remaining, outcomes = api(stock, argument)
                    self.assertEqual(remaining, expected_stock)
                    self.assertEqual(outcomes, [
                        {"order_id": order_id, "accepted": success}
                        for (order_id, _), success in zip(requests, accepted)
                    ])
                    self.assertTrue(all(type(value) is int and value >= 0
                                        for value in remaining.values()))
                    self.assertTrue(all(type(row["accepted"]) is bool
                                        for row in outcomes))
                    self.assertIsNot(remaining, stock)
                    self.assertEqual(stock, before_stock)
                    self.assertEqual(orders, before_orders)

    def test_json_validation_precedes_engine_execution(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_orders = [
            None,
            {"id": "bad"},
            {"id": "bad", "items": [], "extra": 1},
            {"id": 1, "items": []},
            {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": ["a"]},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": [["missing", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 2]]},
        ]
        invalid_orders.extend(
            {"id": "bad", "items": [["a", quantity]]}
            for quantity in (0, -1, 1.5, True, False, "1", None)
        )
        texts = ["[", "{}", "null"] + [
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
