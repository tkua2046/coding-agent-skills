import copy
import json
import unittest
from unittest.mock import patch
from inventory import reserve
from batch import execute

class InventoryTests(unittest.TestCase):
    def test_whole_order_rejection_through_both_apis(self):
        orders = [
            {"id": "first", "items": [["a", 1]]},
            {"id": "reject", "items": [["a", 3], ["b", 2]]},
            {"id": "later", "items": [["a", 4], ["b", 1]]},
            {"id": "empty", "items": []},
            {"id": "exhausted", "items": [["a", 1]]},
        ]
        expected_stock = [
            {"a": 5, "b": 1}, {"a": 4, "b": 1}, {"a": 4, "b": 1},
            {"a": 0, "b": 0}, {"a": 0, "b": 0}, {"a": 0, "b": 0},
        ]
        expected_outcomes = [
            {"order_id": "first", "accepted": True},
            {"order_id": "reject", "accepted": False},
            {"order_id": "later", "accepted": True},
            {"order_id": "empty", "accepted": True},
            {"order_id": "exhausted", "accepted": False},
        ]
        for api in (reserve, execute):
            for length in range(len(orders) + 1):
                with self.subTest(api=api.__name__, prefix=length):
                    stock = {"a": 5, "b": 1}
                    batch = copy.deepcopy(orders[:length])
                    original_stock, original_orders = copy.deepcopy((stock, batch))
                    argument = batch if api is reserve else json.dumps(batch)
                    remaining, outcomes = api(stock, argument)
                    self.assertEqual(remaining, expected_stock[length])
                    self.assertEqual(outcomes, expected_outcomes[:length])
                    self.assertIsNot(remaining, stock)
                    self.assertEqual(stock, original_stock)
                    self.assertEqual(batch, original_orders)
                    self.assertTrue(all(type(n) is int for n in remaining.values()))
                    self.assertTrue(all(type(o["accepted"]) is bool for o in outcomes))

    def test_invalid_json_batch_never_reaches_reservation(self):
        valid = {"id": "first", "items": [["a", 1]]}
        invalid_orders = [
            None,
            {"id": "bad"},
            {"id": "bad", "items": [], "extra": 1},
            {"id": 1, "items": []},
            {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": ["a"]},
            {"id": "bad", "items": [[1, 1]]},
            {"id": "bad", "items": [["missing", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 1]]},
        ] + [
            {"id": "bad", "items": [["a", quantity]]}
            for quantity in (0, -1, True, 1.5, "1", None)
        ]
        texts = ["{", "{}"] + [json.dumps([valid, invalid]) for invalid in invalid_orders]
        for text in texts:
            with self.subTest(text=text):
                stock = {"a": 4}
                with patch("batch.reserve") as reservation:
                    with self.assertRaises(ValueError):
                        execute(stock, text)
                    reservation.assert_not_called()
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
