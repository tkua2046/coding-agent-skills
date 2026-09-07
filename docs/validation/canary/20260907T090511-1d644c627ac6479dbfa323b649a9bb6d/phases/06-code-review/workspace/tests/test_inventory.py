import copy
import json
import unittest
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
    def test_whole_order_rejection_and_continuation(self):
        orders = [
            {"id": "reject", "items": [["a", 3], ["b", 2]]},
            {"id": "fill", "items": [["a", 4], ["b", 1]]},
            {"id": "depleted", "items": [["a", 1]]},
            {"id": "empty", "items": []},
        ]
        expected_outcomes = [
            {"order_id": "reject", "accepted": False},
            {"order_id": "fill", "accepted": True},
            {"order_id": "depleted", "accepted": False},
            {"order_id": "empty", "accepted": True},
        ]
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            for length, expected_stock in ((1, {"a": 4, "b": 1}),
                                           (4, {"a": 0, "b": 0})):
                with self.subTest(api=api, length=length):
                    stock = {"a": 4, "b": 1}
                    batch = copy.deepcopy(orders[:length])
                    original = copy.deepcopy((stock, batch))
                    remaining, outcomes = api(stock, batch)
                    self.assertEqual(remaining, expected_stock)
                    self.assertEqual(outcomes, expected_outcomes[:length])
                    self.assertEqual((stock, batch), original)
                    self.assertIsNot(remaining, stock)
                    self.assertTrue(all(type(count) is int for count in remaining.values()))
                    self.assertTrue(all(type(outcome["accepted"]) is bool for outcome in outcomes))

    def test_empty_batch_returns_copy_through_both_apis(self):
        for api in (reserve, lambda stock, orders: execute(stock, json.dumps(orders))):
            with self.subTest(api=api):
                stock = {"a": 2}
                remaining, outcomes = api(stock, [])
                self.assertEqual((remaining, outcomes), ({"a": 2}, []))
                self.assertIsNot(remaining, stock)

    def test_invalid_json_and_invalid_order_after_shortage_still_raise(self):
        payloads = [
            '{',
            json.dumps([
                {"id": "short", "items": [["a", 5]]},
                {"id": "invalid", "items": [["missing", 1]]},
            ]),
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                stock = {"a": 4}
                with self.assertRaises(ValueError):
                    execute(stock, payload)
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
