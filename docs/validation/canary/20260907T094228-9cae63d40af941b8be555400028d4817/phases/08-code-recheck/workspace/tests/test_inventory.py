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

    def assert_reservation(self, stock, orders, expected):
        for api in (reserve, execute):
            with self.subTest(api=api.__name__):
                original_stock = copy.deepcopy(stock)
                original_orders = copy.deepcopy(orders)
                payload = json.dumps(orders) if api is execute else orders
                remaining, outcomes = api(stock, payload)
                self.assertEqual((remaining, outcomes), expected)
                self.assertIsNot(remaining, stock)
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)
                for quantity in remaining.values():
                    self.assertIs(type(quantity), int)
                for outcome in outcomes:
                    self.assertIs(type(outcome["accepted"]), bool)

    def test_shortage_leaves_entire_order_unchanged(self):
        self.assert_reservation(
            {"a": 4, "b": 1},
            [{"id": "reject", "items": [["a", 3], ["b", 2]]}],
            ({"a": 4, "b": 1}, [{"order_id": "reject", "accepted": False}]),
        )

    def test_continuation_exact_stock_depletion_and_empty_order(self):
        self.assert_reservation(
            {"a": 4, "b": 1},
            [
                {"id": "reject", "items": [["a", 3], ["b", 2]]},
                {"id": "later", "items": [["a", 4], ["b", 1]]},
                {"id": "depleted", "items": [["a", 1]]},
                {"id": "empty", "items": []},
            ],
            ({"a": 0, "b": 0}, [
                {"order_id": "reject", "accepted": False},
                {"order_id": "later", "accepted": True},
                {"order_id": "depleted", "accepted": False},
                {"order_id": "empty", "accepted": True},
            ]),
        )

    def test_empty_batch_returns_copied_stock_through_both_apis(self):
        self.assert_reservation({"a": 2}, [], ({"a": 2}, []))

    def test_json_validation_regressions(self):
        invalid_payloads = [
            "{", "{}", "null", "[1]",
            '[{"id":"o"}]',
            '[{"id":"o","items":[],"extra":1}]',
            '[{"id":1,"items":[]}]',
            '[{"id":"o","items":{}}]',
            '[{"id":"o","items":["a"]}]',
            '[{"id":"o","items":[["a"]]}]',
            '[{"id":"o","items":[[1,1]]}]',
            '[{"id":"o","items":[["missing",1]]}]',
            '[{"id":"o","items":[["a",1],["a",2]]}]',
            '[{"id":"o","items":[]},{"id":"o","items":[]}]',
        ]
        for quantity in (0, -1, True, 1.5, "1", None):
            invalid_payloads.append(json.dumps([
                {"id": "o", "items": [["a", quantity]]}
            ]))
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                stock = {"a": 4}
                with self.assertRaises(ValueError):
                    execute(stock, payload)
                self.assertEqual(stock, {"a": 4})

    def test_entire_json_payload_validated_before_reservation(self):
        stock = {"a": 4}
        payload = json.dumps([
            {"id": "valid", "items": [["a", 2]]},
            {"id": "invalid", "items": [["a", 0]]},
        ])
        with patch("batch.reserve") as engine:
            with self.assertRaises(ValueError):
                execute(stock, payload)
            engine.assert_not_called()
        self.assertEqual(stock, {"a": 4})
