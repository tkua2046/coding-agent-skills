import unittest

from inventory import reserve_batches


class ExistingAPI(unittest.TestCase):
    def test_single_sku_and_continuation(self):
        self.assertEqual(
            reserve_batches({"a": 2}, [{"a": 3}, {"a": 1}]),
            ({"a": 1}, [False, True]),
        )

    def test_caller_inputs_are_unchanged(self):
        stock, batches = {"a": 2}, [{"a": 1}]
        reserve_batches(stock, batches)
        self.assertEqual(stock, {"a": 2})
        self.assertEqual(batches, [{"a": 1}])

    def test_missing_sku_is_unavailable(self):
        self.assertEqual(reserve_batches({}, [{"x": 1}]), ({}, [False]))
