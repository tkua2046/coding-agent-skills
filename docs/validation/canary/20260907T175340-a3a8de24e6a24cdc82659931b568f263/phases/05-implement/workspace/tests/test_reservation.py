import copy
import json
import unittest
from unittest.mock import patch

from batch import execute
from inventory import reserve


class ReservationTests(unittest.TestCase):
    def assert_reservation(self, stock, orders, remaining, outcomes):
        for api in (reserve, execute):
            with self.subTest(api=api.__name__):
                original_stock = copy.deepcopy(stock)
                original_orders = copy.deepcopy(orders)
                argument = orders if api is reserve else json.dumps(orders)
                actual_stock, actual_outcomes = api(stock, argument)
                self.assertEqual((actual_stock, actual_outcomes), (remaining, outcomes))
                self.assertIsNot(actual_stock, stock)
                self.assertEqual(stock, original_stock)
                self.assertEqual(orders, original_orders)
                self.assertTrue(all(type(value) is int for value in actual_stock.values()))
                self.assertTrue(all(type(result["accepted"]) is bool for result in actual_outcomes))

    def test_late_shortage_preserves_all_items_and_continues(self):
        self.assert_reservation(
            {"a": 4, "b": 1},
            [{"id": "reject", "items": [["a", 2], ["b", 2]]},
             {"id": "consume", "items": [["a", 4]]},
             {"id": "empty", "items": []}],
            {"a": 0, "b": 1},
            [{"order_id": "reject", "accepted": False},
             {"order_id": "consume", "accepted": True},
             {"order_id": "empty", "accepted": True}],
        )

    def test_availability_tracks_prior_successes_only(self):
        self.assert_reservation(
            {"a": 4},
            [{"id": "first", "items": [["a", 3]]},
             {"id": "short", "items": [["a", 2]]},
             {"id": "last", "items": [["a", 1]]}],
            {"a": 0},
            [{"order_id": "first", "accepted": True},
             {"order_id": "short", "accepted": False},
             {"order_id": "last", "accepted": True}],
        )

    def test_zero_stock_rejects_without_consuming_other_items(self):
        self.assert_reservation(
            {"a": 0, "b": 2},
            [{"id": "zero", "items": [["a", 1], ["b", 1]]}],
            {"a": 0, "b": 2},
            [{"order_id": "zero", "accepted": False}],
        )

    def test_success_deducts_every_item_including_exact_stock(self):
        self.assert_reservation(
            {"a": 4, "b": 2},
            [{"id": "success", "items": [["a", 4], ["b", 1]]}],
            {"a": 0, "b": 1},
            [{"order_id": "success", "accepted": True}],
        )

    def test_empty_order_and_batch(self):
        self.assert_reservation({"a": 2}, [], {"a": 2}, [])
        self.assert_reservation(
            {}, [{"id": "empty", "items": []}], {},
            [{"order_id": "empty", "accepted": True}],
        )

    def test_json_validation_finishes_before_engine_invocation(self):
        # A valid but insufficient first order must not mask a later invalid order.
        invalid_orders = [
            None,
            {"id": "bad"},
            {"id": "bad", "items": [], "extra": 1},
            {"id": 3, "items": []},
            {"id": "first", "items": []},
            {"id": "bad", "items": {}},
            {"id": "bad", "items": [["a"]]},
            {"id": "bad", "items": [["unknown", 1]]},
            {"id": "bad", "items": [["a", 1], ["a", 1]]},
        ] + [{"id": "bad", "items": [["a", quantity]]}
             for quantity in (0, -1, True, 1.5, "1")]
        texts = ["{", "{}"] + [
            json.dumps([{"id": "first", "items": [["a", 9]]}, invalid])
            for invalid in invalid_orders
        ]
        for text in texts:
            with self.subTest(text=text), patch("batch.reserve") as engine:
                stock = {"a": 4}
                with self.assertRaises(ValueError):
                    execute(stock, text)
                engine.assert_not_called()
                self.assertEqual(stock, {"a": 4})
